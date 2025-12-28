# yt-dlp-skill

<div align="center">

**Claude Code 专用的 yt-dlp 技能包**

[English Version](#english-version) | [中文文档](#中文文档)

</div>

---

## 中文文档

> yt-dlp 是 youtube-dl 的活跃分支，支持从 1000+ 网站下载视频/音频，具备强大的格式选择、后处理和扩展能力。

### 功能特性

- 🎬 **多平台支持** - YouTube、Bilibili、小红书、Twitch、Twitter、Instagram 等 1000+ 网站
- 🎯 **格式选择** - 强大的格式选择语法，精确控制下载质量
- 📝 **元数据提取** - 完整的视频信息、标签、封面、描述
- 🍪 **认证支持** - Cookies 处理，登录后内容下载
- 🔧 **可扩展** - 自定义提取器和后处理器开发
- 🐍 **Python API** - 完整的 Python 集成支持

### 快速开始

```bash
# 安装 yt-dlp
pip install yt-dlp

# 基础下载
yt-dlp "视频URL"

# 下载完整资源包（推荐）
yt-dlp -o "输出目录/%(title)s/%(title)s.%(ext)s" \
  --write-info-json \
  --write-description \
  --write-thumbnail \
  --convert-thumbnails jpg \
  "视频URL"
```

### 技能包结构

```
yt-dlp-skill/
├── SKILL.md           # 技能包主入口
├── workflows/         # 完整工作流文档
│   ├── basic-download.md      # 基础下载
│   ├── format-selection.md    # 格式选择
│   ├── authentication.md      # 认证处理
│   └── xhs-download.md        # 小红书实战案例
├── references/        # 参考文档
│   ├── architecture.md        # 架构设计
│   ├── format-selector.md     # 格式选择器
│   └── api-reference.md       # API 文档
├── scripts/           # 实用脚本
└── templates/         # 代码模板
```

### 小红书下载实战案例

本技能包包含完整的小红书视频下载方案，可下载：
- 视频文件
- 完整元数据（JSON）
- 视频封面图
- 视频描述文本

**输出结构：**
```
如何用AI轻松写出任意提示词？\
├── 如何用AI轻松写出任意提示词？.mov      # 视频
├── 如何用AI轻松写出任意提示词？.jpg       # 封面
├── 如何用AI轻松写出任意提示词？.info.json # 元数据
└── 如何用AI轻松写出任意提示词？.description # 描述
```

### 安装到 Claude Code

```bash
# 克隆到 skills 目录
git clone https://github.com/runningZ1/yt-dlp-skill.git \
  ~/.claude/skills/yt-dlp-skill

# Windows
git clone https://github.com/runningZ1/yt-dlp-skill.git \
  %USERPROFILE%\.claude\skills\yt-dlp-skill
```

### 使用场景

| 场景 | 命令 |
|------|------|
| 下载视频 | `yt-dlp "URL"` |
| 完整资源包 | 添加 `--write-info-json --write-description --write-thumbnail` |
| 只下载音频 | `yt-dlp -x --audio-format mp3 "URL"` |
| 选择格式 | `yt-dlp -f "bestvideo[height<=1080]+bestaudio" "URL"` |

### 常见问题

**Q: 下载速度慢？**
```bash
yt-dlp --external-downloader aria2 --external-downloader-args "-x 8 -k 1M" "URL"
```

**Q: 需要登录？**
```bash
yt-dlp --cookies-from-browser chrome "URL"
```

**Q: FFmpeg 相关错误？**
- Windows: 从 https://ffmpeg.org 下载并添加到 PATH
- Linux: `sudo apt install ffmpeg`
- macOS: `brew install ffmpeg`

### 贡献

欢迎提交 Issue 和 Pull Request！

### 许可证

本项目采用 [MIT License](LICENSE) 开源协议。

---

<a name="english-version"></a>

## English Version

> Expert skill package for yt-dlp (youtube-dl fork) - supporting 1000+ websites for video/audio downloading with powerful format selection and post-processing capabilities.

### Features

- 🎬 **Multi-platform Support** - YouTube, Bilibili, XiaoHongShu, Twitch, Twitter, Instagram and 1000+ sites
- 🎯 **Format Selection** - Powerful format selection syntax for precise quality control
- 📝 **Metadata Extraction** - Complete video info, tags, thumbnails, descriptions
- 🍪 **Authentication** - Cookie handling for logged-in content
- 🔧 **Extensible** - Custom extractors and postprocessors
- 🐍 **Python API** - Full Python integration support

### Quick Start

```bash
# Install yt-dlp
pip install yt-dlp

# Basic download
yt-dlp "VIDEO_URL"

# Download complete package (recommended)
yt-dlp -o "output/%(title)s/%(title)s.%(ext)s" \
  --write-info-json \
  --write-description \
  --write-thumbnail \
  --convert-thumbnails jpg \
  "VIDEO_URL"
```

### Skill Package Structure

```
yt-dlp-skill/
├── SKILL.md           # Main skill entry point
├── workflows/         # Complete workflow documentation
│   ├── basic-download.md      # Basic downloading
│   ├── format-selection.md    # Format selection
│   ├── authentication.md      # Authentication handling
│   └── xhs-download.md        # XiaoHongShu case study
├── references/        # Reference documentation
│   ├── architecture.md        # Architecture design
│   ├── format-selector.md     # Format selector
│   └── api-reference.md       # API documentation
├── scripts/           # Utility scripts
└── templates/         # Code templates
```

### XiaoHongShu Download Case Study

This skill includes a complete solution for downloading XiaoHongShu videos with:
- Video file
- Complete metadata (JSON)
- Video thumbnail
- Video description

**Output Structure:**
```
How to Write AI Prompts Easily\
├── How to Write AI Prompts Easily.mov      # Video
├── How to Write AI Prompts Easily.jpg       # Thumbnail
├── How to Write AI Prompts Easily.info.json # Metadata
└── How to Write AI Prompts Easily.description # Description
```

### Install to Claude Code

```bash
# Clone to skills directory
git clone https://github.com/runningZ1/yt-dlp-skill.git \
  ~/.claude/skills/yt-dlp-skill

# Windows
git clone https://github.com/runningZ1/yt-dlp-skill.git \
  %USERPROFILE%\.claude\skills\yt-dlp-skill
```

### Use Cases

| Scenario | Command |
|----------|---------|
| Download video | `yt-dlp "URL"` |
| Complete package | Add `--write-info-json --write-description --write-thumbnail` |
| Audio only | `yt-dlp -x --audio-format mp3 "URL"` |
| Select format | `yt-dlp -f "bestvideo[height<=1080]+bestaudio" "URL"` |

### FAQ

**Q: Slow download speed?**
```bash
yt-dlp --external-downloader aria2 --external-downloader-args "-x 8 -k 1M" "URL"
```

**Q: Need to login?**
```bash
yt-dlp --cookies-from-browser chrome "URL"
```

**Q: FFmpeg related errors?**
- Windows: Download from https://ffmpeg.org and add to PATH
- Linux: `sudo apt install ffmpeg`
- macOS: `brew install ffmpeg`

### Contributing

Issues and Pull Requests are welcome!

### License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

**Made with ❤️ for Claude Code users**

</div>
