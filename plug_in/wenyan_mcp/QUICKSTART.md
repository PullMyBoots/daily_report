# 快速开始指南

## 🚀 快速配置（5分钟搞定）

### 第一步：获取微信公众号凭证

1. 登录 [微信公众号平台](https://mp.weixin.qq.com/)
2. 点击左侧菜单：**设置与开发** → **开发接口管理**
3. 复制并保存：
   - `AppID`（应用ID）
   - `AppSecret`（应用密钥）

### 第二步：配置 IP 白名单 ⚠️

**这一步非常重要！不配置会导致 API 调用失败**

1. 在微信公众号平台，点击：**开发** → **基本配置**
2. 找到 **IP白名单** 部分
3. 点击 **修改**，添加你的服务器 IP 地址

**如何获取本机 IP？**

```bash
# macOS/Linux
curl ifconfig.me

# 或者访问
# https://www.ip.cn/
```

### 第三步：创建配置文件

在当前目录创建 `.env` 文件：

```bash
# 复制模板
cp env_template.txt .env

# 编辑配置（使用你喜欢的编辑器）
nano .env
# 或
vim .env
# 或
code .env
```

填入你的配置：

```env
WECHAT_APP_ID=wx1234567890abcdef
WECHAT_APP_SECRET=1234567890abcdef1234567890abcdef
HOST_IMAGE_PATH=/Users/你的用户名/Desktop/Self-Media/personal_growth/get_text_vocal
```

### 第四步：选择使用方式

#### 方式 A：使用 MCP + AI 助手（推荐，最智能）

适合：想要 AI 自动帮你排版发布的用户

**1. 全局安装 wenyan-mcp**

```bash
npm install -g @wenyan-md/mcp
```

**2. 配置你的 AI 工具（如 Cursor、Claude Desktop）**

找到 MCP 配置文件：
- **Cursor**: `~/.cursor/mcp.json` 或 Cursor 设置中的 MCP 配置
- **Claude Desktop**: `~/Library/Application Support/Claude/claude_desktop_config.json`

添加以下配置：

```json
{
  "mcpServers": {
    "wenyan-mcp": {
      "name": "公众号助手",
      "command": "wenyan-mcp",
      "env": {
        "WECHAT_APP_ID": "wx1234567890abcdef",
        "WECHAT_APP_SECRET": "1234567890abcdef1234567890abcdef"
      }
    }
  }
}
```

**3. 重启你的 AI 工具**

**4. 开始使用**

对 AI 说：
- "帮我把这篇文章发布到微信公众号"
- "使用 Rainbow 主题发布这篇文章到公众号草稿箱"
- "查看可用的公众号主题"

AI 会自动帮你：
- ✅ 选择合适的主题
- ✅ 排版文章
- ✅ 上传图片
- ✅ 发布到草稿箱

#### 方式 B：使用 Python 脚本（程序员友好）

适合：想要完全控制发布流程的开发者

**1. 安装依赖**

```bash
pip install -r requirements.txt
```

**2. 编辑 `wechat_publisher.py`**

修改 `example_publish()` 函数中的示例内容，或者创建自己的发布脚本。

**3. 运行发布**

```bash
python wechat_publisher.py
```

**4. 自定义发布示例**

```python
from wechat_publisher import WeChatPublisher

# 创建发布器
publisher = WeChatPublisher(
    app_id="你的AppID",
    app_secret="你的AppSecret"
)

# 发布文章
result = publisher.publish_article(
    title="我的第一篇文章",
    content="<p>这是文章内容，支持HTML格式</p>",
    thumb_image_path="/path/to/cover.jpg",
    author="作者名",
    digest="文章摘要"
)

print(f"发布成功！{result}")
```

## 📝 准备你的文章

### Markdown 格式要求

每篇文章开头需要包含 frontmatter：

```markdown
---
title: 文章标题（必填）
cover: /path/to/cover.jpg（可选）
---

# 正文开始

这里是你的文章内容...

![示例图片](https://example.com/image.jpg)
```

**字段说明：**

| 字段 | 必填 | 说明 |
|------|------|------|
| title | ✅ | 文章标题 |
| cover | ❌ | 封面图片（本地路径或网络URL）<br>如果正文有图片可省略 |

### 图片要求

- ✅ 支持本地路径：`/Users/username/Pictures/cover.jpg`
- ✅ 支持网络URL：`https://example.com/image.jpg`
- ✅ 格式支持：JPG、PNG
- ⚠️ 大小限制：建议 < 2MB

## 🎨 可用主题

文颜提供了多个精美主题：

| 主题名称 | 风格 |
|---------|------|
| Orange Heart | 温暖橙色 |
| Rainbow | 彩虹渐变 |
| Lapis | 优雅蓝调 |
| Pie | 简约清新 |
| Maize | 活力黄色 |
| Purple | 神秘紫色 |
| 物理猫-薄荷 | 清新薄荷 |

👉 [查看主题预览](https://yuzhi.tech/docs/wenyan/themes)

## 🔧 常用命令

```bash
# 全局安装 wenyan-mcp
npm install -g @wenyan-md/mcp

# 更新到最新版
npm update -g @wenyan-md/mcp

# 查看版本
npm list -g @wenyan-md/mcp

# 使用 Inspector 调试
npx @modelcontextprotocol/inspector

# Python 依赖安装
pip install -r requirements.txt

# 运行 Python 发布脚本
python wechat_publisher.py
```

## 🐛 常见问题排查

### 1️⃣ 错误：40164 - IP不在白名单

**症状：** API 调用返回 `errcode: 40164`

**原因：** 服务器 IP 未添加到白名单

**解决：**
1. 获取你的公网 IP：访问 https://www.ip.cn/
2. 在微信公众号平台添加到白名单
3. 等待 5-10 分钟生效

### 2️⃣ 错误：40001 - Access Token 无效

**症状：** `errcode: 40001, invalid credential`

**原因：** AppID 或 AppSecret 配置错误

**解决：**
1. 检查 `.env` 文件中的配置
2. 确认没有多余的空格或引号
3. 重新从微信平台复制 AppID 和 AppSecret

### 3️⃣ 图片上传失败

**原因可能：**
- 图片路径不存在
- 图片格式不支持（仅支持 JPG、PNG）
- 图片大小超过限制（建议 < 2MB）

**解决：**
```bash
# 检查图片是否存在
ls -lh /path/to/image.jpg

# 检查图片大小
du -h /path/to/image.jpg

# 压缩图片（如果太大）
# 使用在线工具或命令行工具压缩
```

### 4️⃣ 文章发布后格式不对

**原因：** Markdown 转 HTML 格式问题

**解决：**
- 使用 MCP 方式，文颜会自动处理排版
- 使用 Python 方式，需要确保 content 是正确的 HTML 格式

### 5️⃣ MCP 无法连接

**症状：** AI 工具提示无法连接到 wenyan-mcp

**解决：**
1. 检查是否全局安装：`npm list -g @wenyan-md/mcp`
2. 检查 MCP 配置文件路径是否正确
3. 重启 AI 工具
4. 查看 AI 工具的日志输出

## 📚 API 接口说明

### 核心流程

```
1. 获取 Access Token
   ↓
2. 上传封面图片 → 获取 media_id
   ↓
3. 创建草稿（包含文章内容）→ 获取 draft_media_id
   ↓
4. 发布草稿到公众号
```

### 主要接口

| 接口 | 用途 | 文档 |
|------|------|------|
| `/cgi-bin/token` | 获取 access_token | [文档](https://developers.weixin.qq.com/doc/offiaccount/Basic_Information/Get_access_token.html) |
| `/cgi-bin/material/add_material` | 上传永久素材 | [文档](https://developers.weixin.qq.com/doc/offiaccount/Asset_Management/New_temporary_materials.html) |
| `/cgi-bin/draft/add` | 新建草稿 | [文档](https://developers.weixin.qq.com/doc/offiaccount/Draft_Box/Add_draft.html) |
| `/cgi-bin/freepublish/submit` | 发布草稿 | [文档](https://developers.weixin.qq.com/doc/offiaccount/Publish/Publish.html) |

## 🔗 相关资源

- 📦 **GitHub 项目**: https://github.com/caol64/wenyan-mcp
- 📖 **官方文档**: https://yuzhi.tech/docs/wenyan/
- 🎨 **主题预览**: https://yuzhi.tech/docs/wenyan/themes
- 📝 **微信官方文档**: https://developers.weixin.qq.com/doc/offiaccount/Getting_Started/Overview.html
- 🔧 **IP白名单配置**: https://yuzhi.tech/docs/wenyan/upload

## 💡 使用技巧

### 技巧 1：批量发布

创建一个脚本批量处理多篇文章：

```python
articles = [
    {"title": "文章1", "content": "...", "cover": "..."},
    {"title": "文章2", "content": "...", "cover": "..."},
]

for article in articles:
    publisher.publish_article(**article)
    time.sleep(5)  # 避免频率限制
```

### 技巧 2：定时发布

使用 cron (macOS/Linux) 或 Task Scheduler (Windows) 实现定时发布：

```bash
# 每天上午 9:00 发布
0 9 * * * /usr/bin/python3 /path/to/wechat_publisher.py
```

### 技巧 3：Markdown 转 HTML

如果需要自己转换 Markdown：

```python
import markdown

md_content = "# 标题\n\n这是内容"
html_content = markdown.markdown(md_content)
```

## ⚠️ 重要限制

- 📊 **Access Token 有效期**: 2小时（工具会自动刷新）
- 🔢 **API 调用频率**: 有限制，建议间隔 2-5 秒
- 📅 **群发限制**: 
  - 订阅号：每天 1 次
  - 服务号：每月 4 次
- 📝 **内容审核**: 文章需符合微信平台规范

## 🎉 开始使用

现在你已经完成了所有配置！试试发布你的第一篇文章吧！

### 使用 AI 助手（推荐）

```
你：帮我把 example_article.md 发布到微信公众号

AI：好的，我来帮你发布...
    ✅ 已选择 Rainbow 主题
    ✅ 图片已上传
    ✅ 草稿已创建
    ✅ 文章已发布到草稿箱
    
    请登录公众号后台查看并发布！
```

### 使用 Python 脚本

```bash
python wechat_publisher.py
```

---

**祝你使用愉快！如有问题，请查看 README.md 或访问项目主页。** 🚀

