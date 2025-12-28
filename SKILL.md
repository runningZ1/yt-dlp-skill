---
name: yt-dlp
description: |
  Expert skill for yt-dlp (youtube-dl fork) - a powerful command-line media downloader supporting 1000+ websites.
  Use for: downloading videos/audio from YouTube, Bilibili, Twitch, Twitter, etc; format selection and conversion;
  subtitle downloading and embedding; playlist handling; metadata embedding; cookies/authentication; SponsorBlock integration;
  custom extractor development; understanding yt-dlp codebase architecture.

  Examples: "download YouTube video 4K", "extract audio mp3", "yt-dlp best format", "embed subtitles",
  "Bilibili downloader", "sponsorblock skip ads", "cookies authentication", "write custom extractor",
  "XiaoHongShu download complete package"
category: media-downloader
estimated_tokens: 800
---

# Yt-dlp

<objective>
提供 yt-dlp 项目的专业知识、架构理解和完整工作流指导。yt-dlp 是 youtube-dl 的活跃分支，支持从 1000+ 网站下载视频/音频，具备强大的格式选择、后处理和扩展能力。
</objective>

<when_to_use>
- 场景 1: 从 YouTube、Bilibili、Twitch、Twitter、Instagram 等平台下载视频或音频
- 场景 2: 需要特定格式、质量或进行音视频分离/合并
- 场景 3: 下载字幕、嵌入元数据、使用 SponsorBlock 移除广告片段
- 场景 4: 使用 cookies/认证访问受保护或登录后才能看到的内容
- 场景 5: 处理播放列表、直播流或频道内容
- 场景 6: 理解、修改或扩展 yt-dlp 源代码
- 场景 7: 编写自定义提取器支持新网站
- 场景 8: 集成 yt-dlp 到 Python 项目中

**何时不使用:**
- 下载普通文件（使用 wget/curl）
- 播放视频（使用 mpv/vlc 等播放器）
- 纯视频转码编辑（直接使用 FFmpeg）
- 简单的 YouTube 下载（已有 GUI 工具如 4K Video Downloader）
</when_to_use>

<architecture>
## 架构概览

本 skill 采用 Router Pattern，SKILL.md 作为导航中心，详细内容分布在：

- `workflows/` - 完整工作流（下载、格式选择、开发）
- `references/` - 核心架构、API 文档、最佳实践
- `scripts/` - 实用脚本工具
- `templates/` - 代码模板和配置示例
- `assets/` - 架构图和流程图

```
yt-dlp-skill/
├── SKILL.md (你在这里)
├── workflows/
│   ├── basic-download.md        # 基础下载流程
│   ├── format-selection.md      # 格式选择工作流
│   ├── authentication.md        # 认证处理流程
│   ├── xhs-download.md          # 小红书下载实战案例
│   └── extractor-development.md # 提取器开发指南
├── references/
│   ├── architecture.md          # 核心架构说明
│   ├── format-selector.md       # 格式选择语法
│   ├── postprocessors.md        # 后处理器参考
│   └── extractor-guide.md       # 提取器开发指南
├── scripts/
│   ├── batch-download.py        # 批量下载脚本
│   ├── format-analyzer.py       # 格式分析工具
│   └── cookie-extractor.py      # Cookies 提取工具
├── templates/
│   ├── extractor-template.py    # 提取器模板
│   ├── config-template.conf     # 配置文件模板
│   └── python-api-template.py   # Python API 模板
└── assets/
    └── architecture-diagram.txt # 架构图
```
</architecture>

<quick_start>
## 快速开始

### 基础下载（30秒）

```bash
# 安装
pip install yt-dlp

# 下载视频（最佳质量）
yt-dlp "https://www.youtube.com/watch?v=VIDEO_ID"

# 只下载音频
yt-dlp -x --audio-format mp3 "URL"

# 选择格式
yt-dlp -f "bestvideo[height<=1080]+bestaudio" "URL"
```

### Python API（1分钟）

```python
import yt_dlp

# 下载
ydl_opts = {'outtmpl': '%(title)s.%(ext)s'}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['VIDEO_URL'])

# 只获取信息
ydl_opts = {'quiet': True}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info('URL', download=False)
    print(info['title'])
```
</quick_start>

<workflows>
## 工作流索引

### 使用类工作流
- [基础下载](workflows/basic-download.md) - 从零开始下载第一个视频
- [格式选择](workflows/format-selection.md) - 理解和使用强大的格式选择语法
- [认证处理](workflows/authentication.md) - 处理登录、cookies、API 密钥
- [小红书下载实战](workflows/xhs-download.md) - 小红书视频完整下载案例（含元数据、封面）

### 开发类工作流
- [提取器开发](workflows/extractor-development.md) - 为新网站编写提取器
- [后处理器开发](workflows/postprocessor-development.md) - 扩展后处理功能
- [调试技巧](workflows/debugging.md) - 调试和问题排查

**推荐路径:** 基础下载 → 格式选择 → 认证处理 → 提取器开发
</workflows>

<references>
## 参考文档索引

### 核心概念
- [架构设计](references/architecture.md) - 提取器系统、下载器、后处理器
- [格式选择器](references/format-selector.md) - 完整的格式选择语法和示例
- [后处理器参考](references/postprocessors.md) - 内置后处理器详解

### 开发指南
- [提取器开发指南](references/extractor-guide.md) - 编写自定义提取器
- [API 参考](references/api-reference.md) - Python API 完整文档
- [最佳实践](references/best-practices.md) - 性能优化和安全建议

### 故障排查
- [常见问题](references/troubleshooting.md) - 错误和解决方案
- [已知限制](references/limitations.md) - 平台特定限制
</references>

<tools>
## 脚本工具索引

实用脚本工具（位于 `scripts/`）：

- `batch-download.py` - 从文件批量下载 URL
- `format-analyzer.py` - 分析视频可用格式
- `cookie-extractor.py` - 从浏览器提取 cookies
- `playlist-tools.py` - 播放列表管理工具

运行 `python scripts/<script-name>.py --help` 查看详细用法。
</tools>

<core_concepts>
## 核心概念速览

### 提取器 (Extractors)

每个网站有独立的提取器类，继承自 `InfoExtractor`：

```python
class MySiteIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?mysite\.com/watch/(?P<id>[^/]+)'

    def _real_extract(self, url):
        # 提取视频信息的逻辑
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)
        # ... 返回 info_dict
```

位置：`yt_dlp/extractor/*.py`

### 格式选择 (Format Selection)

强大的格式选择语言：

```bash
# 基础
-f best                 # 最佳质量
-f "bestvideo+bestaudio" # 最佳视频+音频

# 过滤
-f "bestvideo[height<=1080]"  # 不高于 1080p
-f "mp4"                      # 只要 MP4

# 排序
-S "res:1080,fmt:mp4,size"    # 按分辨率、格式、大小排序
```

### 后处理器 (Postprocessors)

链式处理流程：

```python
ydl_opts = {
    'format': 'bestvideo+bestaudio',
    'outtmpl': '%(title)s.%(ext)s',
    'postprocessors': [
        {'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'},
        {'key': 'FFmpegMetadata'},
        {'key': 'EmbedThumbnail'},
    ]
}
```
</core_concepts>

<failure_analysis>
## 已知问题和解决方案

### 问题 1: FFmpeg 相关错误
**症状:** `ffmpeg not found`, `postprocessor` 失败
**解决方案:**
- Windows: 从 https://ffmpeg.org 下载并添加到 PATH
- Linux: `sudo apt install ffmpeg`
- macOS: `brew install ffmpeg`

### 问题 2: 格式合并失败
**症状:** `WARNING: Requested formats are incompatible for merge`
**解决方案:**
```bash
yt-dlp --merge-output-format mp4 "URL"
# 或
yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]" "URL"
```

### 问题 3: Geo-restricted 内容
**解决方案:**
```bash
yt-dlp --proxy socks5://127.0.0.1:1080 "URL"
```

### 问题 4: 登录后才能访问的内容
**解决方案:**
```bash
yt-dlp --cookies-from-browser chrome "URL"
# 或使用 cookies.txt
yt-dlp --cookies cookies.txt "URL"
```

### 问题 5: YouTube 限速
**解决方案:**
```bash
# 使用 aria2 外部下载器
yt-dlp --external-downloader aria2 --external-downloader-args "-x 8 -k 1M" "URL"

# 或限制速率避免被封
yt-dlp --limit-rate 1M "URL"
```
</failure_analysis>

<success_criteria>
成功使用此 skill 的标准:

- [ ] 能够下载各类网站的视频/音频
- [ ] 理解并使用格式选择语法
- [ ] 能够处理字幕、元数据和认证
- [ ] 能够导航和理解 yt-dlp 源代码
- [ ] 能够解决常见下载问题
- [ ] 能够编写简单的自定义提取器
- [ ] 能够在 Python 项目中集成 yt-dlp
</success_criteria>
