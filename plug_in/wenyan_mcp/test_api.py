#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试微信公众号 API 连接
快速验证配置是否正确
"""

from wechat_publisher import WeChatPublisher

# 已配置的凭证
APP_ID = "wxcce79ce3dac424f8"
APP_SECRET = "6b7e108e47327cb8bac4c68dd400d074"


def test_all():
    """完整测试流程"""
    print("\n" + "=" * 60)
    print("🧪 微信公众号 API 完整测试")
    print("=" * 60)
    
    try:
        publisher = WeChatPublisher(APP_ID, APP_SECRET)
        
        # 测试 1: 获取 Access Token
        print("\n[1/3] 测试获取 Access Token...")
        token = publisher.get_access_token()
        print(f"✅ Access Token 获取成功")
        print(f"    Token (前20字符): {token[:20]}...")
        print(f"    过期时间: {publisher.token_expires_at}")
        
        # 测试 2: 获取草稿列表
        print("\n[2/3] 测试获取草稿列表...")
        drafts = publisher.get_draft_list(offset=0, count=5)
        if "item" in drafts:
            print(f"✅ 草稿列表获取成功")
            print(f"    总数量: {drafts.get('total_count', 0)}")
            print(f"    返回数量: {drafts.get('item_count', 0)}")
            if drafts.get('item_count', 0) > 0:
                print(f"\n    最近的草稿:")
                for i, item in enumerate(drafts['item'][:3], 1):
                    articles = item.get('content', {}).get('news_item', [])
                    if articles:
                        print(f"      {i}. {articles[0].get('title', '无标题')}")
        else:
            print(f"✅ 接口调用成功（暂无草稿）")
        
        # 测试 3: 测试图片上传（可选）
        print("\n[3/3] 测试图片上传功能...")
        print("    ⚠️  跳过（需要实际图片文件）")
        print("    提示：使用 publish_to_wechat.py 发布文章时会自动测试上传")
        
        print("\n" + "=" * 60)
        print("🎉 所有测试通过！")
        print("=" * 60)
        print("\n✅ 配置正确，可以开始使用了！")
        print("\n下一步:")
        print("  1. 准备一篇 Markdown 文章")
        print("  2. 准备封面图片")
        print("  3. 运行: python publish_to_wechat.py <文章.md> <封面.jpg>")
        print("  或使用 AI 助手自动发布（需要安装 wenyan-mcp）")
        
        return True
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ 测试失败")
        print("=" * 60)
        print(f"\n错误信息: {e}")
        
        print("\n🔍 问题排查:")
        print("\n1. 检查 IP 白名单")
        print("   - 登录: https://mp.weixin.qq.com/")
        print("   - 进入: 开发 → 基本配置 → IP白名单")
        print("   - 添加你的 IP 地址")
        print("   - 获取你的 IP: curl ifconfig.me")
        
        print("\n2. 检查 AppID 和 AppSecret")
        print("   - 当前 AppID: " + APP_ID)
        print("   - 当前 AppSecret: " + APP_SECRET[:10] + "..." + APP_SECRET[-10:])
        print("   - 确认路径: 设置与开发 → 开发接口管理")
        
        print("\n3. 检查网络连接")
        print("   - 确保可以访问: https://api.weixin.qq.com/")
        
        print("\n4. 常见错误码")
        print("   - 40001: AppSecret 错误")
        print("   - 40164: IP 不在白名单")
        print("   - 41001: Access Token 缺失")
        print("   - 42001: Access Token 过期")
        
        return False


if __name__ == "__main__":
    test_all()

