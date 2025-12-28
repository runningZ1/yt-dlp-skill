# Python API 模板

## 基础下载模板

```python
#!/usr/bin/env python3
"""
基础视频下载脚本
"""

import yt_dlp


def download_video(url, output_dir='downloads'):
    """下载视频"""
    ydl_opts = {
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'format': 'bestvideo+bestaudio',
        'merge_output_format': 'mp4',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


if __name__ == '__main__':
    download_video('https://www.youtube.com/watch?v=xxx')
```

## 音频下载模板

```python
#!/usr/bin/env python3
"""
音频下载脚本
"""

import yt_dlp


def download_audio(url, output_dir='audio', audio_format='mp3'):
    """下载音频"""
    ydl_opts = {
        'format': 'bestaudio',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': audio_format,
            'preferredquality': '0',
        }],
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


if __name__ == '__main__':
    download_audio('https://www.youtube.com/watch?v=xxx', audio_format='mp3')
```

## 播放列表下载模板

```python
#!/usr/bin/env python3
"""
播放列表下载脚本
"""

import yt_dlp


def download_playlist(playlist_url, output_dir='playlists'):
    """下载播放列表"""
    ydl_opts = {
        'outtmpl': f'{output_dir}/%(playlist_title)s/%(playlist_index)03d - %(title)s.%(ext)s',
        'format': 'bestvideo+bestaudio',
        'merge_output_format': 'mp4',
        'ignoreerrors': True,  # 失败继续
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])


if __name__ == '__main__':
    download_playlist('https://www.youtube.com/playlist?list=xxx')
```

## 带进度监控的下载模板

```python
#!/usr/bin/env python3
"""
带进度监控的下载脚本
"""

import time
import yt_dlp


class ProgressMonitor:
    """进度监控器"""

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
                total = d.get('_total_bytes_str', 'N/A')
                downloaded = d.get('_downloaded_bytes_str', 'N/A')

                print(f"[{elapsed:.0f}s] {percent} - {downloaded}/{total} - Speed: {speed} - ETA: {eta}")

        elif d['status'] == 'finished':
            total_time = time.time() - self.start_time
            print(f'下载完成！耗时: {total_time:.1f}秒')


def download_with_progress(url, output_dir='downloads'):
    """带进度监控的下载"""
    ydl_opts = {
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'format': 'bestvideo+bestaudio',
        'progress_hooks': [ProgressMonitor()],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


if __name__ == '__main__':
    download_with_progress('https://www.youtube.com/watch?v=xxx')
```

## 信息提取模板

```python
#!/usr/bin/env python3
"""
视频信息提取脚本
"""

import json
import yt_dlp


def extract_video_info(url):
    """提取视频信息"""
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

        return {
            'id': info.get('id'),
            'title': info.get('title'),
            'description': info.get('description'),
            'uploader': info.get('uploader'),
            'uploader_id': info.get('uploader_id'),
            'uploader_url': info.get('uploader_url'),
            'channel': info.get('channel'),
            'channel_id': info.get('channel_id'),
            'channel_url': info.get('channel_url'),
            'duration': info.get('duration'),
            'view_count': info.get('view_count'),
            'like_count': info.get('like_count'),
            'upload_date': info.get('upload_date'),
            'thumbnail': info.get('thumbnail'),
            'webpage_url': info.get('webpage_url'),
            'formats': [
                {
                    'format_id': f.get('format_id'),
                    'ext': f.get('ext'),
                    'height': f.get('height'),
                    'width': f.get('width'),
                    'fps': f.get('fps'),
                    'filesize': f.get('filesize'),
                    'vcodec': f.get('vcodec'),
                    'acodec': f.get('acodec'),
                }
                for f in info.get('formats', [])
            ],
        }


if __name__ == '__main__':
    url = 'https://www.youtube.com/watch?v=xxx'
    info = extract_video_info(url)
    print(json.dumps(info, indent=2, ensure_ascii=False))
```

## 自定义格式选择模板

```python
#!/usr/bin/env python3
"""
自定义格式选择下载脚本
"""

import yt_dlp


def custom_format_selector(ctx):
    """自定义格式选择函数"""
    formats = ctx['formats']
    # 可用字段: ctx['formats'], ctx['info_dict']

    # 选择最佳 1080p 或以下
    for f in formats:
        if f.get('height', 0) <= 1080 and f.get('vcodec') != 'none':
            return f

    # 如果没有找到，返回最佳格式
    return formats[-1]


def download_with_custom_format(url):
    """使用自定义格式选择下载"""
    ydl_opts = {
        'outtmpl': '%(title)s.%(ext)s',
        'format': custom_format_selector,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


if __name__ == '__main__':
    download_with_custom_format('https://www.youtube.com/watch?v=xxx')
```

## 错误处理模板

```python
#!/usr/bin/env python3
"""
带错误处理的下载脚本
"""

import sys
import yt_dlp
from yt_dlp.utils import DownloadError, ExtractorError


def safe_download(url, output_dir='downloads'):
    """安全下载，包含错误处理"""
    ydl_opts = {
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'ignoreerrors': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            if info is None:
                print(f"错误: 无法提取信息 - {url}")
                return False

            if 'entries' in info:  # 播放列表
                videos = [e for e in info['entries'] if e is not None]
                print(f"播放列表包含 {len(videos)} 个视频")

                for i, entry in enumerate(videos, 1):
                    print(f"[{i}/{len(videos)}] {entry.get('title', 'Unknown')}")

            else:  # 单个视频
                print(f"标题: {info.get('title', 'Unknown')}")
                print(f"上传者: {info.get('uploader', 'Unknown')}")
                print(f"时长: {info.get('duration_string', 'Unknown')}")

            # 开始下载
            ydl.download([url])
            return True

    except DownloadError as e:
        print(f"下载错误: {e}")
        return False

    except ExtractorError as e:
        print(f"提取错误: {e}")
        return False

    except Exception as e:
        print(f"未知错误: {e}")
        return False


if __name__ == '__main__':
    url = sys.argv[1] if len(sys.argv) > 1 else 'https://www.youtube.com/watch?v=xxx'
    success = safe_download(url)
    sys.exit(0 if success else 1)
```

## 配置文件模板

```python
# config.py

# 通用配置
DEFAULT_OPTIONS = {
    'outtmpl': 'downloads/%(title)s.%(ext)s',
    'format': 'bestvideo+bestaudio',
    'merge_output_format': 'mp4',
    'ignoreerrors': True,
    'no_warnings': True,
}

# 音频配置
AUDIO_OPTIONS = {
    **DEFAULT_OPTIONS,
    'format': 'bestaudio',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '0',
    }],
}

# 高质量配置
HIGH_QUALITY_OPTIONS = {
    **DEFAULT_OPTIONS,
    'format': 'bestvideo[height<=2160]+bestaudio',
}

# 快速下载配置
FAST_OPTIONS = {
    **DEFAULT_OPTIONS,
    'format': 'worst',  # 最差质量 = 最快下载
}
```

使用配置:

```python
#!/usr/bin/env python3
import yt_dlp
from config import DEFAULT_OPTIONS, AUDIO_OPTIONS


def download_with_config(url, options=DEFAULT_OPTIONS):
    """使用配置下载"""
    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])


if __name__ == '__main__':
    import sys

    url = sys.argv[1]
    download_with_config(url, AUDIO_OPTIONS)
```
