# 提取器开发指南

## 概述

本指南详细介绍如何为 yt-dlp 编写自定义提取器。

## InfoExtractor 基类

位置: `yt_dlp/extractor/common.py`

### 核心属性

```python
class InfoExtractor:
    # 提取器描述
    IE_DESC = 'Site Name'
    IE_NAME = 'sitename'

    # URL 匹配正则（必需）
    _VALID_URL = r'https?://(?:www\.)?example\.com/(?P<path>[^/]+)'

    # 测试用例（推荐）
    _TESTS = []

    # 是否适用于播放列表
    _WORKING = True

    # 是否需要登录
    _LOGIN_REQUIRED = False

    # 网络请求超时（秒）
    _NETRC_MACHINE = None
```

### 核心方法

#### suitable()

检查 URL 是否匹配此提取器。

```python
@classmethod
def suitable(cls, url):
    """Return whether this extractor can handle the given URL."""
    return re.match(cls._VALID_URL, url) is not None
```

#### _real_extract()

子类必须实现的提取方法。

```python
def _real_extract(self, url):
    """
    Extract information from URL.

    Returns:
        dict: info_dict with video information
    """
    raise NotImplementedError('Subclasses must implement this method')
```

#### extract()

主提取入口。

```python
def extract(self, url):
    """
    Extract info from URL.

    Returns:
        dict: info_dict
    """
    try:
        return self._real_extract(url)
    except ExtractorError as e:
        raise
```

## 常用工具方法

### URL 处理

```python
# 从 URL 提取 ID
video_id = self._match_id(url)
# 或使用命名组
video_id = self._match_valid_url(url).group('id')

# 构建完整 URL
full_url = urljoin(base_url, relative_url)

# 解析 URL
parsed = urllib.parse.urlparse(url)
```

### HTTP 请求

```python
# 下载网页
webpage = self._download_webpage(url, video_id)

# 带请求头
webpage = self._download_webpage(
    url, video_id,
    headers={'User-Agent': 'CustomUA', 'Referer': 'https://example.com'}
)

# POST 请求
webpage = self._download_webpage(
    api_url, video_id,
    data={'key': 'value'},  # 表单数据
    json={'key': 'value'},  # JSON 数据
)

# 不在失败时抛出异常
webpage = self._download_webpage(
    url, video_id,
    expected_status=False  # 返回响应即使失败
)

# 处理重定向
webpage = self._download_webpage(
    url, video_id,
    note='Downloading page...',
    errnote='Failed to download page'
)
```

### JSON 处理

```python
# 从 HTML 提取 JSON
json_data = self._search_json(
    r'var\s+config\s*=',  # 搜索模式
    webpage,              # 源字符串
    'config',             # 数据名称
    video_id,             # 用于错误消息
)

# 从 script 标签提取
json_data = self._search_json(
    r'<script[^>]+type="application/json">\s*',
    webpage,
    'json_data',
    video_id,
    end_pattern=r'</script>'
)

# 解析 JSON 字符串
data = self._parse_json(json_string, video_id)

# 从 URL 获取 JSON
json_data = self._download_json(
    'https://api.example.com/video/123',
    video_id
)
```

### HTML 解析

```python
# 正则搜索
title = self._html_search_regex(
    r'<h1[^>]+title="([^"]+)"',  # 正则模式
    webpage,                       # 源字符串
    'title'                        # 字段名（用于错误消息）
)

# 带默认值
title = self._html_search_regex(
    r'<h1>(.+?)</h1>',
    webpage,
    'title',
    default='Unknown'
)

# 搜索多个
matches = self._html_search_regexes(
    r'<a[^>]+href="([^"]+)"',
    webpage
)

# 搜索 meta 标签
description = self._html_search_meta('description', webpage)
thumbnail = self._html_search_meta('og:image', webpage)

# 使用 XPath
title = self._search_regex(
    r'//h1/@title',
    webpage,
    'title'
)

# 使用 CSS 选择器
from yt_dlp.utils import get_elements_by_class
elements = get_elements_by_class('video-class', webpage)
```

### 清理和转换

```python
# 清理 HTML 标签
clean_text = self._html_search_regex(
    r'<p>(.+?)</p>',
    webpage,
    'text',
    # 自动清理 HTML
)

# 清理空白
clean_text = self._clean_html(webpage)

# 编码转换
text = self._decode_text(text, encoding)

# 日期转换
upload_date = self._search_regex(
    r'发布于\s+(\d{4}-\d{2}-\d{2})',
    webpage,
    'upload_date'
)
# 统一格式为 YYYYMMDD
upload_date = upload_date.replace('-', '')

# 数字转换
view_count = int(self._search_regex(
    r'(\d+)\s*次观看',
    webpage,
    'view count'
))

# 时长转换
duration = self._parse_duration(
    self._html_search_regex(r'duration:\s*(\d+:\d+)', webpage, 'duration')
)
```

### 构建返回字典

```python
def _real_extract(self, url):
    video_id = self._match_id(url)
    webpage = self._download_webpage(url, video_id)

    # 基础信息
    info = {
        'id': video_id,
        'title': self._html_search_regex(r'<title>([^<]+)</title>', webpage, 'title'),
        'description': self._html_search_meta('description', webpage),
        'thumbnail': self._html_search_meta('og:image', webpage),
        'uploader': self._html_search_regex(r'uploader:\s*([^<]+)', webpage, 'uploader'),
        'upload_date': self._search_regex(r'date:\s*(\d{4}-\d{2}-\d{2})', webpage, 'upload_date'),
    }

    # 格式
    formats = self._extract_formats(url, video_id, webpage)
    info['formats'] = formats

    # 字幕
    info['subtitles'] = self._extract_subtitles(video_id, webpage)

    return info
```

## 格式提取

### 直接 URL 格式

```python
def _extract_formats(self, url, video_id):
    formats = [{
        'url': 'https://example.com/video.mp4',
        'ext': 'mp4',
        'height': 1080,
        'width': 1920,
        'fps': 30,
        'vcodec': 'h264',
        'acodec': 'none',  # video only
    }]
    return formats
```

### M3U8 格式

```python
def _extract_m3u8_formats(self, m3u8_url, video_id, **kwargs):
    return self._extract_m3u8_formats(
        m3u8_url,
        video_id,
        ext='mp4',
        entry_protocol='m3u8_native',
        **kwargs
    )
```

### DASH 格式

```python
def _extract_dash_formats(self, mpd_url, video_id, **kwargs):
    return self._extract_mpd_formats(
        mpd_url,
        video_id,
        mpd_id='dash',
        **kwargs
    )
```

### 从 JSON 提取格式

```python
def _extract_formats_from_json(self, json_data, video_id):
    formats = []
    for quality in json_data['qualities']:
        formats.append({
            'url': quality['url'],
            'format_id': quality['label'],
            'height': quality.get('height'),
            'width': quality.get('width'),
            'ext': 'mp4',
        })
    return formats
```

## 字幕提取

```python
def _get_subtitles(self, video_id, webpage):
    subtitles = {}

    # 查找字幕 URL
    subtitle_url = self._html_search_regex(
        r'"subtitle"\s*:\s*"([^"]+)"',
        webpage,
        'subtitle url',
        fatal=False  # 字幕是可选的
    )

    if subtitle_url:
        subtitles['en'] = [{
            'url': subtitle_url,
            'ext': 'srt',
        }]

    return subtitles
```

## 认证处理

### 基础登录

```python
def _perform_login(self, username, password):
    login_url = 'https://www.example.com/login'

    # 获取登录页面
    login_page = self._download_webpage(login_url, None)

    # 提取 CSRF token
    csrf_token = self._html_search_regex(
        r'name="csrf_token"\s+value="([^"]+)"',
        login_page,
        'csrf token'
    )

    # 提交登录表单
    login_form = {
        'username': username,
        'password': password,
        'csrf_token': csrf_token,
    }

    login_post = self._download_webpage(
        login_url,
        None,
        data=login_form,
        headers={'Referer': login_url}
    )

    # 验证登录成功
    if 'error' in login_post:
        raise ExtractorError('Login failed')
```

### OAuth 认证

```python
def _perform_login(self, username, password):
    # 获取 OAuth 令牌
    oauth_url = 'https://api.example.com/oauth/token'

    token_data = self._download_json(
        oauth_url,
        None,
        data={
            'grant_type': 'password',
            'username': username,
            'password': password,
        },
        headers={'Content-Type': 'application/json'}
    )

    self._token = token_data['access_token']
```

## 播放列表支持

```python
class MySitePlaylistIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?mysite\.com/playlist/(?P<id>[^/]+)'

    def _real_extract(self, url):
        playlist_id = self._match_id(url)

        # 获取播放列表页面
        webpage = self._download_webpage(url, playlist_id)

        # 提取视频列表
        video_urls = self._html_search_regexes(
            r'<a[^>]+href="/watch/([^"]+)"',
            webpage
        )

        entries = [{
            '_type': 'url',
            'url': f'https://www.mysite.com/watch/{video_id}',
            'ie_key': 'MySite',
        } for video_id in video_urls]

        return {
            '_type': 'playlist',
            'id': playlist_id,
            'title': self._html_search_regex(r'<h1>([^<]+)</h1>', webpage, 'title'),
            'entries': entries,
        }
```

## 测试用例

```python
_TESTS = [{
    'url': 'https://www.example.com/watch/test123',
    'info_dict': {
        'id': 'test123',
        'ext': 'mp4',
        'title': 'Test Video',
        'uploader': 'TestUser',
        'upload_date': '20250128',
        'description': 'md5:expected_hash',
        'thumbnail': 'md5:thumbnail_hash',
    },
    'params': {
        'skip_download': True,  # 测试时不下载
    },
}, {
    'url': 'https://www.example.com/playlist/test',
    'info_dict': {
        'id': 'test',
        'title': 'Test Playlist',
    },
    'playlist_mincount': 5,  # 至少 5 个视频
    'playlist': [{
        'info_dict': {
            'id': 'video1',
            'ext': 'mp4',
            'title': 'Video 1',
        },
    }],
}]
```

## 注册提取器

在 `yt_dlp/extractor/_extractors.py` 中注册:

```python
from .mysite import MySiteIE, MySitePlaylistIE

_ALL_CLASSES = [
    # ...
    MySiteIE,
    MySitePlaylistIE,
]
```

## 最佳实践

### 规则 1: 始终使用 fatal=False

```python
# 对于可选数据
thumbnail = self._html_search_meta('og:image', webpage, fatal=False)
description = self._html_search_regex(r'<p>(.+?)</p>', webpage, 'description', fatal=False)
```

### 规则 2: 优先使用专用方法

```python
# 优先
thumbnail = self._html_search_meta('og:image', webpage)

# 而不是
thumbnail = self._html_search_regex(r'og:image"\s+content="([^"]+)"', webpage, 'thumbnail')
```

### 规则 3: 提供清晰的错误消息

```python
raise ExtractorError(
    f'Failed to extract video info for {video_id}. '
    f'The page may have been updated.'
)
```

### 规则 4: 处理异常

```python
try:
    video_url = self._html_search_regex(r'"url":"([^"]+)"', webpage, 'video url')
except ExtractorError:
    self.report_warning('Could not extract video URL, trying fallback method')
    # 备用方法...
```

## 调试技巧

### 保存网页内容

```python
self._save_webpage('debug.html', webpage)
```

### 打印调试信息

```python
self.to_screen(f'DEBUG: Found {len(formats)} formats')
self.write_debug(f'JSON data: {json_data}')
```

### 使用断点

```python
import pdb; pdb.set_trace()
```

## 参考资料

- [提取器开发工作流](../workflows/extractor-development.md)
- [调试工作流](../workflows/debugging.md)
- [架构参考](architecture.md)
- [模板](../templates/extractor-template.py)
