#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号发布脚本 - 已配置好的版本
直接运行即可发布文章
"""

import os
import sys
from pathlib import Path
from wechat_publisher import WeChatPublisher

# 已配置的微信公众号凭证
APP_ID = "wxcce79ce3dac424f8"
APP_SECRET = "6b7e108e47327cb8bac4c68dd400d074"


def publish_markdown_to_wechat(
    md_file_path: str,
    cover_image_path: str = None,
    author: str = "",
    theme: str = "rainbow"
):
    """
    发布 Markdown 文件到微信公众号
    
    Args:
        md_file_path: Markdown 文件路径
        cover_image_path: 封面图片路径（可选）
        author: 作者名（可选）
        theme: 主题名称（可选）
    """
    if not os.path.exists(md_file_path):
        print(f"❌ 错误：文件不存在 - {md_file_path}")
        return False
    
    print(f"\n{'=' * 60}")
    print(f"📝 准备发布文章到微信公众号")
    print(f"{'=' * 60}")
    print(f"文件: {md_file_path}")
    
    # 读取 Markdown 文件
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 简单解析 frontmatter
    title = None
    cover = cover_image_path
    
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            md_content = parts[2].strip()
            
            # 解析 frontmatter
            for line in frontmatter.strip().split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    if key == 'title':
                        title = value
                    elif key == 'cover' and not cover:
                        cover = value
        else:
            md_content = content
    else:
        md_content = content
    
    if not title:
        # 尝试从第一个标题提取
        for line in md_content.split('\n'):
            if line.startswith('# '):
                title = line[2:].strip()
                break
    
    if not title:
        title = Path(md_file_path).stem
    
    print(f"标题: {title}")
    print(f"封面: {cover if cover else '(将从文章中提取)'}")
    print(f"作者: {author if author else '(未设置)'}")
    
    # 将 Markdown 转换为 HTML（简单版本）
    # 注意：实际使用中建议使用 markdown 库或直接使用 wenyan-mcp
    html_content = f"<div>{md_content.replace(chr(10), '<br>')}</div>"
    
    try:
        # 创建发布器
        publisher = WeChatPublisher(APP_ID, APP_SECRET)
        
        # 如果没有封面图，需要提供一个默认的
        if not cover:
            print("\n⚠️  警告：未提供封面图片")
            print("建议：在 Markdown 文件的 frontmatter 中添加 cover 字段")
            print("或者在调用时传入 cover_image_path 参数")
            return False
        
        # 发布文章
        result = publisher.publish_article(
            title=title,
            content=html_content,
            thumb_image_path=cover,
            author=author,
            digest=title[:50],  # 使用标题前50字作为摘要
        )
        
        print(f"\n{'=' * 60}")
        print(f"🎉 发布成功！")
        print(f"{'=' * 60}")
        print(f"Publish ID: {result.get('publish_id', 'N/A')}")
        print(f"\n请登录微信公众号后台查看文章草稿")
        
        return True
        
    except Exception as e:
        print(f"\n{'=' * 60}")
        print(f"❌ 发布失败")
        print(f"{'=' * 60}")
        print(f"错误信息: {e}")
        print(f"\n常见问题排查:")
        print(f"1. 检查 IP 是否在白名单中")
        print(f"2. 检查 AppID 和 AppSecret 是否正确")
        print(f"3. 检查网络连接")
        print(f"4. 检查图片路径是否正确")
        return False


def test_connection():
    """测试连接和配置"""
    print(f"\n{'=' * 60}")
    print(f"🔧 测试微信公众号 API 连接")
    print(f"{'=' * 60}")
    
    try:
        publisher = WeChatPublisher(APP_ID, APP_SECRET)
        token = publisher.get_access_token()
        
        print(f"✅ 连接成功！")
        print(f"Access Token (前20字符): {token[:20]}...")
        print(f"\n配置信息:")
        print(f"AppID: {APP_ID}")
        print(f"AppSecret: {APP_SECRET[:10]}...{APP_SECRET[-10:]}")
        
        return True
        
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        print(f"\n请检查:")
        print(f"1. AppID 和 AppSecret 是否正确")
        print(f"2. 服务器 IP 是否在白名单中")
        print(f"3. 网络连接是否正常")
        return False


def main():
    """主函数"""
    print("=" * 60)
    print("微信公众号自动发布工具")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        print("\n使用方法:")
        print(f"  测试连接: python {sys.argv[0]} test")
        print(f"  发布文章: python {sys.argv[0]} <markdown文件路径> [封面图片路径]")
        print(f"\n示例:")
        print(f"  python {sys.argv[0]} test")
        print(f"  python {sys.argv[0]} example_article.md")
        print(f"  python {sys.argv[0]} my_article.md /path/to/cover.jpg")
        return
    
    if sys.argv[1] == "test":
        test_connection()
    else:
        md_file = sys.argv[1]
        cover = sys.argv[2] if len(sys.argv) > 2 else None
        publish_markdown_to_wechat(md_file, cover)


if __name__ == "__main__":
    main()

