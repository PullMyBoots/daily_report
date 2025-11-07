#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号自动发布脚本
使用微信公众号官方 API 实现文章自动发布
"""

import os
import requests
import json
import time
from pathlib import Path
from typing import Dict, Optional


class WeChatPublisher:
    """微信公众号发布器"""
    
    def __init__(self, app_id: str, app_secret: str):
        """
        初始化发布器
        
        Args:
            app_id: 微信公众号 AppID
            app_secret: 微信公众号 AppSecret
        """
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token = None
        self.token_expires_at = 0
        
    def get_access_token(self, force_refresh: bool = False) -> str:
        """
        获取 Access Token
        
        Args:
            force_refresh: 是否强制刷新
            
        Returns:
            access_token
        """
        # 检查是否需要刷新（提前5分钟刷新）
        if not force_refresh and self.access_token and time.time() < self.token_expires_at - 300:
            return self.access_token
            
        url = "https://api.weixin.qq.com/cgi-bin/token"
        params = {
            "grant_type": "client_credential",
            "appid": self.app_id,
            "secret": self.app_secret
        }
        
        response = requests.get(url, params=params)
        result = response.json()
        
        if "access_token" in result:
            self.access_token = result["access_token"]
            # access_token 有效期 7200 秒（2小时）
            self.token_expires_at = time.time() + result.get("expires_in", 7200)
            print(f"✅ Access Token 获取成功，有效期至: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.token_expires_at))}")
            return self.access_token
        else:
            raise Exception(f"获取 Access Token 失败: {result}")
    
    def upload_image(self, image_path: str) -> str:
        """
        上传图片素材
        
        Args:
            image_path: 图片路径（本地路径）
            
        Returns:
            media_id
        """
        access_token = self.get_access_token()
        url = f"https://api.weixin.qq.com/cgi-bin/material/add_material"
        params = {
            "access_token": access_token,
            "type": "image"
        }
        
        with open(image_path, 'rb') as f:
            files = {'media': (Path(image_path).name, f, 'image/jpeg')}
            response = requests.post(url, params=params, files=files)
            
        result = response.json()
        
        if "media_id" in result:
            print(f"✅ 图片上传成功: {Path(image_path).name} -> {result['media_id']}")
            return result["media_id"]
        else:
            raise Exception(f"图片上传失败: {result}")
    
    def upload_news_image(self, image_path: str) -> str:
        """
        上传图文消息内的图片
        
        Args:
            image_path: 图片路径
            
        Returns:
            图片 URL
        """
        access_token = self.get_access_token()
        url = f"https://api.weixin.qq.com/cgi-bin/media/uploadimg"
        params = {
            "access_token": access_token
        }
        
        with open(image_path, 'rb') as f:
            files = {'media': (Path(image_path).name, f, 'image/jpeg')}
            response = requests.post(url, params=params, files=files)
            
        result = response.json()
        
        if "url" in result:
            print(f"✅ 图文图片上传成功: {Path(image_path).name}")
            return result["url"]
        else:
            raise Exception(f"图文图片上传失败: {result}")
    
    def create_draft(self, articles: list) -> str:
        """
        创建草稿
        
        Args:
            articles: 文章列表，每篇文章包含:
                - title: 标题
                - author: 作者
                - digest: 摘要
                - content: 内容（HTML格式）
                - content_source_url: 原文链接
                - thumb_media_id: 封面图片 media_id
                - need_open_comment: 是否打开评论（0/1）
                - only_fans_can_comment: 是否粉丝才可评论（0/1）
                
        Returns:
            draft_media_id
        """
        access_token = self.get_access_token()
        url = f"https://api.weixin.qq.com/cgi-bin/draft/add"
        params = {
            "access_token": access_token
        }
        
        data = {
            "articles": articles
        }
        
        response = requests.post(url, params=params, json=data)
        result = response.json()
        
        if "media_id" in result:
            print(f"✅ 草稿创建成功: {result['media_id']}")
            return result["media_id"]
        else:
            raise Exception(f"草稿创建失败: {result}")
    
    def publish_draft(self, draft_media_id: str) -> Dict:
        """
        发布草稿
        
        Args:
            draft_media_id: 草稿 media_id
            
        Returns:
            发布结果
        """
        access_token = self.get_access_token()
        url = f"https://api.weixin.qq.com/cgi-bin/freepublish/submit"
        params = {
            "access_token": access_token
        }
        
        data = {
            "media_id": draft_media_id
        }
        
        response = requests.post(url, params=params, json=data)
        result = response.json()
        
        if result.get("errcode") == 0:
            print(f"✅ 文章发布成功！publish_id: {result.get('publish_id')}")
            return result
        else:
            raise Exception(f"文章发布失败: {result}")
    
    def get_draft_list(self, offset: int = 0, count: int = 20) -> Dict:
        """
        获取草稿列表
        
        Args:
            offset: 偏移量
            count: 数量（最大20）
            
        Returns:
            草稿列表
        """
        access_token = self.get_access_token()
        url = f"https://api.weixin.qq.com/cgi-bin/draft/batchget"
        params = {
            "access_token": access_token
        }
        
        data = {
            "offset": offset,
            "count": min(count, 20),
            "no_content": 0
        }
        
        response = requests.post(url, params=params, json=data)
        return response.json()
    
    def publish_article(
        self,
        title: str,
        content: str,
        thumb_image_path: str,
        author: str = "",
        digest: str = "",
        source_url: str = "",
        need_open_comment: int = 0,
        only_fans_can_comment: int = 0
    ) -> Dict:
        """
        发布文章（完整流程）
        
        Args:
            title: 标题
            content: 内容（HTML格式）
            thumb_image_path: 封面图片路径
            author: 作者
            digest: 摘要
            source_url: 原文链接
            need_open_comment: 是否打开评论
            only_fans_can_comment: 是否粉丝才可评论
            
        Returns:
            发布结果
        """
        # 1. 上传封面图片
        print(f"\n📤 上传封面图片...")
        thumb_media_id = self.upload_image(thumb_image_path)
        
        # 2. 创建草稿
        print(f"\n📝 创建草稿...")
        article_data = {
            "title": title,
            "author": author,
            "digest": digest or title[:50],  # 默认使用标题前50字作为摘要
            "content": content,
            "content_source_url": source_url,
            "thumb_media_id": thumb_media_id,
            "need_open_comment": need_open_comment,
            "only_fans_can_comment": only_fans_can_comment
        }
        
        draft_media_id = self.create_draft([article_data])
        
        # 3. 发布草稿
        print(f"\n🚀 发布文章...")
        result = self.publish_draft(draft_media_id)
        
        return result


def load_env_from_file(env_file: str = ".env") -> Dict[str, str]:
    """
    从 .env 文件加载环境变量
    
    Args:
        env_file: .env 文件路径
        
    Returns:
        环境变量字典
    """
    env_vars = {}
    if os.path.exists(env_file):
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
    return env_vars


def example_publish():
    """发布示例"""
    # 从 .env 文件或环境变量获取配置
    env_vars = load_env_from_file()
    app_id = env_vars.get('WECHAT_APP_ID') or os.getenv('WECHAT_APP_ID')
    app_secret = env_vars.get('WECHAT_APP_SECRET') or os.getenv('WECHAT_APP_SECRET')
    
    if not app_id or not app_secret:
        print("❌ 错误：请配置 WECHAT_APP_ID 和 WECHAT_APP_SECRET")
        print("方法1：创建 .env 文件并配置")
        print("方法2：设置环境变量")
        return
    
    # 创建发布器
    publisher = WeChatPublisher(app_id, app_secret)
    
    # 示例：发布一篇测试文章
    html_content = """
    <h1>测试文章标题</h1>
    <p>这是一篇测试文章，用于演示微信公众号自动发布功能。</p>
    <h2>功能特点</h2>
    <ul>
        <li>自动获取 Access Token</li>
        <li>自动上传图片素材</li>
        <li>创建草稿</li>
        <li>一键发布</li>
    </ul>
    <h2>代码示例</h2>
    <pre><code>
def hello_world():
    print("Hello, WeChat!")
    </code></pre>
    <p><strong>注意事项：</strong>使用前请确保已配置 IP 白名单。</p>
    """
    
    try:
        result = publisher.publish_article(
            title="测试文章：微信公众号自动发布",
            content=html_content,
            thumb_image_path="path/to/your/cover/image.jpg",  # 替换为实际图片路径
            author="测试作者",
            digest="这是一篇测试文章摘要",
            source_url="https://your-website.com",
            need_open_comment=1,
            only_fans_can_comment=0
        )
        
        print(f"\n🎉 发布成功！")
        print(f"结果: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
    except Exception as e:
        print(f"\n❌ 发布失败: {e}")


if __name__ == "__main__":
    print("=" * 60)
    print("微信公众号自动发布工具")
    print("=" * 60)
    
    # 运行示例
    example_publish()

