# 小红书(XiaoHongShu) 下载实战案例

## 案例背景

小红书是中国流行的社交电商平台，用户分享短视频和图文内容。yt-dlp 内置了小红书提取器，可以直接下载视频及相关元数据。

**测试 URL 示例：**
```
https://www.xiaohongshu.com/explore/694a779f000000001b027371?xsec_token=ABmo52Gv2L-9BnRWETozL9k9ud85BwFSa6A4yczIBIbbY=&xsec_source=pc_like
```

## 场景 1: 基础视频下载

**需求：** 只下载视频文件到指定目录

```bash
# 下载视频到 D:\Download 目录
yt-dlp -o "D:/Download/%(title)s.%(ext)s" "小红书URL"
```

**输出：**
- 单个视频文件（如 `.mov` 格式）

---

## 场景 2: 完整资源包下载（推荐）

**需求：** 下载视频 + 元数据 + 封面 + 描述，并整理到独立文件夹

```bash
yt-dlp -o "D:/Download/%(title)s/%(title)s.%(ext)s" \
  --write-info-json \
  --write-description \
  --write-thumbnail \
  --convert-thumbnails jpg \
  --write-subs \
  --sub-langs all \
  "小红书URL"
```

### 参数详解

| 参数 | 作用 |
|------|------|
| `-o "D:/Download/%(title)s/..."` | 以视频标题创建文件夹，所有文件放入其中 |
| `--write-info-json` | 下载完整元数据为 JSON 文件 |
| `--write-description` | 下载视频描述文本 |
| `--write-thumbnail` | 下载视频封面图 |
| `--convert-thumbnails jpg` | 将封面转换为 JPG 格式 |
| `--write-subs` | 尝试下载字幕（如果有） |
| `--sub-langs all` | 下载所有语言的字幕 |

### 输出文件结构

```
D:\Download\如何用AI轻松写出任意提示词？\
├── 如何用AI轻松写出任意提示词？.mov         # 视频文件 (266.92 MiB)
├── 如何用AI轻松写出任意提示词？.jpg          # 视频封面图
├── 如何用AI轻松写出任意提示词？.info.json    # 完整元数据
└── 如何用AI轻松写出任意提示词？.description  # 视频描述文本
```

### info.json 包含的信息

```json
{
  "id": "694a779f000000001b027371",
  "title": "如何用AI轻松写出任意提示词？",
  "description": "完整描述文本...",
  "uploader": "作者名称",
  "uploader_id": "作者ID",
  "upload_date": "20241228",
  "timestamp": 1735392000,
  "duration": 1024,
  "view_count": 12345,
  "like_count": 678,
  "tags": ["AI", "提示词", "教程"],
  "thumbnail": "封面URL",
  "formats": [...],
  ...
}
```

---

## 场景 3: 批量下载小红书视频

**需求：** 从文本文件读取多个 URL 批量下载

```bash
# 创建 urls.txt，每行一个 URL
# https://www.xiaohongshu.com/explore/xxx
# https://www.xiaohongshu.com/explore/yyy

# 批量下载（自动应用完整资源包配置）
yt-dlp -o "D:/Download/XHS/%(title)s/%(title)s.%(ext)s" \
  --write-info-json \
  --write-description \
  --write-thumbnail \
  --convert-thumbnails jpg \
  -a urls.txt
```

---

## 常见问题

### Q1: 下载速度慢怎么办？

```bash
# 使用 aria2 多线程下载
yt-dlp --external-downloader aria2 \
  --external-downloader-args "-x 8 -k 1M" \
  "小红书URL"
```

### Q2: 需要登录才能下载的内容？

小红书公开内容无需登录即可下载。如遇认证问题：

```bash
# 从浏览器导入 cookies（Windows 可能遇到 DPAPI 解密问题）
yt-dlp --cookies-from-browser chrome "小红书URL"

# 或使用 cookies.txt 文件
yt-dlp --cookies cookies.txt "小红书URL"
```

**注意：** Windows 上 `--cookies-from-browser` 可能遇到 DPAPI 解密错误，这是 Windows 安全机制导致的。对于小红书公开内容，通常不需要 cookies。

### Q3: 只想下载封面图怎么办？

```bash
yt-dlp --skip-download --write-thumbnail \
  --convert-thumbnails jpg \
  -o "封面/%(title)s.%(ext)s" \
  "小红书URL"
```

### Q4: 如何只获取视频信息而不下载？

```bash
# 输出 JSON 格式的完整信息
yt-dlp --dump-json "小红书URL"

# 或只输出特定字段
yt-dlp --print "%(title)s | %(uploader)s | %(duration)s" "小红书URL"
```

---

## 最佳实践

### 1. 命令别名（Linux/macOS）

在 `~/.bashrc` 或 `~/.zshrc` 中添加：

```bash
# 小红书完整下载别名
alias xhs-dl='yt-dlp -o "~/Downloads/XHS/%(title)s/%(title)s.%(ext)s" \
  --write-info-json \
  --write-description \
  --write-thumbnail \
  --convert-thumbnails jpg'
```

使用：
```bash
xhs-dl "小红书URL"
```

### 2. 配置文件

创建 `~/.config/yt-dlp/config.txt`：

```ini
# 小红书默认配置
-o ~/Downloads/XHS/%(title)s/%(title)s.%(ext)s
--write-info-json
--write-description
--write-thumbnail
--convert-thumbnails jpg
--no-mtime
```

### 3. Python API 使用

```python
import yt_dlp

def download_xhs_complete(url, output_dir):
    """下载小红书视频及所有元数据"""
    ydl_opts = {
        'outtmpl': f'{output_dir}/%(title)s/%(title)s.%(ext)s',
        'writeinfojson': True,
        'writedescription': True,
        'writethumbnail': True,
        'convertthumbnails': 'jpg',
        'writesubtitles': True,
        'subtitleslangs': ['all'],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# 使用
download_xhs_complete(
    'https://www.xiaohongshu.com/explore/xxx',
    'D:/Download'
)
```

---

## 总结

| 场景 | 推荐命令 |
|------|----------|
| 快速下载视频 | `yt-dlp -o "路径/%(title)s.%(ext)s" "URL"` |
| 完整资源包 | 添加 `--write-info-json --write-description --write-thumbnail` |
| 批量下载 | 使用 `-a urls.txt` 配合完整参数 |
| 只下载封面 | `--skip-download --write-thumbnail` |

**关键要点：**
1. 始终使用 `%(title)s` 创建文件夹，避免文件散乱
2. `--write-info-json` 包含最完整的元数据（标签、统计等）
3. 小红书公开视频通常不需要 cookies
4. 使用 `--convert-thumbnails jpg` 统一封面格式
