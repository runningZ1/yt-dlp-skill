# 后处理器开发工作流

## 目标

为 yt-dlp 编写自定义后处理器，扩展视频处理功能。

## 前置条件

- [ ] 熟悉 Python 编程
- [ ] 了解 FFmpeg 基础
- [ ] 已阅读 [后处理器参考](../references/postprocessors.md)

## 步骤

### 步骤 1: 了解后处理器架构

后处理器在 `yt_dlp/postprocessor/` 目录中：

```
postprocessor/
├── __init__.py
├── common.py              # 基类
├── ffmpeg.py              # FFmpeg 相关
├── metadata.py            # 元数据处理
├── embedsubtitle.py       # 字幕嵌入
└── ...
```

### 步骤 2: 后处理器基类

```python
from yt_dlp.postprocessor.common import PostProcessor

class MyPostProcessor(PostProcessor):
    """自定义后处理器"""

    def __init__(self, downloader=None, option1=None, option2=None):
        # 初始化参数
        super().__init__(downloader)
        self.option1 = option1
        self.option2 = option2

    def run(self, information):
        """
        处理主方法

        Args:
            information: 包含视频信息的字典

        Returns:
            tuple: (information列表, 需要再次处理的文件列表)
        """
        filepath = information['filepath']

        # 处理文件
        self.to_screen(f'Processing: {filepath}')

        # 处理逻辑...

        return [information], []
```

### 步骤 3: 创建简单后处理器

```python
# yt_dlp/postprocessor/mypostprocessor.py

import os
from yt_dlp.postprocessor.common import PostProcessor
from yt_dlp.utils import (
    encodeArgument,
    encodeFilename,
)


class WatermarkPP(PostProcessor):
    """添加水印后处理器"""

    def __init__(self, downloader=None, watermark_image=None, position='bottom-right'):
        super().__init__(downloader)
        self.watermark_image = watermark_image
        self.position = position

    def run(self, information):
        filepath = information['filepath']
        filename = os.path.basename(filepath)

        if not self.watermark_image or not os.path.exists(self.watermark_image):
            self.to_screen('Watermark image not found, skipping')
            return [information], []

        # 生成输出文件名
        outfile = filepath.replace('.mp4', '_watermarked.mp4')

        # 构建 FFmpeg 命令
        cmd = [
            'ffmpeg',
            '-i', filepath,
            '-i', self.watermark_image,
            '-filter_complex',
            f'[0:v][1:v]overlay={self._get_overlay_position()}[out]',
            '-map', '[out]',
            '-map', '0:a?',  # 保留音频流
            '-c:a', 'copy',  # 音频不重新编码
            outfile
        ]

        self.to_screen(f'Adding watermark to {filename}')

        # 执行命令
        self.write_debug('Executing command: ' + ' '.join(cmd))
        retval = self.run_ffmpeg(cmd)

        if retval != 0:
            raise PostProcessingError('ffmpeg failed to add watermark')

        # 更新信息
        information['filepath'] = outfile
        information['ext'] = 'mp4'

        return [information], []

    def _get_overlay_position(self):
        """转换位置为 FFmpeg overlay 语法"""
        positions = {
            'top-left': '10:10',
            'top-right': 'W-w-10:10',
            'bottom-left': '10:H-h-10',
            'bottom-right': 'W-w-10:H-h-10',
            'center': '(W-w)/2:(H-h)/2',
        }
        return positions.get(self.position, 'W-w-10:H-h-10')
```

### 步骤 4: FFmpeg 后处理器

```python
from yt_dlp.postprocessor.ffmpeg import (
    FFmpegPostProcessor,
    FFmpegVideoConvertorPP,
)


class MyFFmpegPP(FFmpegPostProcessor):
    """使用 FFmpeg 的后处理器基类"""

    def __init__(self, downloader=None, custom_option=None):
        super().__init__(downloader)
        self.custom_option = custom_option

    def run(self, information):
        filepath = information['filepath']

        # 获取视频信息
        info = self.get_audio_information(filepath)
        self.to_screen(f'Audio codec: {info.get("codec")}')

        # 使用 FFmpeg 处理
        options = {
            'custom_option': self.custom_option,
        }

        # 调用父类方法
        return super().run(information)
```

### 步骤 5: 元数据后处理器

```python
from yt_dlp.postprocessor.metadata import (
    MetadataFromFieldPP,
    MetadataParserPP,
)


class CustomMetadataPP(PostProcessor):
    """自定义元数据处理"""

    def run(self, information):
        # 添加自定义字段
        information['custom_field'] = 'custom_value'

        # 修改现有字段
        information['title'] = f"[PREFIX] {information['title']}"

        # 解析格式化的元数据
        # information['description'] = self._parse_description(information)

        self.to_screen('Updated metadata')

        return [information], []
```

### 步骤 6: 注册后处理器

在 `yt_dlp/postprocessor/__init__.py` 中注册：

```python
from .mypostprocessor import WatermarkPP, CustomMetadataPP

# 导出列表
__all__ = [
    # ...
    'WatermarkPP',
    'CustomMetadataPP',
]
```

### 步骤 7: 使用后处理器

#### 命令行

```bash
# 内置后处理器
yt-dlp --embed-metadata --embed-subs "URL"

# 自定义后处理器（需要修改代码或使用配置）
```

#### Python API

```python
import yt_dlp
from yt_dlp.postprocessor.mypostprocessor import WatermarkPP

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
        # 自定义后处理器需要直接添加到处理链
    ],
}

# 手动添加自定义后处理器
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    # 添加自定义 PP
    pp = WatermarkPP(ydl, watermark_image='watermark.png')
    ydl.add_post_processor(pp)

    ydl.download(['URL'])
```

### 步骤 8: 后处理器链

后处理器按顺序执行：

```python
ydl_opts = {
    'postprocessors': [
        # 1. 转换视频
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

## 内置后处理器参考

### FFmpegVideoConvertor

```python
{
    'key': 'FFmpegVideoConvertor',
    'preferedformat': 'mp4',  # 目标格式
}
```

### FFmpegExtractAudio

```python
{
    'key': 'FFmpegExtractAudio',
    'preferredcodec': 'mp3',
    'preferredquality': '0',  # 0=best, 9=worst
}
```

### FFmpegMetadata

```python
{
    'key': 'FFmpegMetadata',
    'add_metadata': True,
}
```

### FFmpegEmbedSubtitle

```python
{
    'key': 'FFmpegEmbedSubtitle',
    'subtitlesformat': 'srt',
}
```

### EmbedThumbnail

```python
{
    'key': 'EmbedThumbnail',
    'already_have_thumbnail': False,
}
```

### MetadataFromField

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

```python
{
    'key': 'SponsorBlock',
    'categories': ['sponsor', 'intro', 'outro', 'selfpromo'],
}
```

## 实用后处理器示例

### 示例 1: 视频旋转

```python
class RotateVideoPP(FFmpegPostProcessor):
    """旋转视频"""

    def __init__(self, downloader=None, degrees=90):
        super().__init__(downloader)
        self.degrees = degrees

    def run(self, information):
        filepath = information['filepath']

        # FFmpeg 旋转滤镜
        # 90度: transpose=1
        # 180度: transpose=1,transpose=1
        # 270度: transpose=2
        transpose_map = {90: 1, 180: '1,1', 270: 2}

        cmd = [
            'ffmpeg', '-i', filepath,
            '-vf', f'transpose={transpose_map.get(self.degrees, 1)}',
            '-a', 'copy',
            self._ffmpeg_filename_extension(filepath, 'mp4')
        ]

        return self.run_ffmpeg(cmd, information)
```

### 示例 2: 视频裁剪

```python
class CropVideoPP(FFmpegPostProcessor):
    """裁剪视频"""

    def __init__(self, downloader=None, crop=None):
        super().__init__(downloader)
        self.crop = crop  # "w:h:x:y"

    def run(self, information):
        filepath = information['filepath']

        cmd = [
            'ffmpeg', '-i', filepath,
            '-vf', f'crop={self.crop}',
            '-c:a', 'copy',
            self._ffmpeg_filename_extension(filepath, 'mp4')
        ]

        return self.run_ffmpeg(cmd, information)
```

### 示例 3: 添加音频

```python
class AddAudioPP(FFmpegPostProcessor):
    """添加背景音乐"""

    def __init__(self, downloader=None, audio_file=None, volume=0.5):
        super().__init__(downloader)
        self.audio_file = audio_file
        self.volume = volume

    def run(self, information):
        filepath = information['filepath']

        cmd = [
            'ffmpeg',
            '-i', filepath,
            '-i', self.audio_file,
            '-filter_complex',
            f'[0:a][1:a]amix=inputs=2:duration=first:weights=1 {self.volume}[aout]',
            '-map', '0:v',
            '-map', '[aout]',
            '-c:v', 'copy',
            self._ffmpeg_filename_extension(filepath, 'mp4')
        ]

        return self.run_ffmpeg(cmd, information)
```

## 后处理器最佳实践

### 规则 1: 优雅处理失败

```python
def run(self, information):
    try:
        # 处理逻辑
        pass
    except Exception as e:
        self.report_warning(f'Processing failed: {e}')
        return [information], []  # 返回原信息，不中断
```

### 规则 2: 检查前置条件

```python
def run(self, information):
    filepath = information.get('filepath')
    if not filepath or not os.path.exists(filepath):
        self.to_screen('File not found, skipping')
        return [information], []
```

### 规则 3: 更新信息字典

```python
def run(self, information):
    # 处理后更新文件路径
    information['filepath'] = new_filepath

    # 更新其他字段
    information['ext'] = 'mp4'
    information['filesize'] = os.path.getsize(new_filepath)

    return [information], []
```

### 规则 4: 提供清晰日志

```python
self.to_screen(f'Processing {filename}')
self.write_debug(f'Command: {cmd}')
self.report_warning(f'Using fallback method')
self.report_error(f'Processing failed')
```

## 调试后处理器

```bash
# 使用 -v 查看详细日志
yt-dlp -v --embed-metadata "URL"

# 只运行后处理器（不下载）
yt-dlp --skip-download --postprocessor-args "args" "URL"

# 测试单个后处理器
python -c "
from yt_dlp import YoutubeDL
from yt_dlp.postprocessor.mypostprocessor import MyPP
ydl = YoutubeDL({'verbose': True})
pp = MyPP(ydl)
pp.run({'filepath': 'test.mp4', 'title': 'Test'})
"
```

## 下一步

- [后处理器参考](../references/postprocessors.md) - 完整 API 文档
- [提取器开发工作流](extractor-development.md) - 开发提取器
- [调试工作流](debugging.md) - 调试和问题排查
