# 架构设计参考

## 概述

yt-dlp 采用模块化架构，主要组件包括提取器系统、下载器、后处理器和核心引擎。

## 核心组件

### YoutubeDL 类

位置: `yt_dlp/YoutubeDL.py`

核心下载引擎，负责协调所有组件：

```python
class YoutubeDL:
    """主类"""

    def __init__(self, params=None):
        """初始化，解析参数"""
        self.params = params or {}

    def download(self, url_list):
        """下载 URL 列表"""
        for url in url_list:
            self.extract_info(url, download=True)

    def extract_info(self, url, download=True):
        """提取信息并可选下载"""
        # 1. 匹配提取器
        ie = self.get_info_extractor(url)

        # 2. 提取信息
        info = ie.extract(url)

        # 3. 格式选择
        info = self._format_selection(info)

        # 4. 后处理
        if download:
            self.process_info(info)

        return info
```

### 提取器系统

位置: `yt_dlp/extractor/`

#### InfoExtractor 基类

所有提取器的基类：

```python
class InfoExtractor:
    """提取器基类"""

    # 类属性
    IE_DESC = 'Extractor name'
    IE_NAME = 'extractor'
    _VALID_URL = r'https?://example\.com/watch/(?P<id>[^/]+)'

    # 核心方法
    def suitable(self, url):
        """检查 URL 是否匹配此提取器"""
        return re.match(self._VALID_URL, url) is not None

    def _real_extract(self, url):
        """子类必须实现：提取视频信息"""
        raise NotImplementedError('This method must be implemented by subclasses')

    def extract(self, url):
        """提取入口"""
        # 验证 URL
        if not self.suitable(url):
            return None

        # 调用子类实现
        return self._real_extract(url)
```

#### 通用提取器

| 提取器 | 用途 |
|--------|------|
| `common.IE` | 通用基类 |
| `generic.IE` | 通用提取器（匹配所有 URL） |
| `search.IE` | 搜索结果 |
| `youtube.IE` | YouTube 视频/频道/播放列表 |

#### 提取器注册

位置: `yt_dlp/extractor/_extractors.py`

```python
# 导入所有提取器
from .youtube import YoutubeIE
from .bilibili import BilibiliIE
# ...

# 注册
_ALL_CLASSES = [
    YoutubeIE,
    BilibiliIE,
    # ...
]
```

### 下载器系统

位置: `yt_dlp/downloader/`

| 下载器 | 协议 | 用途 |
|--------|------|------|
| `http.HttpFD` | HTTP/HTTPS | 基础下载 |
| `hls.HlsFD` | HLS | m3u8 流媒体 |
| `dash.DashFD` | DASH | MPD 流媒体 |
| `rtmp.RtmpFD` | RTMP | 老式流协议 |
| `external.ExternalFD` | 外部 | aria2, curl, wget |

```python
class HttpFD:
    """HTTP 下载器"""

    def download(self, filename, url):
        """下载文件到 filename"""
        # 实现分块下载、断点续传、重试等
        pass
```

### 后处理器系统

位置: `yt_dlp/postprocessor/`

```python
class PostProcessor:
    """后处理器基类"""

    def run(self, information):
        """
        处理信息字典

        Args:
            information: 包含 filepath, title 等的字典

        Returns:
            ([info], []): 处理后的信息列表和需要重新处理的文件列表
        """
        raise NotImplementedError()
```

#### 内置后处理器

| 后处理器 | 功能 |
|----------|------|
| `FFmpegVideoConvertor` | 视频格式转换 |
| `FFmpegExtractAudio` | 音频提取 |
| `FFmpegMetadata` | 元数据嵌入 |
| `FFmpegEmbedSubtitle` | 字幕嵌入 |
| `EmbedThumbnail` | 缩略图嵌入 |
| `SponsorBlock` | 移除赞助片段 |
| `XAttrPP` | 扩展属性设置 |

## 数据流

### 完整下载流程

```
URL
  ↓
[1] URL 解析和提取器匹配
  ↓
[2] InfoExtractor._real_extract()
  ↓
[3] 返回 info_dict {
       id, title, formats,
       subtitles, thumbnail, ...
     }
  ↓
[4] 格式选择 (format_selector)
  ↓
[5] 下载器下载 (downloader)
  ↓
[6] 后处理器链 (postprocessors)
  ↓
最终文件
```

### info_dict 结构

```python
info = {
    # 必需字段
    'id': 'video_id',
    'title': '视频标题',

    # 格式列表
    'formats': [
        {
            'url': 'https://...',
            'ext': 'mp4',
            'height': 1080,
            'width': 1920,
            'fps': 30,
            'vcodec': 'h264',
            'acodec': 'none',  # video only
        },
        {
            'url': 'https://...',
            'ext': 'm4a',
            'acodec': 'aac',
            'vcodec': 'none',  # audio only
        }
    ],

    # 元数据
    'description': '视频描述',
    'uploader': '上传者',
    'uploader_id': 'user123',
    'upload_date': '20250128',
    'duration': 600,  # 秒
    'view_count': 1000000,
    'like_count': 50000,

    # 媒体
    'thumbnail': 'https://...',
    'subtitles': {
        'en': [{'url': '...', 'ext': 'vtt'}],
        'zh': [{'url': '...', 'ext': 'vtt'}],
    },

    # 其他
    'webpage_url': 'https://...',
    'extractor': 'youtube',
    'extractor_key': 'Youtube',
}
```

## 格式选择器

位置: `yt_dlp/utils.py`

```python
def build_format_selector(filter_spec):
    """构建格式选择器"""

    # 解析选择字符串
    # "bestvideo[height<=1080]+bestaudio"

    # 返回选择函数
    def selector(formats):
        # 过滤
        filtered = [f for f in formats if match_filter(f, filter_spec)]

        # 排序
        sorted_formats = sorted(filtered, key=key_func)

        return sorted_formats[0]  # 返回最佳

    return selector
```

## 缓存系统

位置: `yt_dlp/cache.py`

```python
class Cache:
    """缓存管理"""

    def get(self, key):
        """获取缓存"""

    def set(self, key, value):
        """设置缓存"""

    def remove(self, key):
        """删除缓存"""
```

缓存用途:
- 网页内容（避免重复下载）
- 提取器结果
- 格式信息

## 插件系统

位置: `yt_dlp/plugins/`

```python
# 用户自定义提取器
# ~/.local/share/yt-dlp/plugins/extractor/mysite.py

class MySiteIE(InfoExtractor):
    _VALID_URL = r'https?://mysite\.com/watch/(?P<id>[^/]+)'

    def _real_extract(self, url):
        # 自定义提取逻辑
        pass
```

## 配置系统

### 配置文件优先级

```
1. 命令行参数
2. 便携配置: ./yt-dlp.conf
3. 用户配置: ~/.config/yt-dlp/yt-dlp.conf
4. 系统配置: /etc/yt-dlp.conf
```

### 配置解析

位置: `yt_dlp/options.py`

```python
def parseOpts(overrideArguments=None):
    """解析命令行选项"""

    parser = create_parser()
    opts = parser.parse_args()

    # 加载配置文件
    load_config_files(opts)

    return opts
```

## 网络层

位置: `yt_dlp/networking/`

```python
class Request:
    """HTTP 请求封装"""

    def __init__(self, url, headers=None, data=None):
        self.url = url
        self.headers = headers
        self.data = data

class RequestHandler:
    """请求处理器"""

    def send(self, request):
        """发送请求，返回响应"""
        # 实现重试、代理、超时等
        pass
```

## 工具函数

位置: `yt_dlp/utils/`

| 模块 | 功能 |
|------|------|
| `utils.py` | 通用工具函数 |
| `traversal.py` | 树遍历 |
| `html.py` | HTML 解析 |
| `jsinterp.py` | JavaScript 解释器 |
| `regex.py` | 正则工具 |
| `datetime.py` | 日期时间处理 |
| `soup.py` | BeautifulSoup 封装 |

## 设计模式

### 1. 策略模式 - 提取器

```python
# 不同网站使用不同提取器
class YoutubeIE(InfoExtractor): pass
class BilibiliIE(InfoExtractor): pass

# 运行时选择
ie = get_info_extractor(url)
info = ie.extract(url)
```

### 2. 责任链模式 - 后处理器

```python
# 后处理器按顺序执行
pp1 = FFmpegVideoConvertor(ydl)
pp2 = FFmpegMetadata(ydl)

info = pp1.run(info)
info = pp2.run(info)
```

### 3. 工厂模式 - 下载器

```python
def get_downloader(url, params):
    """根据 URL 创建下载器"""
    if '.m3u8' in url:
        return HlsFD(params)
    elif '.mpd' in url:
        return DashFD(params)
    else:
        return HttpFD(params)
```

### 4. 单例模式 - YoutubeDL

```python
# 通常一个实例处理所有下载
ydl = YoutubeDL(params)
ydl.download(urls)
```

## 扩展点

### 添加提取器

```python
# 1. 创建 yt_dlp/extractor/mysite.py
class MySiteIE(InfoExtractor):
    _VALID_URL = r'https?://mysite\.com/...'

    def _real_extract(self, url):
        # ...

# 2. 在 _extractors.py 注册
from .mysite import MySiteIE
_ALL_CLASSES.append(MySiteIE)
```

### 添加后处理器

```python
# 1. 创建 yt_dlp/postprocessor/mypp.py
class MyPP(PostProcessor):
    def run(self, info):
        # ...

# 2. 在 __init__.py 导出
from .mypp import MyPP
```

### 添加下载器

```python
# 1. 创建 yt_dlp/downloader/mydownloader.py
class MyDownloader:
    def download(self, filename, url):
        # ...

# 2. 在下载器工厂中注册
```

## 性能考虑

### 懒惰加载

```python
# 提取器延迟加载以减少启动时间
def get_info_extractor(name):
    if name not in _LOADED_EXTRACTORS:
        _LOADED_EXTRACTORS[name] = _import_extractor(name)
    return _LOADED_EXTRACTORS[name]
```

### 并发下载

```bash
# 使用 aria2 多线程下载
yt-dlp --external-downloader aria2 \
       --external-downloader-args "-x 16 -k 1M"
```

### 缓存策略

```python
# 智能缓存失效
cache.set(key, value, expire=3600)  # 1小时
```

## 安全考虑

### 输入验证

```python
# 验证 URL
if not re.match(_VALID_URL, url):
    return None

# 验证文件路径
filepath = sanitize_path(filepath)
```

### 凭据保护

```python
# 不在日志中显示密码
password = '***' if log_sensitive else password
```

## 参考资料

- [Python API 参考](api-reference.md)
- [提取器开发指南](extractor-guide.md)
- [格式选择器参考](format-selector.md)
- [后处理器参考](postprocessors.md)
