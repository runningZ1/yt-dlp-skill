# 认证处理工作流

## 目标

处理需要登录、cookies、API 密钥或其他认证才能访问的内容。

## 前置条件

- [ ] 已完成 [基础下载工作流](basic-download.md)
- [ ] 了解基础命令行操作

## 步骤

### 步骤 1: 从浏览器导入 Cookies（最简单）

```bash
# 从 Chrome 导入 cookies
yt-dlp --cookies-from-browser chrome "URL"

# 从 Firefox 导入
yt-dlp --cookies-from-browser firefox "URL"

# 从 Edge 导入
yt-dlp --cookies-from-browser edge "URL"

# 从 Brave 导入
yt-dlp --cookies-from-browser brave "URL"

# 从 Opera 导入
yt-dlp --cookies-from-browser opera "URL"

# 从 Chromium 导入（需指定配置文件路径）
yt-dlp --cookies-from-browser chrome:"C:\Users\User\AppData\Local\Google\Chrome\User Data" "URL"

# 从特定配置文件导入
yt-dlp --cookies-from-browser chrome:Profile 1 "URL"
```

**注意事项:**
- 浏览器需要关闭才能正常读取 cookies
- 某些网站可能检测到自动化访问并拒绝 cookies

### 步骤 2: 使用 Cookies 文件

```bash
# 使用 cookies.txt 文件
yt-dlp --cookies cookies.txt "URL"

# 使用 Netscape 格式
yt-dlp --cookies cookies.txt "URL"
```

**创建 cookies.txt 的方法:**

1. 使用浏览器扩展（推荐）：
   - 安装 "Get cookies.txt" 扩展
   - 访问目标网站并登录
   - 点击扩展图标导出 cookies.txt

2. 使用浏览器开发者工具：
   ```bash
   # 手动创建 cookies.txt（Netscape 格式）
   # 格式: domain \t flag \t path \t secure \t expiration \t name \t value
   .youtube.com\tTRUE\t/\tFALSE\t1735689600\tSAPISID\t<your_value>
   ```

### 步骤 3: 用户名和密码认证

```bash
# 基础用户名密码
yt-dlp -u USERNAME -p PASSWORD "URL"

# 密码会被提示输入（不在命令行显示）
yt-dlp -u USERNAME --video-password PASSWORD "URL"

# 使用环境变量（更安全）
export YTDLP_USERNAME="username"
export YTDLP_PASSWORD="password"
yt-dlp "URL"
```

### 步骤 4: Two-Factor Authentication (2FA)

```bash
# 某些提取器支持 2FA 令牌
yt-dlp -u USERNAME -p PASSWORD --twofactor TOTP_CODE "URL"
```

### 步骤 5: API 密钥认证

#### YouTube API 密钥

```bash
# 使用 YouTube API
yt-dlp --ap-mso "电视提供商" --ap-username "用户名" --ap-password "密码" "URL"

# 示例: 美国电视提供商认证
yt-dlp --ap-mso comcast --ap-username user@example.com --ap-password pass123 "URL"
```

#### Crunchyroll API

```bash
# 使用 Crunchyroll OAuth
yt-dlp --username USERNAME --password PASSWORD "URL"
```

#### Netflix (需要高级配置)

```bash
# Netflix 需要 cookies 和特定的用户代理
yt-dlp --cookies cookies.txt --user-agent "Mozilla/5.0..." "URL"
```

### 步骤 6: 自定义请求头

```bash
# 添加自定义请求头
yt-dlp --add-header "Authorization: Bearer TOKEN" "URL"

# 多个请求头
yt-dlp --add-header "Referer: https://example.com" --add-header "User-Agent: CustomUA" "URL"

# 从文件读取请求头
yt-dlp --headers headers.txt "URL"
```

**headers.txt 格式:**
```
Authorization: Bearer TOKEN
User-Agent: Custom User Agent
Referer: https://example.com
```

### 步骤 7: 代理设置

```bash
# HTTP 代理
yt-dlp --proxy http://127.0.0.1:8080 "URL"

# SOCKS5 代理
yt-dlp --proxy socks5://127.0.0.1:1080 "URL"

# 带认证的代理
yt-dlp --proxy http://user:pass@proxy.example.com:8080 "URL"

# 使用环境变量
export HTTP_PROXY=http://127.0.0.1:8080
export HTTPS_PROXY=http://127.0.0.1:8080
yt-dlp "URL"
```

### 步骤 8: 配置文件认证

创建配置文件 `yt-dlp.conf` 或 `yt-dlp.conf.txt`：

```ini
# Windows: %APPDATA%\yt-dlp\yt-dlp.conf
# Linux/macOS: ~/.config/yt-dlp/yt-dlp.conf

# Cookies
--cookies-from-browser chrome

# 用户名密码
# -u username
# -p password

# 代理
# --proxy socks5://127.0.0.1:1080

# 输出目录
# -o ~/Downloads/%(title)s.%(ext)s
```

### 步骤 9: Python API 认证

```python
import yt_dlp

# 使用 cookies
ydl_opts = {
    'cookiefile': 'cookies.txt',
}

# 使用 cookies 从浏览器
ydl_opts = {
    'cookiesfrombrowser': ('chrome',),
}

# 使用用户名密码
ydl_opts = {
    'username': 'USERNAME',
    'password': 'PASSWORD',
}

# 使用代理
ydl_opts = {
    'proxy': 'http://127.0.0.1:8080',
}

# 使用请求头
ydl_opts = {
    'http_headers': {
        'Authorization': 'Bearer TOKEN',
        'User-Agent': 'CustomUA',
    }
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['URL'])
```

## 平台特定认证

### YouTube

```bash
# 登录后的内容
yt-dlp --cookies-from-browser chrome "URL"

# YouTube Premium 内容
yt-dlp --cookies-from-browser chrome --proxy socks5://127.0.0.1:1080 "URL"
```

### Bilibili

```bash
# 需要 cookies 和 possibly CNProxy
yt-dlp --cookies cookies.txt "URL"

# Bilibili 通常需要特定请求头
yt-dlp --add-header "Referer: https://www.bilibili.com" "URL"
```

### Twitch

```bash
# 使用 OAuth 令牌
yt-dlp --oauth-token YOUR_OAUTH_TOKEN "URL"

# 从 cookies
yt-dlp --cookies-from-browser chrome "URL"
```

### Twitter/X

```bash
# Twitter 需要 cookies 和特定的用户代理
yt-dlp --cookies-from-browser chrome --user-agent "Mozilla/5.0..." "URL"
```

### Instagram

```bash
# Instagram 需要 cookies 和登录状态
yt-dlp --cookies-from-browser chrome --username USERNAME --password PASSWORD "URL"
```

### Netflix

```bash
# Netflix 需要 cookies + 宽 DRM 支持
yt-dlp --cookies cookies.txt "URL"

# 注意: DRM 内容可能无法下载
```

### Crunchyroll

```bash
# Crunchyroll 需要 OAuth 认证
yt-dlp --username EMAIL --password PASSWORD "URL"
```

## 常见问题

### 问题 1: Cookies 过期

```bash
# 重新从浏览器导入
yt-dlp --cookies-from-browser chrome "URL"

# 或使用 cookie 导出工具重新导出
```

### 问题 2: 认证后仍然无法访问

```bash
# 尝试添加请求头
yt-dlp --cookies-from-browser chrome --add-header "Referer: https://example.com" "URL"

# 尝试更改 User-Agent
yt-dlp --user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" "URL"

# 使用代理
yt-dlp --proxy socks5://127.0.0.1:1080 "URL"
```

### 问题 3: 两步验证 (2FA)

```bash
# 如果提取器支持 2FA
yt-dlp --twofactor CODE -u USERNAME -p PASSWORD "URL"

# 否则使用 cookies
yt-dlp --cookies-from-browser chrome "URL"
```

### 问题 4: IP 被封

```bash
# 使用代理更换 IP
yt-dlp --proxy socks5://127.0.0.1:1080 "URL"

# 或限制请求速率
yt-dlp --limit-rate 1M "URL"
```

## 安全最佳实践

### 规则 1: 不要在命令行暴露密码

```bash
# 错误: 密码会出现在 shell 历史中
yt-dlp -u user -p mypassword123 "URL"

# 正确: 使用配置文件或环境变量
export YTDLP_PASSWORD="mypassword123"
yt-dlp -u user "URL"
```

### 规则 2: 不要在代码中硬编码凭据

```python
# 错误
password = "mypassword123"

# 正确
import os
password = os.getenv('YTDLP_PASSWORD')
```

### 规则 3: 使用配置文件存储凭据

```ini
# yt-dlp.conf
--username username
--password password
# 注意: 配置文件权限设置正确
```

### 规则 4: Cookies 文件安全

```bash
# 设置 cookies.txt 文件权限
chmod 600 cookies.txt  # Linux/macOS
```

## 下一步

- [提取器开发工作流](extractor-development.md) - 为需要认证的网站编写提取器
- [故障排查](../references/troubleshooting.md) - 常见认证错误
- [最佳实践](../references/best-practices.md) - 安全和性能建议
