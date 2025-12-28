# 格式选择工作流

## 目标

掌握 yt-dlp 强大的格式选择语法，精确控制下载的视频/音频质量、格式和大小。

## 前置条件

- [ ] 已完成 [基础下载工作流](basic-download.md)
- [ ] 了解基础命令行操作

## 步骤

### 步骤 1: 理解格式结构

视频通常有两种流：

```
视频流 (video only): 137, 299, 303 等
音频流 (audio only): 140, 251 等
已合并流 (video+audio): 22, 18 等
```

```bash
# 查看所有格式
yt-dlp -F "URL"
```

### 步骤 2: 基础格式选择

```bash
# 最佳质量（自动合并视频和音频）
yt-dlp -f "bestvideo+bestaudio" "URL"

# 最差质量
yt-dlp -f "worst" "URL"

# 最佳但不超过 1080p
yt-dlp -f "bestvideo[height<=1080]+bestaudio" "URL"

# 只要 MP4 格式
yt-dlp -f "mp4" "URL"

# 只要视频，不要音频
yt-dlp -f "bestvideo" "URL"
```

### 步骤 3: 使用过滤器

格式过滤器语法：`格式选择键+过滤条件`

**可用过滤键:**

| 过滤键 | 说明 | 示例 |
|--------|------|------|
| `height` | 视频高度 | `height<=1080` |
| `width` | 视频宽度 | `width>=1920` |
| `fps` | 帧率 | `fps==60` |
| `filesize` | 文件大小（字节） | `filesize<500M` |
| `filesize_approx` | 近似文件大小 | `filesize_approx?1G` |
| `duration` | 时长（秒） | `duration<=600` |
| `vcodec` | 视频编解码器 | `vcodec!=vp9` |
| `acodec` | 音频编解码器 | `acodec=aac` |
| `vbr` | 视频比特率 | `vbr>5000k` |
| `abr` | 音频比特率 | `abr>=192k` |
| `ext` | 容器格式 | `ext=mp4` |
| `protocol` | 协议 | `protocol=http` |
| `source` | 来源 | `source=youtube` |

**运算符:**

| 运算符 | 说明 |
|--------|------|
| `=` | 等于 |
| `!=` | 不等于 |
| `<` `>` `<=` `>=` | 比较 |
| `~=` | 正则匹配 |
| `!~=` | 正则不匹配 |
| `?` | 近似匹配 |
| `*=` | 包含 |
| `*!` | 不包含 |

**示例:**

```bash
# 不高于 1080p
-f "bestvideo[height<=1080]+bestaudio"

# 至少 60fps
-f "bestvideo[fps>=60]+bestaudio"

# MP4 容器
-f "bestvideo[ext=mp4]+bestaudio[ext=m4a]"

# 不使用 vp9 编码
-f "bestvideo[vcodec!=vp9]+bestaudio"

# 文件大小小于 500MB
-f "bestvideo[filesize<500M]+bestaudio"

# 时长 5-10 分钟
-f "bestvideo[duration<=600][duration>=300]+bestaudio"
```

### 步骤 4: 格式排序

使用 `-S` 按优先级排序格式：

```bash
# 按分辨率排序（1080p 优先）
yt-dlp -S "res:1080" "URL"

# 按分辨率、格式、大小排序
yt-dlp -S "res:1080,fmt:mp4,size" "URL"

# 最佳质量但文件最小
yt-dlp -S "+res,-size" "URL"

# 排序键说明:
# res: 分辨率
# fps: 帧率
# size: 文件大小
# br: 比特率
# asr: 音频采样率
# proto: 协议优先级 (https > http)
# vcodec: 视频编解码器
# acodec: 音频编解码器
# lang: 语言
# quality: 质量评分
# +key: 降序（越大越优先）
# -key: 升序（越小越优先）
```

### 步骤 5: 高级格式选择

#### 格式拼接

```bash
# 尝试多个格式选择，按顺序
yt-dlp -f "bestvideo[height<=1080]+bestaudio/bestvideo+bestaudio/best" "URL"

# 格式说明:
# 首先尝试: bestvideo[height<=1080]+bestaudio
# 如果失败: bestvideo+bestaudio
# 如果还失败: best
```

#### 分离视频和音频

```bash
# 下载最佳视频流和最佳音频流
yt-dlp -f "bestvideo+bestaudio" "URL"

# 指定视频和音频格式
yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best" "URL"
```

#### 合并输出格式

```bash
# 合并为特定容器格式
yt-dlp -f "bestvideo+bestaudio" --merge-output-format mp4 "URL"

# 常用合并格式: mp4, mkv, webm, avi
```

### 步骤 6: 实用组合

```bash
# 场景 1: 下载 1080p 或以下最佳 MP4 视频
yt-dlp -f "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" "URL"

# 场景 2: 下载最高质量但文件小于 1GB
yt-dlp -f "bestvideo[filesize<1G]+bestaudio/best" "URL"

# 场景 3: 下载 720p 60fps 视频
yt-dlp -f "bestvideo[height=720][fps=60]+bestaudio" "URL"

# 场景 4: 下载最佳音质（用于音乐）
yt-dlp -f "bestaudio" --extract-audio --audio-format mp3 "URL"

# 场景 5: 下载 4K 视频但保留 HDR
yt-dlp -f "bestvideo[height>=2160]+bestaudio" "URL"

# 场景 6: 下载 SDR 版本（无 HDR）
yt-dlp -f "bestvideo[hdr=no]+bestaudio" "URL"
```

### 步骤 7: 打印而不下载

```bash
# 打印选中的格式
yt-dlp -f "bestvideo+bestaudio" --print "%(format)s" "URL"

# 打印所有格式信息
yt-dlp --list-formats "URL"

# 打印格式 ID
yt-dlp --print "%(id)s - %(format)s - %(ext)s" "URL"
```

## 格式选择最佳实践

### 规则 1: 兼容性优先

```bash
# 大多数设备兼容
-f "bestvideo[ext=mp4][height<=1080]+bestaudio[ext=m4a]/best[ext=mp4]/best"
```

### 规则 2: 质量与大小平衡

```bash
# 1080p 优先，如果太大则降级
-f "bestvideo[height<=1080][filesize<500M]+bestaudio/bestvideo[height<=720]+bestaudio"
```

### 规则 3: 编解码器选择

```bash
# 优先选择 H.264 而非 VP9（更好的兼容性）
-f "bestvideo[vcodec~='^avc1']+bestaudio/bestvideo+bestaudio"

# 优先选择 VP9 而非 H.264（更好的压缩）
-f "bestvideo[vcodec~='^vp9']+bestaudio/bestvideo+bestaudio"
```

## 常见问题

### 问题 1: 格式不兼容无法合并

```bash
# 错误: Requested formats are incompatible for merge

# 解决方案 1: 指定合并格式
yt-dlp -f "bestvideo+bestaudio" --merge-output-format mp4 "URL"

# 解决方案 2: 选择兼容格式
yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]" "URL"

# 解决方案 3: 使用 remux
yt-dlp -f "bestvideo+bestaudio" --remux-video mp4 "URL"
```

### 问题 2: 找不到符合条件的格式

```bash
# 使用多个备选方案
-f "bestvideo[height=2160]+bestaudio/bestvideo[height=1080]+bestaudio/best"
```

### 问题 3: 音视频不同步

```bash
# 使用 --fixup 参数
yt-dlp --fixup warn_corrupt --merge-output-format mp4 "URL"
```

## 下一步

- [认证处理工作流](authentication.md) - 处理登录后才能访问的内容
- [格式选择器参考](../references/format-selector.md) - 完整语法文档
- [最佳实践](../references/best-practices.md) - 性能优化建议
