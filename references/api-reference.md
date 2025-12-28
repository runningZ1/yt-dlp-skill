# Python API 参考

## 概述

yt-dlp 提供了完整的 Python API，可以在代码中集成下载功能。

## YoutubeDL 类

### 基础用法

```python
import yt_dlp

# 创建实例
ydl_opts = {}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['https://www.youtube.com/watch?v=BaW_jenozKc'])
```

### 构造函数参数

```python
ydl_opts = {
    # 输出选项
    'outtmpl': '%(title)s.%(ext)s',        # 输出文件名模板
    'paths': {'home': 'downloads'},         # 输出目录
    'restrictfilenames': True,              # 限制文件名（仅 ASCII）
    'windowsfilenames': True,               # Windows 兼容文件名

    # 下载选项
    'format': 'bestvideo+bestaudio',        # 格式选择
    'format_sort': ['res', 'fps'],          # 格式排序
    'merge_output_format': 'mp4',           # 合并输出格式
    'keepvideo': False,                     # 合并后保留原视频

    # 后处理
    'postprocessors': [...],                # 后处理器列表
    'prefer_ffmpeg': True,                  # 优先使用 FFmpeg

    # 网络选项
    'proxy': 'http://127.0.0.1:8080',       # 代理
    'socket_timeout': 60,                   # 超时时间

    # 认证
    'username': 'user',
    'password': 'pass',
    'video_password': 'pass',
    'cookiesfrombrowser': ('chrome',),      # 从浏览器导入 cookies
    'cookiefile': 'cookies.txt',

    # 元数据
    'writeinfojson': True,                  # 写入 info.json
    'writedescription': True,               # 写入描述
    'writeannotations': True,               # 写入注释
    'writesubtitles': True,                 # 写入字幕
    'subtitleslangs': ['en', 'zh'],         # 字幕语言
    'writeautomaticsub': True,              # 写入自动字幕

    # 缩略图
    'writethumbnail': True,                 # 写入缩略图
    'writethumbnail': False,

    # 日志和输出
    'quiet': False,                         # 静默模式
    'no_warnings': False,                   # 不显示警告
    'verbose': True,                        # 详细输出
    'print_to_file': True,                  # 输出到文件
    'print_filename': 'output.txt',

    # 缓存
    'cachedir': '/path/to/cache',           # 缓存目录
    'no_cache': False,                      # 不使用缓存

    # 播放列表
    'noplaylist': False,                    # 不下载播放列表
    'playliststart': 1,                     # 播放列表起始位置
    'playlistend': None,                    # 播放列表结束位置
    'playlistreverse': False,               # 反向播放列表

    # 其他
    'ignoreerrors': True,                   # 忽略错误继续下载
    'nocheckcertificate': False,            # 不检查 SSL 证书
    'prefer_insecure': False,               # 优先使用 HTTP
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['URL'])
```

## 主要方法

### download()

下载视频或播放列表。

```python
def download(self, url_list):
    """
    下载给定的 URL 列表

    Args:
        url_list: URL 或 URL 列表

    Returns:
        bool: 成功返回 True，失败返回 False
    """
    pass
```

### extract_info()

提取信息而不下载。

```python
def extract_info(self, url, download=True, process=True):
    """
    提取视频信息

    Args:
        url: 视频 URL
        download: 是否下载
        process: 是否处理（格式选择、后处理）

    Returns:
        dict: 视频信息字典
    """
    pass
```

**示例：**

```python
# 只获取信息不下载
ydl_opts = {'quiet': True}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info('URL', download=False)
    print(info['title'])
    print(info['uploader'])
    print(info['duration'])
    print(info['view_count'])

# 获取格式信息
info = ydl.extract_info('URL', download=False)
for fmt in info['formats']:
    print(f"{fmt['format_id']}: {fmt['ext']} {fmt.get('height', 'N/A')}p")
```

### prepare_filename()

获取输出文件名。

```python
def prepare_filename(self, info):
    """
    准备输出文件名

    Args:
        info: 信息字典

    Returns:
        str: 文件名
    """
    pass
```

**示例：**

```python
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info('URL', download=False)
    filename = ydl.prepare_filename(info)
    print(f'Output file: {filename}')
```

### add_post_processor()

添加后处理器。

```python
from yt_dlp.postprocessor import PostProcessor

class MyPP(PostProcessor):
    def run(self, info):
        print(f"Processing: {info['filepath']}")
        return [info], []

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.add_post_processor(MyPP(ydl))
    ydl.download(['URL'])
```

## 进阶用法

### 下载回调

```python
class MyLogger:
    def debug(self, msg):
        print(f'DEBUG: {msg}')

    def warning(self, msg):
        print(f'WARNING: {msg}')

    def error(self, msg):
        print(f'ERROR: {msg}')

def my_hook(d):
    if d['status'] == 'downloading':
        print(f"Downloading: {d['_percent_str']} at {d['_speed_str']}")
    elif d['status'] == 'finished':
        print('Download complete, now post-processing...')

ydl_opts = {
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['URL'])
```

### 自定义格式选择

```python
def format_selector(ctx):
    """自定义格式选择函数"""
    formats = ctx['formats']
    # 选择最佳 1080p 或以下
    for f in formats:
        if f.get('height', 0) <= 1080:
            return f
    return formats[-1]  # 返回最后一个

ydl_opts = {
    'format': format_selector,
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['URL'])
```

### 批量下载

```python
urls = [
    'https://www.youtube.com/watch?v=video1',
    'https://www.youtube.com/watch?v=video2',
    'https://www.youtube.com/watch?v=video3',
]

ydl_opts = {
    'outtmpl': 'downloads/%(title)s.%(ext)s',
    'ignoreerrors': True,  # 失败继续
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(urls)
```

### 播放列表处理

```python
ydl_opts = {
    'extract_flat': True,  # 只获取播放列表，不下载视频
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    result = ydl.extract_info('PLAYLIST_URL', download=False)

    for entry in result['entries']:
        print(f"{entry['title']}: {entry['url']}")
```

### 下载特定播放列表片段

```python
ydl_opts = {
    'playliststart': 5,   # 从第 5 个开始
    'playlistend': 10,    # 到第 10 个结束
    'noplaylist': False,
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['PLAYLIST_URL'])
```

### 字幕处理

```python
ydl_opts = {
    'writesubtitles': True,
    'subtitleslangs': ['en', 'zh-Hans', 'zh-Hant'],
    'writeautomaticsub': True,
    'subtitlesformat': 'srt',
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['URL'])
```

### 元数据处理

```python
ydl_opts = {
    'writeinfojson': True,           # 写入 info.json
    'writedescription': True,        # 写入描述文件
    'writeannotations': True,        # 写入注释
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['URL'])
```

## 实用示例

### 示例 1: 只获取视频信息

```python
import yt_dlp

def get_video_info(url):
    ydl_opts = {'quiet': True, 'no_warnings': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

        return {
            'title': info.get('title'),
            'uploader': info.get('uploader'),
            'duration': info.get('duration'),
            'view_count': info.get('view_count'),
            'like_count': info.get('like_count'),
            'upload_date': info.get('upload_date'),
            'description': info.get('description'),
            'thumbnail': info.get('thumbnail'),
        }

# 使用
info = get_video_info('https://www.youtube.com/watch?v=xxx')
print(f"Title: {info['title']}")
print(f"Duration: {info['duration']} seconds")
```

### 示例 2: 下载音频

```python
def download_audio(url, output_dir='audio'):
    ydl_opts = {
        'format': 'bestaudio',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '0',
        }],
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# 使用
download_audio('https://www.youtube.com/watch?v=xxx')
```

### 示例 3: 下载最佳 MP4

```python
def download_best_mp4(url, max_height=1080):
    ydl_opts = {
        'format': f'bestvideo[height<={max_height}][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': '%(title)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# 使用
download_best_mp4('https://www.youtube.com/watch?v=xxx', max_height=720)
```

### 示例 4: 进度监控

```python
import time

class ProgressMonitor:
    def __init__(self):
        self.start_time = None
        self.last_update = None

    def __call__(self, d):
        if d['status'] == 'downloading':
            if self.start_time is None:
                self.start_time = time.time()
                self.last_update = self.start_time

            now = time.time()
            if now - self.last_update >= 1:  # 每秒更新一次
                self.last_update = now
                elapsed = now - self.start_time
                percent = d.get('_percent_str', 'N/A')
                speed = d.get('_speed_str', 'N/A')
                eta = d.get('_eta_str', 'N/A')
                print(f"[{elapsed:.0f}s] {percent} - Speed: {speed} - ETA: {eta}")

        elif d['status'] == 'finished':
            total_time = time.time() - self.start_time
            print(f'Download complete in {total_time:.1f}s')

ydl_opts = {
    'progress_hooks': [ProgressMonitor()],
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['URL'])
```

### 示例 5: 错误处理

```python
def safe_download(url):
    ydl_opts = {
        'ignoreerrors': True,
        'no_warnings': True,
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(url, download=False)

            if result is None:
                print(f"Failed to extract info from: {url}")
                return None

            if 'entries' in result:  # 播放列表
                videos = [e for e in result['entries'] if e is not None]
                print(f"Playlist has {len(videos)} videos")
                return result
            else:  # 单个视频
                print(f"Video: {result.get('title')}")
                return result

    except Exception as e:
        print(f"Error processing {url}: {e}")
        return None

# 使用
result = safe_download('https://www.youtube.com/watch?v=xxx')
if result:
    print("Success!")
```

## 异常处理

```python
from yt_dlp.utils import (
    DownloadError,
    ExtractorError,
    UnsupportedError,
)

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
except DownloadError as e:
    print(f"Download failed: {e}")
except ExtractorError as e:
    print(f"Extraction failed: {e}")
except UnsupportedError as e:
    print(f"URL not supported: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## 参考资料

- [架构参考](architecture.md)
- [格式选择器参考](format-selector.md)
- [后处理器参考](postprocessors.md)
- [提取器开发指南](extractor-guide.md)
