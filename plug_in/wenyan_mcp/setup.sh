#!/bin/bash

echo "======================================================================"
echo "文颜 MCP - 微信公众号自动发布工具 - 快速配置脚本"
echo "======================================================================"

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo ""
echo "📁 当前目录: $SCRIPT_DIR"

# 1. 创建 .env 文件
echo ""
echo "📝 [1/4] 创建环境变量配置文件..."

if [ -f ".env" ]; then
    echo "⚠️  .env 文件已存在"
    read -p "是否覆盖？(y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "跳过创建 .env 文件"
    else
        cat > .env << 'EOF'
WECHAT_APP_ID=wxcce79ce3dac424f8
WECHAT_APP_SECRET=6b7e108e47327cb8bac4c68dd400d074
HOST_IMAGE_PATH=/Users/dushiliren/Desktop/Self-Media/personal_growth/get_text_vocal
EOF
        echo "✅ .env 文件已创建"
    fi
else
    cat > .env << 'EOF'
WECHAT_APP_ID=wxcce79ce3dac424f8
WECHAT_APP_SECRET=6b7e108e47327cb8bac4c68dd400d074
HOST_IMAGE_PATH=/Users/dushiliren/Desktop/Self-Media/personal_growth/get_text_vocal
EOF
    echo "✅ .env 文件已创建"
fi

# 2. 检查 Python
echo ""
echo "🐍 [2/4] 检查 Python 环境..."

if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ 找到 Python: $PYTHON_VERSION"
else
    echo "❌ 未找到 Python3"
    echo "请先安装 Python 3: https://www.python.org/"
    exit 1
fi

# 3. 安装 Python 依赖
echo ""
echo "📦 [3/4] 安装 Python 依赖..."

if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt -q
    if [ $? -eq 0 ]; then
        echo "✅ Python 依赖安装完成"
    else
        echo "❌ Python 依赖安装失败"
        exit 1
    fi
else
    echo "⚠️  未找到 requirements.txt"
fi

# 4. 获取本机 IP
echo ""
echo "🌐 [4/4] 获取本机公网 IP..."

if command -v curl &> /dev/null; then
    PUBLIC_IP=$(curl -s ifconfig.me)
    if [ -n "$PUBLIC_IP" ]; then
        echo "✅ 你的公网 IP: $PUBLIC_IP"
        echo ""
        echo "⚠️  重要提醒：请将此 IP 添加到微信公众号平台的白名单中！"
        echo ""
        echo "操作步骤："
        echo "  1. 登录：https://mp.weixin.qq.com/"
        echo "  2. 进入：开发 → 基本配置 → IP白名单"
        echo "  3. 添加 IP: $PUBLIC_IP"
        echo "  4. 保存并等待 5-10 分钟生效"
    else
        echo "⚠️  无法获取公网 IP"
        echo "请访问 https://www.ip.cn/ 查看你的 IP"
    fi
else
    echo "⚠️  未安装 curl，无法自动获取 IP"
    echo "请访问 https://www.ip.cn/ 查看你的 IP"
fi

# 完成
echo ""
echo "======================================================================"
echo "✅ 配置完成！"
echo "======================================================================"
echo ""
echo "下一步："
echo ""
echo "1. 测试 API 连接："
echo "   python3 test_api.py"
echo ""
echo "2. 发布示例文章："
echo "   python3 publish_to_wechat.py example_article.md /path/to/cover.jpg"
echo ""
echo "3. 或者安装全局 MCP 服务（与 AI 集成）："
echo "   npm install -g @wenyan-md/mcp"
echo ""
echo "详细文档：查看 CONFIGURED.md 和 QUICKSTART.md"
echo ""

