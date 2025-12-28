# 提取器模板

此模板提供自定义提取器的完整结构。

## 基础模板

```python
# yt_dlp/extractor/mysite.py

import re

from .common import InfoExtractor
from ..utils import (
    ExtractorError,
    determine_ext,
    int_or_none,
    parse_duration,
    unified_timestamp,
)


class MySiteIE(InfoExtractor):
    """MySite 视频提取器

    支持从 www.mysite.com 下载视频
    """

    # 提取器描述
    IE_DESC = 'MySite Video'
    IE_NAME = 'mysite'

    # URL 匹配正则
    _VALID_URL = r'https?://(?:www\.)?mysite\.com/watch/(?P<id>[^/]+)'

    # 测试用例
    _TESTS = [{
        'url': 'https://www.mysite.com/watch/test123',
        'info_dict': {
            'id': 'test123',
            'ext': 'mp4',
            'title': '测试视频',
            'uploader': '测试用户',
            'upload_date': '20250128',
            'timestamp': 1706409600,
            'description': 'md5:expected_hash',
            'thumbnail': 'md5:thumbnail_hash',
        },
        'params': {
            'skip_download': True,  # 测试时不下载
        },
    }]

    def _real_extract(self, url):
        """主提取方法"""
        # 1. 提取视频 ID
        video_id = self._match_id(url)

        # 2. 下载网页
        webpage = self._download_webpage(url, video_id)

        # 3. 提取视频信息
        title = self._html_search_regex(
            r'<h1[^>]+title="([^"]+)"',
            webpage,
            'title',
            fatal=False
        ) or self._html_search_meta(
            'og:title',
            webpage
        )

        # 4. 提取视频 URL
        video_url = self._html_search_regex(
            r'"videoUrl"\s*:\s*"([^"]+)"',
            webpage,
            'video url'
        )

        # 5. 构建格式列表
        formats = [{
            'url': video_url,
            'ext': 'mp4',
            'height': 1080,
            'width': 1920,
        }]

        # 6. 提取元数据
        description = self._html_search_meta(
            'description',
            webpage,
            fatal=False
        )

        uploader = self._html_search_regex(
            r'uploader:\s*"([^"]+)"',
            webpage,
            'uploader',
            fatal=False
        )

        upload_date = self._html_search_regex(
            r'upload_date:\s*"(\d{4}-\d{2}-\d{2})"',
            webpage,
            'upload date',
            fatal=False
        )
        if upload_date:
            upload_date = upload_date.replace('-', '')

        thumbnail = self._html_search_meta(
            'og:image',
            webpage,
            fatal=False
        )

        # 7. 返回信息字典
        return {
            'id': video_id,
            'title': title,
            'formats': formats,
            'description': description,
            'uploader': uploader,
            'upload_date': upload_date,
            'thumbnail': thumbnail,
        }
```

## M3U8/HLS 模板

```python
class MySiteIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?mysite\.com/watch/(?P<id>[^/]+)'

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)

        # 提取 M3U8 URL
        m3u8_url = self._html_search_regex(
            r'"hlsUrl"\s*:\s*"([^"]+\.m3u8[^"]*)"',
            webpage,
            'm3u8 url'
        )

        # 提取 M3U8 格式
        formats = self._extract_m3u8_formats(
            m3u8_url,
            video_id,
            ext='mp4',
            entry_protocol='m3u8_native'
        )

        title = self._html_search_meta('og:title', webpage)

        return {
            'id': video_id,
            'title': title,
            'formats': formats,
        }
```

## DASH 模板

```python
class MySiteIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?mysite\.com/watch/(?P<id>[^/]+)'

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)

        # 提取 MPD URL
        mpd_url = self._html_search_regex(
            r'"dashUrl"\s*:\s*"([^"]+\.mpd[^"]*)"',
            webpage,
            'mpd url'
        )

        # 提取 DASH 格式
        formats = self._extract_mpd_formats(
            mpd_url,
            video_id,
            mpd_id='dash'
        )

        title = self._html_search_meta('og:title', webpage)

        return {
            'id': video_id,
            'title': title,
            'formats': formats,
        }
```

## JSON API 模板

```python
class MySiteIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?mysite\.com/watch/(?P<id>[^/]+)'

    def _real_extract(self, url):
        video_id = self._match_id(url)

        # 调用 API
        api_url = f'https://api.mysite.com/v1/videos/{video_id}'
        data = self._download_json(api_url, video_id)

        # 从 JSON 提取信息
        title = data['title']
        description = data.get('description')

        # 构建格式
        formats = []
        for fmt in data['formats']:
            formats.append({
                'url': fmt['url'],
                'ext': fmt.get('container', 'mp4'),
                'height': fmt.get('height'),
                'width': fmt.get('width'),
                'format_id': fmt.get('quality', 'unknown'),
            })

        return {
            'id': video_id,
            'title': title,
            'formats': formats,
            'description': description,
        }
```

## 带认证的模板

```python
class MySiteIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?mysite\.com/watch/(?P<id>[^/]+)'
    _NETRC_MACHINE = 'mysite'  # 支持 .netrc

    def _perform_login(self, username, password):
        """登录处理"""
        login_url = 'https://www.mysite.com/login'

        # 获取登录页面
        login_page = self._download_webpage(login_url, None)

        # 提取 CSRF token
        csrf_token = self._html_search_regex(
            r'name="csrf_token"\s+value="([^"]+)"',
            login_page,
            'csrf token',
            fatal=False
        )

        # 提交登录
        login_form = {
            'username': username,
            'password': password,
            'csrf_token': csrf_token or '',
        }

        login_page = self._download_webpage(
            login_url,
            None,
            data=login_form,
            headers={'Referer': login_url}
        )

        # 检查登录成功
        if 'error' in login_page:
            raise ExtractorError('Login failed')

    def _real_extract(self, url):
        video_id = self._match_id(url)

        # 如果需要登录
        if self._login_required():
            self._perform_login(
                self._get_netrc_credentials('username'),
                self._get_netrc_credentials('password')
            )

        # 继续提取...
        webpage = self._download_webpage(url, video_id)
        # ...
```

## 播放列表模板

```python
class MySitePlaylistIE(InfoExtractor):
    IE_DESC = 'MySite 播放列表'
    IE_NAME = 'mysite:playlist'

    _VALID_URL = r'https?://(?:www\.)?mysite\.com/playlist/(?P<id>[^/]+)'

    _TESTS = [{
        'url': 'https://www.mysite.com/playlist/test',
        'info_dict': {
            'id': 'test',
            'title': '测试播放列表',
        },
        'playlist_mincount': 3,
    }]

    def _real_extract(self, url):
        playlist_id = self._match_id(url)

        # 下载播放列表页面
        webpage = self._download_webpage(url, playlist_id)

        # 提取播放列表标题
        title = self._html_search_regex(
            r'<h1>([^<]+)</h1>',
            webpage,
            'title'
        )

        # 提取视频列表
        video_ids = self._html_search_regexes(
            r'<a[^>]+href="/watch/([^"]+)"',
            webpage
        )

        # 构建条目
        entries = [{
            '_type': 'url',
            'url': f'https://www.mysite.com/watch/{video_id}',
            'ie_key': 'MySite',
        } for video_id in video_ids]

        return {
            '_type': 'playlist',
            'id': playlist_id,
            'title': title,
            'entries': entries,
        }
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

## 测试提取器

```bash
# 运行测试
python -m yt_dlp.test test_MySiteIE

# 测试 URL
yt-dlp -I "https://www.mysite.com/watch/test123"

# 调试
yt-dlp -v --skip-download "https://www.mysite.com/watch/test123"
```
