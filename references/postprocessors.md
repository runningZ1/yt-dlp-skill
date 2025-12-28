# 后处理器完整参考

## 概述

后处理器在视频下载后对文件进行处理，包括格式转换、元数据嵌入、字幕处理等。

## 内置后处理器

### FFmpegVideoConvertor

视频格式转换后处理器。

```python
{
    'key': 'FFmpegVideoConvertor',
    'preferedformat': 'mp4',  # 目标格式
}
```

**支持的格式:** mp4, mkv, webm, avi, flv, mov

**示例:**
```bash
yt-dlp --merge-output-format mp4 "URL"
```

### FFmpegExtractAudio

音频提取后处理器。

```python
{
    'key': 'FFmpegExtractAudio',
    'preferredcodec': 'mp3',     # 目标音频格式
    'preferredquality': '0',      # 质量 (0=best, 9=worst)
    'nopostoverwrites': False,    # 不覆盖已存在文件
}
```

**支持的格式:** mp3, aac, flac, m4a, opus, vorbis, wav

**质量说明:**
- `0`: 最佳质量（比特率）
- `1-9`: 越低质量越差
- 对于某些格式，可以是具体比特率如 `320K`

**示例:**
```bash
# 提取 MP3，最佳质量
yt-dlp -x --audio-format mp3 --audio-quality 0 "URL"

# 提取 AAC
yt-dlp -x --audio-format aac "URL"

# 提取 FLAC（无损）
yt-dlp -x --audio-format flac "URL"
```

### FFmpegMetadata

元数据嵌入后处理器。

```python
{
    'key': 'FFmpegMetadata',
    'add_metadata': True,        # 添加元数据
    'add_chapters': True,        # 添加章节
}
```

**嵌入的元数据:**
- title
- artist (uploader)
- album
- date (upload_date)
- description
- comment
- track

**示例:**
```bash
yt-dlp --embed-metadata "URL"
```

### FFmpegEmbedSubtitle

字幕嵌入后处理器。

```python
{
    'key': 'FFmpegEmbedSubtitle',
    'subtitlesformat': 'srt',    # 字幕格式
}
```

**支持的格式:** srt, ass, vtt

**限制:** 只能嵌入到 MP4/MKV/WEBM 容器

**示例:**
```bash
# 下载并嵌入字幕
yt-dlp --embed-subs --sub-lang en "URL"

# 下载所有字幕并嵌入
yt-dlp --embed-subs --all-subs "URL"
```

### FFmpegFixupStretched

修复拉伸/压缩视频。

```python
{
    'key': 'FFmpegFixupStretched',
}
```

### FFmpegFixupM4a

修复 M4A 格式问题。

```python
{
    'key': 'FFmpegFixupM4a',
}
```

### FFmpegFixupM3u8

修复 M3U8 下载问题。

```python
{
    'key': 'FFmpegFixupM3u8',
}
```

### EmbedThumbnail

缩略图嵌入后处理器。

```python
{
    'key': 'EmbedThumbnail',
    'already_have_thumbnail': False,  # 已下载缩略图
}
```

**示例:**
```bash
# 下载并嵌入缩略图
yt-dlp --write-thumbnail --embed-thumbnail "URL"
```

### MetadataFromField

从字段提取元数据。

```python
{
    'key': 'MetadataFromField',
    'formats': [
        {
            'fromtitle': '%(title)s - %(uploader)s',
            'to': 'comment',
        },
    ],
}
```

### SponsorBlock

SponsorBlock 集成，移除赞助片段。

```python
{
    'key': 'SponsorBlock',
    'categories': [
        'sponsor',      # 赞助
        'intro',        # 开场
        'outro',        # 结尾
        'selfpromo',    # 自我宣传
        'preview',      # 预告
        'filler',       # 填充内容
        'interaction',  # 互动提醒
        'music_offtopic',  # 非音乐部分
    ],
    'api': 'https://sponsor.ajay.app',
}
```

**示例:**
```bash
# 移除赞助和开场
yt-dlp --sponsorblock-remove sponsor,intro "URL"

# 移除所有类型
yt-dlp --sponsorblock-remove all "URL"
```

### XAttrMetadata

设置扩展属性（文件元数据）。

```python
{
    'key': 'XAttrMetadata',
}
```

**示例:**
```bash
yt-dlp --xattrs "URL"
```

### FFmpegConcat

连接多个视频。

```python
{
    'key': 'FFmpegConcat',
    'only_video': True,
}
```

### FFmpegSplitVideo

分割视频。

```python
{
    'key': 'FFmpegSplitVideo',
    'parts': 2,  # 分割成几部分
}
```

## 后处理器链

后处理器按配置顺序执行：

```python
ydl_opts = {
    'postprocessors': [
        # 1. 转换视频格式
        {'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'},

        # 2. 提取音频
        {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'},

        # 3. 嵌入元数据
        {'key': 'FFmpegMetadata'},

        # 4. 嵌入字幕
        {'key': 'FFmpegEmbedSubtitle'},

        # 5. 嵌入缩略图
        {'key': 'EmbedThumbnail'},
    ]
}
```

## 命令行选项

### 视频/音频转换

```bash
# 合并为特定格式
--merge-output-format mp4

# 转换视频
--remux-video mp4

# 提取音频
-x, --extract-audio
--audio-format mp3
--audio-quality 0
```

### 元数据

```bash
# 嵌入元数据
--embed-metadata

# 从字段提取
--parse-metadata "%(title)s:%(meta_title)s"
```

### 字幕

```bash
# 嵌入字幕
--embed-subs

# 字幕格式
--sub-format srt
```

### 缩略图

```bash
# 写入缩略图
--write-thumbnail

# 嵌入缩略图
--embed-thumbnail

# 转换缩略图格式
--convert-thumbnails jpg
```

### SponsorBlock

```bash
--sponsorblock-remove sponsor,intro,outro

# 或使用 --sponsorblock-chapters
--sponsorblock-chapters
```

### 其他

```bash
--xattrs              # 设置扩展属性
--fixup policy        # 修复策略 (never, warn, detect_or_warn)
--concat-playlist     # 连接播放列表
```

## Python API

### 使用内置后处理器

```python
import yt_dlp

ydl_opts = {
    'outtmpl': '%(title)s.%(ext)s',
    'postprocessors': [
        {
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        },
        {
            'key': 'FFmpegMetadata',
        },
        {
            'key': 'EmbedThumbnail',
        },
    ],
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['URL'])
```

### 添加自定义后处理器

```python
import yt_dlp
from yt_dlp.postprocessor import PostProcessor

class MyPP(PostProcessor):
    def run(self, info):
        filepath = info['filepath']
        self.to_screen(f'Processing {filepath}')
        # 处理逻辑...
        return [info], []

with yt_dlp.YoutubeDL({'outtmpl': '%(title)s.%(ext)s'}) as ydl:
    ydl.add_post_processor(MyPP(ydl))
    ydl.download(['URL'])
```

### 后处理器参数

```python
ydl_opts = {
    'postprocessor_args': {
        'FFmpegVideoConvertor': ['-c:v', 'libx264', '-crf', '23'],
        'FFmpegExtractAudio': ['-b:a', '320k'],
        'ffmpeg': ['-threads', '4'],
    }
}
```

## 常见组合

### 组合 1: 视频 + 元数据 + 缩略图

```python
ydl_opts = {
    'format': 'bestvideo+bestaudio',
    'merge_output_format': 'mp4',
    'postprocessors': [
        {'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'},
        {'key': 'FFmpegMetadata'},
        {'key': 'EmbedThumbnail'},
    ],
    'writethumbnail': True,
}
```

### 组合 2: 音频提取 + 元数据

```python
ydl_opts = {
    'format': 'bestaudio',
    'postprocessors': [
        {
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '0',
        },
        {'key': 'FFmpegMetadata'},
    ],
}
```

### 组合 3: SponsorBlock + 字幕

```python
ydl_opts = {
    'format': 'bestvideo+bestaudio',
    'merge_output_format': 'mp4',
    'postprocessors': [
        {
            'key': 'SponsorBlock',
            'categories': ['sponsor', 'intro', 'outro'],
        },
        {'key': 'FFmpegEmbedSubtitle'},
        {'key': 'FFmpegMetadata'},
    ],
    'writesubtitles': True,
    'subtitleslangs': ['en'],
}
```

## 故障排查

### 问题 1: FFmpeg 未找到

```bash
# 错误: ffmpeg not found
# 解决: 安装 FFmpeg
# Windows: 从 https://ffmpeg.org 下载
# Linux: sudo apt install ffmpeg
# macOS: brew install ffmpeg
```

### 问题 2: 格式不兼容

```bash
# 错误: Requested formats are incompatible
# 解决: 使用 --merge-output-format 或选择兼容格式
yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]" "URL"
```

### 问题 3: 字幕嵌入失败

```bash
# 错误: Cannot embed subtitles
# 解决: 确保容器格式支持嵌入
yt-dlp --embed-subs --merge-output-format mkv "URL"
```

### 问题 4: 元数据编码问题

```bash
# 解决: 指定编码
--metadata-from-title "%(title)s" --encoding utf-8
```

## 参考资料

- [后处理器开发工作流](../workflows/postprocessor-development.md)
- [架构参考](architecture.md)
- [Python API 参考](api-reference.md)
