# 格式选择器完整参考

## 概述

yt-dlp 的格式选择系统是一个强大的 DSL，允许用户精确控制下载的视频/音频格式。

## 基础语法

### 格式标识符

```bash
# 格式代码
yt-dlp -f 22 "URL"           # 使用格式代码
yt-dlp -f "best" "URL"       # 使用预定义选择器
yt-dlp -f "mp4" "URL"        # 使用容器格式
```

### 组合格式

```bash
# 视频流 + 音频流
-f "bestvideo+bestaudio"

# 多个备选方案（按优先级）
-f "bestvideo[height<=1080]+bestaudio/bestvideo+bestaudio/best"

# 格式说明：
# 首先尝试: bestvideo[height<=1080]+bestaudio
# 如果失败: bestvideo+bestaudio
# 如果还失败: best
```

## 格式选择器

### 预定义选择器

| 选择器 | 说明 |
|--------|------|
| `best` | 最佳质量（已合并或单文件） |
| `worst` | 最差质量 |
| `bestvideo` | 最佳视频流（无音频） |
| `worstvideo` | 最差视频流 |
| `bestaudio` | 最佳音频流（无视频） |
| `worstaudio` | 最差音频流 |
| `videoonly` | 仅视频流 |
| `audioonly` | 仅音频流 |

### 容器格式选择

```bash
-f "mp4"       # 只要 MP4 容器
-f "webm"      # 只要 WebM
-f "mkv"       # 只要 MKV
-f "avi"       # 只要 AVI
```

## 过滤器

### 过滤器语法

```
格式选择键 运算符 值
```

### 过滤键

| 键 | 类型 | 说明 | 示例 |
|----|------|------|------|
| `height` | 数字 | 视频高度（像素） | `height<=1080` |
| `width` | 数字 | 视频宽度 | `width>=1920` |
| `fps` | 数字 | 帧率 | `fps==60` |
| `vbr` | 数字 | 视频比特率 | `vbr>5000k` |
| `abr` | 数字 | 音频比特率 | `abr>=192k` |
| `asr` | 数字 | 音频采样率 | `asr=48000` |
| `filesize` | 数字 | 文件大小（字节） | `filesize<500M` |
| `filesize_approx` | 数字 | 近似文件大小 | `filesize_approx?1G` |
| `duration` | 数字 | 时长（秒） | `duration<=600` |
| `vcodec` | 字符串 | 视频编解码器 | `vcodec=h264` |
| `acodec` | 字符串 | 音频编解码器 | `acodec=aac` |
| `ext` | 字符串 | 容器格式 | `ext=mp4` |
| `protocol` | 字符串 | 协议 | `protocol=http` |
| `source` | 字符串 | 来源 | `source=youtube` |
| `format_id` | 字符串 | 格式 ID | `format_id=137` |
| `lang` | 字符串 | 语言 | `lang=en` |
| `quality` | 数字 | 质量评分 | `quality>=5` |
| `hdr` | 布尔 | HDR | `hdr=yes`, `hdr=no` |

### 运算符

| 运算符 | 说明 | 类型 |
|--------|------|------|
| `=` | 等于 | 所有 |
| `!=` | 不等于 | 所有 |
| `<` | 小于 | 数字 |
| `>` | 大于 | 数字 |
| `<=` | 小于等于 | 数字 |
| `>=` | 大于等于 | 数字 |
| `~=` | 正则匹配 | 字符串 |
| `!~=` | 正则不匹配 | 字符串 |
| `?` | 近似匹配 | 数字/字符串 |
| `*=` | 包含子串 | 字符串 |
| `*!` | 不包含子串 | 字符串 |
| `^=` | 以...开头 | 字符串 |
| `$=` | 以...结尾 | 字符串 |

### 过滤器组合

```bash
# 与关系（多个条件）
-f "bestvideo[height<=1080][fps>=30][ext=mp4]+bestaudio"

# 或关系（使用 / 分隔）
-f "bestvideo[ext=mp4]/bestvideo[ext=webm]/bestvideo"
```

## 排序

### 排序语法

```bash
# 按单个键排序
yt-dlp -S "res" "URL"

# 按多个键排序
yt-dlp -S "res,fps,size" "URL"

# 降序（默认）
yt-dlp -S "res" "URL"      # 分辨率从高到低

# 升序
yt-dlp -S "+res" "URL"     # 分辨率从低到高
```

### 排序键

| 键 | 说明 | 示例 |
|----|------|------|
| `res` | 分辨率 | `S "res:1080"` 优先 1080p |
| `fps` | 帧率 | `S "fps"` 优先高帧率 |
| `size` | 文件大小 | `S "-size"` 优先小文件 |
| `br` | 比特率 | `S "br"` 优先高比特率 |
| `abr` | 音频比特率 | `S "abr"` 优先高音质 |
| `asr` | 音频采样率 | `S "asr"` 优先高采样率 |
| `proto` | 协议优先级 | `S "proto"` https > http |
| `vcodec` | 视频编解码器 | `S "vcodec:vp9"` 优先 VP9 |
| `acodec` | 音频编解码器 | `S "acodec:opus"` 优先 Opus |
| `lang` | 语言 | `S "lang:en"` 优先英语 |
| `quality` | 质量评分 | `S "quality"` 综合质量 |
| `filesize` | 文件大小 | `S "-filesize"` 优先小文件 |
| `filesize_approx` | 近似大小 | `S "-filesize_approx"` |
| `width` | 视频宽度 | `S "width"` 优先更宽 |
| `height` | 视频高度 | `S "height"` 优先更高 |
| `duration` | 时长 | `S "duration"` 优先更长 |

### 排序修饰符

```bash
# 降序（默认）
-S "res"        # 最高分辨率优先

# 升序
-S "+res"       # 最低分辨率优先
-S "-size"      # 最小文件优先

# 目标值（最接近的优先）
-S "res:1080"   # 最接近 1080p 优先
-S "fps:30"     # 最接近 30fps 优先

# 排序多个键（优先级从左到右）
-S "res:1080,fps,size"  # 先最接近1080p，然后高帧率，然后小文件
```

## 组合使用

### 格式选择 + 排序

```bash
# 先过滤，再排序
-f "bestvideo[height<=1080]+bestaudio" -S "size"
```

### 命令行完整示例

```bash
# 场景 1: 1080p 或以下最佳 MP4
-f "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"

# 场景 2: 最高质量但文件最小
-f "bestvideo+bestaudio" -S "+res,-size"

# 场景 3: 720p 60fps
-f "bestvideo[height=720][fps=60]+bestaudio/bestvideo[height=720]+bestaudio"

# 场景 4: 不使用特定编解码器
-f "bestvideo[vcodec!=vp9]+bestaudio/bestvideo+bestaudio"

# 场景 5: 按比特率排序
-f "best" -S "br"

# 场景 6: 使用正则表达式
-f "best[vcodec~='^avc1']+bestaudio/best"
```

## 高级用法

### 格式拼接

```bash
# 尝试多个选择方案
-f "bestvideo[height<=1080]+bestaudio/bestvideo+bestaudio/best"

# 选择器优先级：
# 1. bestvideo[height<=1080]+bestaudio
# 2. bestvideo+bestaudio
# 3. best
```

### 分离流处理

```bash
# 下载视频流和音频流（分离）
-f "bestvideo+bestaudio" --merge-output-format mkv
```

### 格式修改

```bash
# 转换格式
-f "best" --remux-video mp4

# 合并格式
-f "bestvideo+bestaudio" --merge-output-format mp4
```

### 格式信息查看

```bash
# 列出所有格式
yt-dlp -F "URL"

# 打印格式字典
yt-dlp --print "%(formats)s" "URL"

# 打印格式选择结果
yt-dlp -f "bestvideo+bestaudio" --print "%(format)s" "URL"

# 查看格式键
yt-dlp --print "keys" "URL"
```

## Python API

```python
import yt_dlp

# 格式选择
ydl_opts = {
    'format': 'bestvideo[height<=1080]+bestaudio/best',
    'format_sort': ['res', 'fps', 'size'],  # 排序
    'format_sort_force': True,  # 强制排序
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['URL'])

# 只获取格式信息
ydl_opts = {
    'quiet': True,
    'listformats': True,
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info('URL', download=False)
    for fmt in info['formats']:
        print(f"{fmt['format_id']}: {fmt['ext']} {fmt.get('height', 'N/A')}p")
```

## 常见模式

### 模式 1: 兼容性优先

```bash
-f "bestvideo[vcodec~='^avc1'][ext=mp4]+bestaudio[acodec~='^mp4a'][ext=m4a]/bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
```

### 模式 2: 质量优先

```bash
-f "bestvideo+bestaudio" -S "res,fps,br"
```

### 模式 3: 大小优先

```bash
-f "bestvideo+bestaudio" -S "+res,-size"
```

### 模式 4: 特定分辨率

```bash
# 720p 优先
-f "bestvideo+bestaudio" -S "res:720"

# 或使用过滤
-f "bestvideo[height=720]+bestaudio/bestvideo[height<=720]+bestaudio/best"
```

### 模式 5: HDR/SDR 选择

```bash
# 只下载 HDR
-f "bestvideo[hdr=yes]+bestaudio/bestvideo+bestaudio"

# 只下载 SDR
-f "bestvideo[hdr=no]+bestaudio/bestvideo+bestaudio"
```

## 故障排查

### 问题 1: 格式不兼容无法合并

```bash
# 解决方案 1: 指定合并格式
-f "bestvideo+bestaudio" --merge-output-format mp4

# 解决方案 2: 选择兼容格式
-f "bestvideo[ext=mp4]+bestaudio[ext=m4a]"

# 解决方案 3: 使用 remux
-f "bestvideo+bestaudio" --remux-video mp4
```

### 问题 2: 没有符合条件的格式

```bash
# 使用多个备选
-f "bestvideo[height=2160]+bestaudio/bestvideo[height=1080]+bestaudio/best"
```

### 问题 3: 音视频不同步

```bash
# 使用 fixup
--fixup warn_corrupt
```

## 参考资料

- [格式选择工作流](../workflows/format-selection.md)
- [架构参考](architecture.md)
- [最佳实践](best-practices.md)
