import ffmpeg
import os
import sys
import argparse

def resize_blur_pad(
    input_path,
    output_path,
    text,
    out_w=1080,
    out_h=1920,
    font_path='arial.ttf',
    font_size=80,
    font_color='white',
):
    inp = ffmpeg.input(input_path)

    bg = (
        inp.video
        .filter('scale', out_w, out_h, force_original_aspect_ratio='increase')
        .filter('crop', out_w, out_h)
        .filter('gblur', sigma=20)
        .filter(
            'drawtext',
            text=text,
            fontfile=font_path,
            fontsize=font_size,
            fontcolor=font_color,
            borderw=4,
            bordercolor='black',
            x='(w-text_w)/2',
            y='500',
        )
    )

    fg = (
        inp.video
        .filter('scale', out_w, out_h, force_original_aspect_ratio='decrease')
    )

    out = ffmpeg.overlay(bg, fg, x='(W-w)/2', y='(H-h)/2')

    (
        ffmpeg
        .output(out, inp.audio, output_path, vcodec='libx264', crf=18, preset='fast', acodec='aac')
        .overwrite_output()
        .run()
    )

def main():
    parser = argparse.ArgumentParser(
        prog='ReelsResizer',
        description='Resizes a video to 9:16 with a blurred background and overlays text',
    )
    parser.add_argument('input_path', help='Path to the source video (e.g. input.mp4)')
    parser.add_argument('output_path', help='Path to write the resized video (e.g. output_916_blur.mp4)')
    parser.add_argument('text', help='Text to overlay on the video')
    parser.add_argument('--out-w', type=int, default=1080, help='Output width (default: 1080)')
    parser.add_argument('--out-h', type=int, default=1920, help='Output height (default: 1920)')
    parser.add_argument('--font-path', default='arial.ttf', help='Path to a .ttf/.otf font file')
    parser.add_argument('--font-size', type=int, default=80, help='Font size in px (default: 80)')
    parser.add_argument('--font-color', default='white', help='Font color, e.g. white, red, #FFAA00')

    args = parser.parse_args()

    if not args.input_path.lower().endswith(('.mp4', '.mov', '.mkv', '.avi')):
        print(f"ERROR: input path '{args.input_path}' doesn't look like a video file!")
        sys.exit(1)

    if not os.path.exists(args.input_path):
        print(f"ERROR: input file '{args.input_path}' not found!")
        sys.exit(1)

    if not os.path.exists(args.font_path):
        print(f"ERROR: font file '{args.font_path}' not found!")
        sys.exit(1)

    try:
        resize_blur_pad(
            args.input_path,
            args.output_path,
            args.text,
            out_w=args.out_w,
            out_h=args.out_h,
            font_path=args.font_path,
            font_size=args.font_size,
            font_color=args.font_color,
        )
    except ffmpeg.Error as e:
        print(e.stderr.decode())
        sys.exit(1)

    print(f"Done! Wrote {args.output_path}")


if __name__ == '__main__':
    main()