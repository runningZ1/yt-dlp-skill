#!/usr/bin/env python3
"""
批量下载脚本

从文件中读取 URL 列表并批量下载视频
"""

import argparse
import sys
from pathlib import Path

try:
    import yt_dlp
except ImportError:
    print("错误: 需要安装 yt-dlp")
    print("请运行: pip install yt-dlp")
    sys.exit(1)


def read_urls_from_file(file_path):
    """从文件读取 URL 列表"""
    urls = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # 跳过空行和注释
            if line and not line.startswith('#'):
                urls.append(line)
    return urls


def batch_download(urls, output_dir='downloads', options=None):
    """
    批量下载视频

    Args:
        urls: URL 列表
        output_dir: 输出目录
        options: 额外的 yt-dlp 选项
    """
    ydl_opts = {
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'ignoreerrors': True,  # 失败继续
        'no_warnings': False,
    }

    # 合并用户选项
    if options:
        ydl_opts.update(options)

    success_count = 0
    fail_count = 0

    print(f"开始批量下载，共 {len(urls)} 个视频")
    print(f"输出目录: {output_dir}")
    print("-" * 60)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for i, url in enumerate(urls, 1):
            print(f"\n[{i}/{len(urls)}] 下载: {url}")

            try:
                ydl.download([url])
                success_count += 1
                print(f"✓ 成功")
            except Exception as e:
                fail_count += 1
                print(f"✗ 失败: {e}")

    print("\n" + "=" * 60)
    print(f"下载完成！成功: {success_count}, 失败: {fail_count}")


def main():
    parser = argparse.ArgumentParser(
        description='从 URL 列表批量下载视频',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 从文件下载
  python batch_download.py -f urls.txt

  # 指定输出目录
  python batch_download.py -f urls.txt -o videos/

  # 使用特定格式
  python batch_download.py -f urls.txt -f "bestvideo+bestaudio"

  # 直接提供 URL
  python batch_download.py https://www.youtube.com/watch?v=xxx https://www.youtube.com/watch?v=yyy

URL 文件格式:
  # 每行一个 URL
  https://www.youtube.com/watch?v=xxx
  https://www.youtube.com/watch?v=yyy
  # 空行和以 # 开头的行会被忽略
        """
    )

    parser.add_argument(
        '-f', '--file',
        help='包含 URL 列表的文件'
    )

    parser.add_argument(
        '-o', '--output-dir',
        default='downloads',
        help='输出目录 (默认: downloads)'
    )

    parser.add_argument(
        '-F', '--format',
        help='视频格式选择 (例如: bestvideo+bestaudio)'
    )

    parser.add_argument(
        '-x', '--extract-audio',
        action='store_true',
        help='只提取音频'
    )

    parser.add_argument(
        '--audio-format',
        default='mp3',
        help='音频格式 (默认: mp3)'
    )

    parser.add_argument(
        '--write-subs',
        action='store_true',
        help='下载字幕'
    )

    parser.add_argument(
        '--embed-subs',
        action='store_true',
        help='嵌入字幕到视频'
    )

    parser.add_argument(
        '--embed-metadata',
        action='store_true',
        help='嵌入元数据'
    )

    parser.add_argument(
        '--playlist-items',
        help='播放列表项范围 (例如: 1-5,10)'
    )

    parser.add_argument(
        'urls',
        nargs='*',
        help='直接提供 URL（可选）'
    )

    args = parser.parse_args()

    # 收集 URL
    urls = []

    if args.file:
        if not Path(args.file).exists():
            print(f"错误: 文件不存在: {args.file}")
            sys.exit(1)
        urls.extend(read_urls_from_file(args.file))

    if args.urls:
        urls.extend(args.urls)

    if not urls:
        print("错误: 没有提供 URL")
        print("请使用 -f 指定 URL 文件或直接提供 URL")
        sys.exit(1)

    # 构建选项
    options = {}

    if args.format:
        options['format'] = args.format

    if args.extract_audio:
        options['format'] = 'bestaudio'
        options['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': args.audio_format,
            'preferredquality': '0',
        }]

    if args.write_subs:
        options['writesubtitles'] = True
        options['subtitleslangs'] = ['en']

    if args.embed_subs:
        options['postprocessors'] = options.get('postprocessors', [])
        options['postprocessors'].append({
            'key': 'FFmpegEmbedSubtitle'
        })

    if args.embed_metadata:
        options['postprocessors'] = options.get('postprocessors', [])
        options['postprocessors'].append({
            'key': 'FFmpegMetadata'
        })

    if args.playlist_items:
        options['playlist_items'] = args.playlist_items

    # 创建输出目录
    Path(args.output_dir).mkdir(parents=True, exist_ok=True)

    # 开始下载
    batch_download(urls, args.output_dir, options)


if __name__ == '__main__':
    main()
