# 基础下载工作流

## 目标

从零开始使用 yt-dlp 下载第一个视频/音频文件。

## 前置条件

- [ ] Python 3.8+ 已安装
- [ ] pip 可用
- [ ] 网络连接正常

## 步骤

### 步骤 1: 安装 yt-dlp

```bash
# 使用 pip 安装
pip install yt-dlp

# 或使用 pipx（推荐，隔离环境）
pipx install yt-dlp

# 验证安装
yt-dlp --version
```

### 步骤 2: 基础视频下载

```bash
# 最简单的用法 - 下载最佳质量
yt-dlp "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# 查看下载进度
yt-dlp --newline "URL"

# 指定保存位置
yt-dlp -o "Downloads/%(title)s.%(ext)s" "URL"
```

### 步骤 3: 音频下载

```bash
# 只下载音频（自动提取）
yt-dlp -x "URL"

# 提取为 MP3
yt-dlp -x --audio-format mp3 "URL"

# 指定音频质量 (0=best, 9=worst)
yt-dlp -x --audio-format mp3 --audio-quality 0 "URL"
```

### 步骤 4: 查看可用格式

```bash
# 列出所有可用格式（不下载）
yt-dlp --list-formats "URL"

# 输出格式表格
yt-dlp -F "URL"
```

输出示例：
```
format code  extension  resolution note
140          m4a        audio only  DASH audio 128k
137          mp4        1920x1080   DASH video 1920k
22           mp4        1280x720    medium
18           mp4        640x360     medium
```

### 步骤 5: 选择特定格式

```bash
# 下载最佳质量（但不超过 1080p）
yt-dlp -f "bestvideo[height<=1080]+bestaudio" "URL"

# 下载 720p MP4
yt-dlp -f "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]" "URL"

# 下载预设格式（如 22）
yt-dlp -f 22 "URL"
```

## 常用选项

### 输出文件名模板

```bash
# 基础模板
yt-dlp -o "%(title)s.%(ext)s" "URL"

# 包含更多信息
yt-dlp -o "%(uploader)s/%(upload_date)s - %(title)s.%(ext)s" "URL"

# 可用变量: id, title, uploader, upload_date, duration, view_count, like_count 等
# 查看完整列表: yt-dlp --print output
```

### 播放列表

```bash
# 下载整个播放列表
yt-dlp "PLAYLIST_URL"

# 只下载特定视频（从 1 开始）
yt-dlp --playlist-items 1-5,10 "PLAYLIST_URL"

# 逆序下载
yt-dlp --playlist-reverse "PLAYLIST_URL"

# 不下载播放列表，只下载单个视频
yt-dlp --no-playlist "VIDEO_IN_PLAYLIST_URL"
```

### 字幕

```bash
# 下载所有可用字幕
yt-dlp --write-subs --all-subs "URL"

# 下载自动生成的字幕
yt-dlp --write-auto-subs "URL"

# 嵌入字幕到视频
yt-dlp --embed-subs --sub-lang en "URL"
```

### 元数据和缩略图

```bash
# 嵌入元数据（标题、描述等）
yt-dlp --embed-metadata "URL"

# 下载并嵌入缩略图
yt-dlp --write-thumbnail --embed-thumbnail "URL"

# 一起使用
yt-dlp --embed-metadata --write-thumbnail --embed-thumbnail "URL"
```

## 故障排查

### 问题: 下载速度慢

```bash
# 使用外部下载器（需要安装 aria2）
yt-dlp --external-downloader aria2 --external-downloader-args "-x 8 -k 1M" "URL"

# 限制下载速率
yt-dlp --limit-rate 1M "URL"
```

### 问题: 需要登录

```bash
# 从浏览器导入 cookies
yt-dlp --cookies-from-browser chrome "URL"

# 或使用 cookies.txt 文件
yt-dlp --cookies cookies.txt "URL"
```

### 问题: FFmpeg 错误

```bash
# 检查 FFmpeg 是否安装
ffmpeg -version

# 如果未安装，参考:
# Windows: https://ffmpeg.org/download.html
# Linux: sudo apt install ffmpeg
# macOS: brew install ffmpeg
```

## 下一步

- [格式选择工作流](format-selection.md) - 学习强大的格式选择语法
- [认证处理工作流](authentication.md) - 处理登录和认证
- [Python API 参考](../references/api-reference.md) - 在代码中使用 yt-dlp
