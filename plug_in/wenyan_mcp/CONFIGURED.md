# ✅ 配置完成！

## 🎉 已完成配置

你的微信公众号凭证已配置完成：

- **AppID**: `wxcce79ce3dac424f8`
- **AppSecret**: `6b7e108e47327cb8bac4c68dd400d074`

## 📝 环境变量配置

请创建 `.env` 文件（已被 git 忽略，安全）：

```bash
# 复制以下内容到 .env 文件
WECHAT_APP_ID=wxcce79ce3dac424f8
WECHAT_APP_SECRET=6b7e108e47327cb8bac4c68dd400d074
HOST_IMAGE_PATH=/Users/dushiliren/Desktop/Self-Media/personal_growth/get_text_vocal
```

快速创建命令：

```bash
cd /Users/dushiliren/Desktop/Self-Media/personal_growth/get_text_vocal/plug_in/wenyan_mcp

cat > .env << 'EOF'
WECHAT_APP_ID=wxcce79ce3dac424f8
WECHAT_APP_SECRET=6b7e108e47327cb8bac4c68dd400d074
HOST_IMAGE_PATH=/Users/dushiliren/Desktop/Self-Media/personal_growth/get_text_vocal
EOF
```

## ⚠️ 重要：配置 IP 白名单

**必须先配置 IP 白名单，否则 API 调用会失败！**

### 步骤：

1. **获取你的公网 IP**：
```bash
curl ifconfig.me
```

2. **登录微信公众号平台**：
   - 访问：https://mp.weixin.qq.com/
   - 使用管理员账号登录

3. **添加 IP 白名单**：
   - 点击左侧：**开发** → **基本配置**
   - 找到 **IP白名单** 部分
   - 点击 **修改**
   - 添加你的 IP 地址
   - 保存并等待 5-10 分钟生效

## 🧪 测试配置

### 方法 1：快速测试（推荐）

```bash
cd /Users/dushiliren/Desktop/Self-Media/personal_growth/get_text_vocal/plug_in/wenyan_mcp

# 安装依赖
pip install -r requirements.txt

# 运行测试
python test_api.py
```

### 方法 2：完整测试

```bash
# 测试发布文章
python publish_to_wechat.py test

# 发布示例文章（需要先准备封面图）
python publish_to_wechat.py example_article.md /path/to/cover.jpg
```

## 🚀 开始使用

### 方式 A：使用 AI 助手（推荐）

1. **全局安装 wenyan-mcp**：
```bash
npm install -g @wenyan-md/mcp
```

2. **配置你的 AI 工具**（Cursor/Claude Desktop）

找到 MCP 配置文件并添加：

**Cursor**: 设置 → MCP 配置

**Claude Desktop**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "wenyan-mcp": {
      "name": "公众号助手",
      "command": "wenyan-mcp",
      "env": {
        "WECHAT_APP_ID": "wxcce79ce3dac424f8",
        "WECHAT_APP_SECRET": "6b7e108e47327cb8bac4c68dd400d074"
      }
    }
  }
}
```

3. **重启 AI 工具**

4. **开始使用**：

对 AI 说：
- "帮我测试一下微信公众号连接"
- "把这篇文章发布到公众号"
- "查看可用的公众号主题"

### 方式 B：使用 Python 脚本

```bash
# 测试连接
python test_api.py

# 发布文章
python publish_to_wechat.py your_article.md cover_image.jpg
```

## 📖 文章格式要求

创建 Markdown 文章时，需要包含 frontmatter：

```markdown
---
title: 你的文章标题
cover: /path/to/cover.jpg
---

# 文章正文开始

这里是你的内容...
```

## 🎨 可用主题

- Orange Heart（温暖橙色）
- Rainbow（彩虹渐变）⭐ 推荐
- Lapis（优雅蓝调）
- Pie（简约清新）
- Maize（活力黄色）
- Purple（神秘紫色）
- 物理猫-薄荷（清新薄荷）

查看效果：https://yuzhi.tech/docs/wenyan/themes

## 🔧 可用脚本

| 脚本 | 用途 |
|------|------|
| `test_api.py` | 测试 API 连接和配置 |
| `publish_to_wechat.py` | 发布文章到公众号 |
| `wechat_publisher.py` | 底层 API 封装（供开发使用） |

## 📂 目录中的现有文章

你可以直接使用这些已有的文章测试发布：

### 深度平台文章

```bash
# 公众号平台文章
ls -la ../../_deep_platforms/gongzhonghao/publish/

# 今日头条文章
ls -la ../../_deep_platforms/daily_toutiao/publish/
```

### 快速平台文章

```bash
# 小红书文章
ls -la ../../_quick_platforms/rednote/publish/
```

## 🎯 快速开始示例

### 示例 1：发布现有公众号文章

```bash
cd /Users/dushiliren/Desktop/Self-Media/personal_growth/get_text_vocal/plug_in/wenyan_mcp

# 假设你有封面图
python publish_to_wechat.py \
  ../../_deep_platforms/gongzhonghao/publish/领导力勇气_西蒙斯涅克_公众号版.md \
  /path/to/cover.jpg
```

### 示例 2：使用 AI 助手

```
你：帮我把 "领导力勇气_西蒙斯涅克_公众号版.md" 发布到微信公众号，使用 Rainbow 主题

AI：好的，我来帮你发布...
    [自动完成排版、上传、发布]
```

## 🐛 常见问题

### 问题 1：API 调用返回 40164

**原因**：IP 不在白名单

**解决**：参考上面"配置 IP 白名单"部分

### 问题 2：Access Token 无效 (40001)

**原因**：AppID 或 AppSecret 错误

**解决**：检查配置是否正确

### 问题 3：图片上传失败

**原因**：
- 图片路径不存在
- 图片格式不支持（仅支持 JPG/PNG）
- 图片太大（建议 < 2MB）

**解决**：
```bash
# 检查图片
ls -lh /path/to/image.jpg

# 查看图片大小
du -h /path/to/image.jpg
```

## 📚 更多文档

- **QUICKSTART.md**: 快速开始指南
- **README.md**: 完整功能文档
- **config.json**: MCP 配置示例
- **example_article.md**: 示例文章

## 🔗 相关链接

- 微信公众号平台：https://mp.weixin.qq.com/
- 文颜项目：https://github.com/caol64/wenyan-mcp
- 主题预览：https://yuzhi.tech/docs/wenyan/themes
- 微信开发文档：https://developers.weixin.qq.com/

---

**现在开始测试吧！** 🚀

```bash
python test_api.py
```

