# 提取器开发工作流

## 目标

为 yt-dlp 编写自定义提取器，支持新的视频网站。

## 前置条件

- [ ] 熟悉 Python 编程
- [ ] 了解 HTTP 请求和 HTML/JSON 解析
- [ ] 已阅读 [架构参考](../references/architecture.md)
- [ ] 有目标网站的访问权限

## 步骤

### 步骤 1: 分析目标网站

```bash
# 使用 --print 和 --skip-download 分析网站
yt-dlp --skip-download --print "%(json)s" "TARGET_URL"

# 查看原始请求
yt-dlp --print traffic "TARGET_URL"

# 查看下载的网页内容
yt-dlp --write-pages "TARGET_URL"
# 页面内容保存在 .dump 文件中
```

**分析要点:**
1. 视频真实 URL 在哪里？（HTML、JSON、API）
2. 是否需要认证？
3. 是否有 API 可以调用？
4. 视频和音频是否分开？

### 步骤 2: 创建提取器文件

```bash
# 在 yt-dlp/yt_dlp/extractor/ 目录创建新文件
touch yt_dlp/extractor/mysite.py
```

### 步骤 3: 基础提取器模板

```python
# yt_dlp/extractor/mysite.py

from .common import InfoExtractor


class MySiteIE(InfoExtractor):
    # 提取器描述
    IE_DESC = 'MySite Video'
    IE_NAME = 'mysite'

    # 正则匹配 URL
    _VALID_URL = r'https?://(?:www\.)?mysite\.com/watch/(?P<id>[^/]+)'

    # 测试用例（必须）
    _TESTS = [{
        'url': 'https://www.mysite.com/watch/abc123',
        'info_dict': {
            'id': 'abc123',
            'ext': 'mp4',
            'title': '视频标题',
            'uploader': '上传者',
            # ... 更多字段
        },
        'params': {
            'skip_download': True,  # 测试时不下载
        }
    }]

    def _real_extract(self, url):
        """主提取方法"""
        # 1. 提取视频 ID
        video_id = self._match_id(url)

        # 2. 下载网页
        webpage = self._download_webpage(url, video_id)

        # 3. 提取信息
        title = self._html_search_regex(
            r'<h1[^>]+title="([^"]+)"', webpage, 'title'
        )

        # 4. 构建返回字典
        return {
            'id': video_id,
            'title': title,
            'url': 'https://example.com/video.mp4',
            'ext': 'mp4',
        }
```

### 步骤 4: 实现核心方法

#### 方法 1: 提取视频 ID

```python
def _real_extract(self, url):
    # 从 URL 提取 ID
    video_id = self._match_id(url)
    # 或使用自定义正则
    video_id = self._html_search_regex(r'/watch/([^/]+)', url, 'video id')
```

#### 方法 2: 下载网页

```python
# 基础下载
webpage = self._download_webpage(url, video_id)

# 添加请求头
webpage = self._download_webpage(
    url, video_id,
    headers={'User-Agent': 'CustomUA'}
)

# POST 请求
webpage = self._download_webpage(
    api_url, video_id,
    data={'key': 'value'},
    headers={'Content-Type': 'application/json'}
)

# 处理错误
webpage = self._download_webpage(
    url, video_id,
    expected_status=True  # 不在 404 时抛出异常
)
```

#### 方法 3: 提取 JSON 数据

```python
# 从 JSON-LD 提取
json_data = self._search_json(
    ld_json_schema, webpage, 'json_data', video_id
)

# 从 script 标签提取
json_data = self._search_json(
    r'<script[^>]+type="application/json">\s*', webpage, 'json_data', video_id
)

# 从变量赋值提取
json_data = self._search_json(
    r'var\s+config\s*=', webpage, 'config', video_id
)

# 解析 JSON 字符串
data = self._parse_json(json_string, video_id)
```

#### 方法 4: 搜索 HTML

```python
# 搜索正则
title = self._html_search_regex(
    r'<h1[^>]+title="([^"]+)"', webpage, 'title'
)

# 搜索带默认值
title = self._html_search_regex(
    r'<h1>(.+?)</h1>', webpage, 'title', default='Unknown'
)

# 搜索多个
matches = self._html_search_regexes(
    r'<a[^>]+href="([^"]+)"', webpage
)

# 使用 XPath
title = self._html_search_meta('og:title', webpage)
thumbnail = self._html_search_meta('og:image', webpage)
```

#### 方法 5: 构建格式列表

```python
def _real_extract(self, url):
    # ... 获取数据 ...

    formats = []

    # 单个格式
    formats.append({
        'url': 'https://example.com/video.mp4',
        'ext': 'mp4',
        'height': 1080,
        'width': 1920,
        'fps': 30,
    })

    # 多个格式
    for quality in ['360p', '720p', '1080p']:
        formats.append({
            'url': f'https://example.com/video_{quality}.mp4',
            'ext': 'mp4',
            'format_id': quality,
            'height': int(quality[:-1]),
        })

    return {
        'id': video_id,
        'title': title,
        'formats': formats,
    }
```

### 步骤 5: 处理特殊情况

#### 情况 1: M3U8/HLS 流

```python
def _real_extract(self, url):
    # ...
    m3u8_url = self._html_search_regex(r'["\'](https://[^"\']+\.m3u8[^"\']*)["\']', webpage, 'm3u8 url')

    formats = self._extract_m3u8_formats(
        m3u8_url, video_id,
        ext='mp4', entry_protocol='m3u8_native'
    )

    return {
        'id': video_id,
        'title': title,
        'formats': formats,
    }
```

#### 情况 2: DASH 流

```python
def _real_extract(self, url):
    # ...
    mpd_url = self._html_search_regex(r'<Dashboard[^>]+url="([^"]+)"', webpage, 'mpd url')

    formats = self._extract_mpd_formats(
        mpd_url, video_id,
        mpd_id='dash'
    )

    return {
        'id': video_id,
        'title': title,
        'formats': formats,
    }
```

#### 情况 3: 分离的视频和音频

```python
def _real_extract(self, url):
    # ...
    video_url = self._html_search_regex(r'"video":"([^"]+)"', webpage, 'video url')
    audio_url = self._html_search_regex(r'"audio":"([^"]+)"', webpage, 'audio url')

    formats = [
        {'url': video_url, 'format_id': 'video-only', 'vcodec': 'none'},
        {'url': audio_url, 'format_id': 'audio-only', 'acodec': 'none'},
    ]

    return {
        'id': video_id,
        'title': title,
        'formats': formats,
    }
```

#### 情况 4: 需要认证

```python
class MySiteIE(InfoExtractor):
    # ...

    def _perform_login(self, username, password):
        """实现登录逻辑"""
        login_url = 'https://www.mysite.com/login'

        # 获取登录页面
        login_page = self._download_webpage(login_url, None)

        # 提取 CSRF token
        csrf_token = self._html_search_regex(
            r'name="csrf_token"\s+value="([^"]+)"',
            login_page, 'csrf token'
        )

        # 提交登录
        login_form = {
            'username': username,
            'password': password,
            'csrf_token': csrf_token,
        }

        self._download_webpage(
            login_url, None,
            data=login_form,
            headers={'Referer': login_url}
        )

        # 验证登录成功
        # ...
```

### 步骤 6: 添加元数据

```python
def _real_extract(self, url):
    # ...

    return {
        'id': video_id,
        'title': title,
        'url': video_url,
        'ext': 'mp4',

        # 基础元数据
        'description': self._html_search_meta('description', webpage),
        'thumbnail': self._html_search_meta('og:image', webpage),
        'uploader': self._html_search_regex(
            r' uploader:\s*"([^"]+)"', webpage, 'uploader'
        ),
        'upload_date': self._html_search_regex(
            r'发布于\s+(\d{4}-\d{2}-\d{2})', webpage, 'upload_date'
        ),
        'duration': int(self._html_search_regex(
            r'duration:\s*(\d+)', webpage, 'duration'
        )),
        'view_count': int(self._html_search_regex(
            r'view_count:\s*(\d+)', webpage, 'view count'
        )),
        'like_count': int(self._html_search_regex(
            r'like_count:\s*(\d+)', webpage, 'like count'
        )),

        # 字幕
        'subtitles': self.extract_subtitles(video_id, webpage),

        # 格式
        'formats': formats,
    }
```

### 步骤 7: 提取字幕

```python
def _get_subtitles(self, video_id, webpage):
    """提取字幕"""
    subtitles = {}

    # 查找字幕 URL
    subtitle_url = self._html_search_regex(
        r'"subtitle"\s*:\s*"([^"]+)"', webpage, 'subtitle url', fatal=False
    )

    if subtitle_url:
        subtitles['en'] = [{
            'url': subtitle_url,
            'ext': 'vtt',
        }]

    return subtitles
```

### 步骤 8: 注册提取器

在 `yt_dlp/extractor/_extractors.py` 中注册：

```python
# _extractors.py

from .mysite import MySiteIE

# 在 _ALL_CLASSES 列表中添加
_ALL_CLASSES = [
    # ...
    MySiteIE,
]
```

### 步骤 9: 测试提取器

```bash
# 运行测试用例
yt-dlp -I "https://www.mysite.com/watch/abc123"

# 详细调试信息
yt-dlp -v --skip-download "URL"

# 只测试不下载
yt-dlp --skip-download --print "%(json)s" "URL"
```

### 步骤 10: 调试技巧

```python
# 保存网页内容用于调试
webpage = self._download_webpage(url, video_id)
self._save_webpage('debug_page.html', webpage)

# 打印调试信息
self._downloader.to_screen(f'DEBUG: {data}')

# 使用 pdb 断点
import pdb; pdb.set_trace()

# 使用 --write-pages 选项
# yt-dlp --write-pages URL
```

## 提取器最佳实践

### 规则 1: 始终包含测试用例

```python
_TESTS = [{
    'url': 'https://www.mysite.com/watch/test123',
    'md5': 'expected_hash',  # 预期文件哈希
    'info_dict': {
        'id': 'test123',
        'ext': 'mp4',
        'title': 'Test Video',
        'uploader': 'TestUser',
        'upload_date': '20250101',
        # ... 所有预期字段
    },
}]
```

### 规则 2: 优雅处理错误

```python
# 使用 fatal=False 允许失败
thumbnail = self._html_search_regex(
    r'og:image"\s+content="([^"]+)"', webpage,
    'thumbnail', fatal=False, default=None
)
```

### 规则 3: 使用合适的提取方法

```python
# 优先使用专用方法
title = self._html_search_meta('og:title', webpage)  # 最好
title = self._og_search_title(webpage)               # 好
title = self._html_search_regex(r'<h1>(.+?)</h1>', webpage, 'title')  # 通用
```

### 规则 4: 处理多种 URL 模式

```python
class MySiteIE(InfoExtractor):
    _VALID_URL = r'''(?x)
        https?://(?:www\.)?mysite\.com/
        (?:
            watch/(?P<id>[^/]+) |
            video/(?P<id2>[^/]+) |
            v/(?P<id3>[^/]+)
        )
    '''

    def _real_extract(self, url):
        # 统一 ID
        video_id = self._match_id(url) or self._match_id2(url) or self._match_id3(url)
        # ...
```

## 完整示例

参考模板文件: [templates/extractor-template.py](../templates/extractor-template.py)

## 下一步

- [提取器开发指南](../references/extractor-guide.md) - 详细 API 参考
- [调试工作流](debugging.md) - 调试和问题排查
- [架构参考](../references/architecture.md) - 深入理解架构
