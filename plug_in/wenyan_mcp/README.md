# 文颜 MCP Server - 微信公众号自动发布工具

> 项目地址：https://github.com/caol64/wenyan-mcp

## 📝 简介

文颜 MCP Server 是一个基于模型上下文协议（Model Context Protocol, MCP）的工具，可以让 AI 自动将 Markdown 文章排版后发布至微信公众号草稿箱。

## ✨ 功能特性

- ✅ 列出并选择支持的文章主题（多个精美主题可选）
- ✅ 使用内置主题对 Markdown 内容排版
- ✅ 发布文章到微信公众号草稿箱
- ✅ 自动上传本地或网络图片
- ✅ 支持自定义封面图片

## 📦 安装说明

已通过 npm 安装到当前目录：

```bash
npm install @wenyan-md/mcp
```

## 🔧 配置步骤

### 1. 获取微信公众号 App ID 和 App Secret

1. 登录 [微信公众号平台](https://mp.weixin.qq.com/)
2. 进入"设置与开发" → "开发接口管理"
3. 复制 `AppID` 和 `AppSecret`

### 2. 配置 IP 白名单

**重要**：必须将服务器 IP 加入公众号平台的 IP 白名单，以确保上传接口调用成功。

1. 在微信公众号平台进入"开发" → "基本配置"
2. 添加服务器 IP 到白名单

详细配置说明：https://yuzhi.tech/docs/wenyan/upload

### 3. 配置环境变量

复制 `.env.example` 为 `.env` 并填入你的配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
WECHAT_APP_ID=你的AppID
WECHAT_APP_SECRET=你的AppSecret
HOST_IMAGE_PATH=/你的图片目录路径
```

### 4. 与 AI 工具集成（如 Cursor、Claude Desktop）

在你的 MCP 配置文件中添加配置。

#### 方式一：使用全局安装的 wenyan-mcp

首先全局安装：

```bash
npm install -g @wenyan-md/mcp
```

然后在 MCP 配置文件中添加：

```json
{
  "mcpServers": {
    "wenyan-mcp": {
      "name": "公众号助手",
      "command": "wenyan-mcp",
      "env": {
        "WECHAT_APP_ID": "your_app_id",
        "WECHAT_APP_SECRET": "your_app_secret"
      }
    }
  }
}
```

#### 方式二：使用 npx（推荐）

```json
{
  "mcpServers": {
    "wenyan-mcp": {
      "name": "公众号助手",
      "command": "npx",
      "args": ["@wenyan-md/mcp"],
      "env": {
        "WECHAT_APP_ID": "your_app_id",
        "WECHAT_APP_SECRET": "your_app_secret"
      }
    }
  }
}
```

## 📖 使用说明

### Markdown 文章格式要求

每篇 Markdown 文章开头需要添加 frontmatter，提供 `title` 和 `cover` 字段：

```markdown
---
title: 在本地跑一个大语言模型(2) - 给模型提供外部知识库
cover: /Users/lei/Downloads/result_image.jpg
---

在[上一篇文章](https://babyno.top)中，我们展示了如何在本地运行大型语言模型...

![示例图片](https://example.com/image.jpg)
```

**字段说明：**

- `title`：文章标题（必填）
- `cover`：文章封面（支持本地路径和网络图片）
  - 如果正文有至少一张图片，可省略，此时将使用其中一张作为封面
  - 如果正文无图片，则必须提供 cover

### 图片支持

- ✅ 本地路径：`/Users/lei/Downloads/result_image.jpg`
- ✅ 网络路径：`https://example.com/image.jpg`

所有图片会自动上传到微信公众号素材库。

### 主题预览

文颜内置了多个精美主题：

- Orange Heart
- Rainbow
- Lapis
- Pie
- Maize
- Purple
- 物理猫-薄荷

👉 查看主题效果：https://yuzhi.tech/docs/wenyan/themes

## 🎯 工作流程示例

### 使用 AI 助手自动发布

1. 准备好 Markdown 文章（包含 frontmatter）
2. 对 AI 说：
   - "帮我把这篇文章发布到微信公众号"
   - "使用 Rainbow 主题发布这篇文章"
   - "上传这篇文章到公众号草稿箱"

3. AI 会自动：
   - 选择主题
   - 排版文章
   - 上传图片
   - 发布到草稿箱

## 🔍 调试工具

使用 MCP Inspector 进行调试：

```bash
npx @modelcontextprotocol/inspector
```

启动后访问提示的链接，可以测试各个接口功能。

## 📚 API 接口说明

根据微信公众号官方文档，发布流程如下：

### 1. 获取 Access Token

```
GET https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={APPSECRET}
```

### 2. 上传图片素材

```
POST https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={ACCESS_TOKEN}&type=image
```

### 3. 创建草稿

```
POST https://api.weixin.qq.com/cgi-bin/draft/add?access_token={ACCESS_TOKEN}
```

### 4. 发布文章

```
POST https://api.weixin.qq.com/cgi-bin/freepublish/submit?access_token={ACCESS_TOKEN}
```

## ⚠️ 注意事项

1. **access_token 有效期为 2 小时**，需要定期刷新
2. **必须配置 IP 白名单**，否则接口调用会失败
3. **必须是认证后的公众号**才能使用发布功能
4. **有 API 调用频率限制**，注意不要频繁调用
5. 文章内容需要符合微信公众号的内容规范

## 🐛 常见问题

### 1. 上传失败，返回 40164 错误

**原因**：IP 不在白名单中

**解决**：在微信公众号平台添加服务器 IP 到白名单

### 2. 图片上传失败

**原因**：
- 图片路径不正确
- 图片格式不支持（支持 jpg、png）
- 图片大小超限（建议小于 2MB）

### 3. Access Token 失效

**原因**：超过 2 小时有效期

**解决**：工具会自动刷新 token，无需手动处理

## 📦 其他版本

文颜还提供了其他版本：

- **macOS App Store 版** - MAC 桌面应用
- **跨平台版本** - Windows/Linux 桌面应用
- **CLI 版本** - CI/CD 或脚本自动化发布
- **嵌入版本** - 将核心功能嵌入 Node 或 Web 项目

## 📄 License

Apache License Version 2.0

## 🔗 相关链接

- 项目主页：https://github.com/caol64/wenyan-mcp
- 官方文档：https://yuzhi.tech/docs/wenyan/
- 主题预览：https://yuzhi.tech/docs/wenyan/themes

