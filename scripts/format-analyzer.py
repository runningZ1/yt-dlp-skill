#!/usr/bin/env python3
"""
格式分析工具

分析视频的可用格式，帮助选择最佳下载选项
"""

import argparse
import json
import sys

try:
    import yt_dlp
except ImportError:
    print("错误: 需要安装 yt-dlp")
    print("请运行: pip install yt-dlp")
    sys.exit(1)


def format_size(size):
    """格式化文件大小"""
    if not size:
        return "N/A"
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f}{unit}"
        size /= 1024.0
    return f"{size:.1f}TB"


def analyze_formats(url, verbose=False):
    """分析视频格式"""
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            print(f"\n标题: {info.get('title', 'N/A')}")
            print(f"上传者: {info.get('uploader', 'N/A')}")
            print(f"时长: {info.get('duration_string', 'N/A')}")
            print(f"观看次数: {info.get('view_count', 'N/A')}")
            print("\n" + "=" * 100)

            formats = info.get('formats', [])
            if not formats:
                print("没有找到可用格式")
                return

            # 按格式分组
            video_only = []
            audio_only = []
            combined = []

            for f in formats:
                vcodec = f.get('vcodec', 'none')
                acodec = f.get('acodec', 'none')

                if vcodec == 'none' and acodec != 'none':
                    audio_only.append(f)
                elif acodec == 'none' and vcodec != 'none':
                    video_only.append(f)
                else:
                    combined.append(f)

            # 显示格式
            print("\n【已合并视频+音频】\n")
            if combined:
                print_format_table(combined, verbose)
            else:
                print("无")

            print("\n【仅视频】\n")
            if video_only:
                print_format_table(video_only, verbose)
            else:
                print("无")

            print("\n【仅音频】\n")
            if audio_only:
                print_format_table(audio_only, verbose)
            else:
                print("无")

            # 推荐格式
            print("\n" + "=" * 100)
            print("\n【推荐格式】\n")
            print_recommendations(video_only, audio_only, combined)

            # 格式选择命令
            print("\n" + "=" * 100)
            print("\n【格式选择命令示例】\n")
            print_command_examples(info)

    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)


def print_format_table(formats, verbose):
    """打印格式表格"""
    # 排序：按高度降序
    formats = sorted(formats, key=lambda f: f.get('height', 0), reverse=True)

    if verbose:
        print(f"{'ID':<12} {'扩展名':<6} {'分辨率':<10} {'帧率':<6} {'文件大小':<10} {'比特率':<12} {'编解码器'}")
        print("-" * 100)

        for f in formats[:20]:  # 只显示前 20 个
            format_id = f.get('format_id', 'N/A')
            ext = f.get('ext', 'N/A')
            height = f.get('height', 'N/A')
            width = f.get('width', 'N/A')
            resolution = f"{width}x{height}" if width and height else f"{height}p" if height else "N/A"
            fps = f.get('fps', 'N/A')
            filesize = format_size(f.get('filesize'))
            vbr = f"{f.get('vbr', 'N/A')}k" if f.get('vbr') else "N/A"
            abr = f"{f.get('abr', 'N/A')}k" if f.get('abr') else "N/A"
            vcodec = f.get('vcodec', 'N/A')
            acodec = f.get('acodec', 'N/A')

            print(f"{format_id:<12} {ext:<6} {resolution:<10} {fps:<6} {filesize:<10} {vbr:>6}/{abr:<6} {vcodec} / {acodec}")
    else:
        print(f"{'ID':<8} {'扩展名':<6} {'分辨率':<10} {'文件大小':<10} {'备注'}")
        print("-" * 70)

        for f in formats[:15]:
            format_id = f.get('format_id', 'N/A')
            ext = f.get('ext', 'N/A')
            height = f.get('height', 'N/A')
            width = f.get('width', 'N/A')
            resolution = f"{width}x{height}" if width and height else f"{height}p" if height else "audio"
            filesize = format_size(f.get('filesize'))
            note = f.get('format_note', '')

            print(f"{format_id:<8} {ext:<6} {resolution:<10} {filesize:<10} {note}")

    if len(formats) > (20 if verbose else 15):
        print(f"\n... 还有 {len(formats) - (20 if verbose else 15)} 个格式")


def print_recommendations(video_only, audio_only, combined):
    """打印推荐格式"""

    # 最佳 1080p
    best_1080p = None
    for f in video_only:
        if f.get('height') == 1080:
            best_1080p = f
            break

    if best_1080p:
        audio = max(audio_only, key=lambda x: x.get('abr', 0)) if audio_only else None
        if audio:
            print(f"1080p: -f {best_1080p['format_id']}+{audio['format_id']}")
            print(f"       文件大小约: {format_size(best_1080p.get('filesize') + audio.get('filesize'))}")

    # 最佳 720p
    best_720p = None
    for f in video_only:
        if f.get('height') == 720:
            best_720p = f
            break

    if best_720p:
        audio = max(audio_only, key=lambda x: x.get('abr', 0)) if audio_only else None
        if audio:
            print(f"720p:  -f {best_720p['format_id']}+{audio['format_id']}")
            print(f"       文件大小约: {format_size(best_720p.get('filesize') + audio.get('filesize'))}")

    # 最佳 MP4（兼容性好）
    best_mp4 = None
    for f in combined:
        if f.get('ext') == 'mp4':
            if not best_mp4 or (f.get('height') and f.get('height') > best_mp4.get('height', 0)):
                best_mp4 = f

    if best_mp4:
        print(f"MP4:   -f {best_mp4['format_id']}")
        print(f"       文件大小约: {format_size(best_mp4.get('filesize'))}")

    # 最佳音频
    if audio_only:
        best_audio = max(audio_only, key=lambda x: x.get('abr', 0))
        print(f"音频:  -f {best_audio['format_id']}")
        print(f"       比特率: {best_audio.get('abr')}k")


def print_command_examples(info):
    """打印命令示例"""
    title = info.get('title', 'video')

    print(f"# 下载最佳质量")
    print(f'yt-dlp -f "bestvideo+bestaudio" "{info["webpage_url"]}"')

    print(f"\n# 下载 1080p 或以下最佳 MP4")
    print(f'yt-dlp -f "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" "{info["webpage_url"]}"')

    print(f"\n# 只下载音频（MP3）")
    print(f'yt-dlp -x --audio-format mp3 "{info["webpage_url"]}"')

    print(f"\n# 下载字幕")
    print(f'yt-dlp --write-subs --sub-lang en "{info["webpage_url"]}"')

    print(f"\n# 查看更多信息")
    print(f'yt-dlp --print "%(title)s\\n%(uploader)s\\n%(duration)s" "{info["webpage_url"]}"')


def main():
    parser = argparse.ArgumentParser(
        description='分析视频的可用格式',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 分析单个视频
  python format_analyzer.py https://www.youtube.com/watch?v=xxx

  # 详细输出
  python format_analyzer.py -v https://www.youtube.com/watch?v=xxx

  # 从文件读取 URL
  python format_analyzer.py -f urls.txt
        """
    )

    parser.add_argument(
        'url',
        nargs='?',
        help='视频 URL'
    )

    parser.add_argument(
        '-f', '--file',
        help='包含 URL 的文件'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='详细输出'
    )

    args = parser.parse_args()

    urls = []

    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    urls.append(line)

    if args.url:
        urls.append(args.url)

    if not urls:
        print("错误: 没有提供 URL")
        sys.exit(1)

    for url in urls:
        analyze_formats(url, args.verbose)
        if len(urls) > 1:
            print("\n" + "=" * 100 + "\n")


if __name__ == '__main__':
    main()
