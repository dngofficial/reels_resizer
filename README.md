# Reels Resizer

Converts a video to 9:16 (1080x1920) with a blurred, padded background and
overlaid text — ready for TikTok/Reels/Shorts.

## Prerequisites

1. **Python 3.8+**
   Check with:
   ```
   python --version
   ```

2. **FFmpeg** (the actual binary, not just the Python wrapper)
   This script calls out to the `ffmpeg` command-line tool, so it must be
   installed and available on your system PATH.

   - **Windows**: Download from https://www.gyan.dev/ffmpeg/builds/ (get the
     "release essentials" build), unzip it, and add the `bin` folder to your
     PATH environment variable.
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt install ffmpeg` (Debian/Ubuntu) or your distro's
     equivalent

   Verify it's installed correctly:
   ```
   ffmpeg -version
   ```

3. **A font file** (`.ttf` or `.otf`)
   By default the script looks for `arial.ttf` in the current
   directory. Place your font file in the project folder, or pass a custom
   path with `--font-path`.

## Installation

1. Clone or download this repo, then move into the folder:
   ```
   cd deltarune_capcutter
   ```

2. (Recommended) Create and activate a virtual environment:
   ```
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

   If you don't have a `requirements.txt` yet, create one with:
   ```
   pip install ffmpeg-python
   pip freeze > requirements.txt
   ```

## Usage

Basic usage:
```
python video_editor.py input.mp4 output.mp4 "Your caption here"
```

With options:
```
python video_editor.py input.mp4 output.mp4 "Your caption here" ^
    --font-path "C:/Fonts/8bitoperator_jve.ttf" ^
    --font-size 100 ^
    --font-color yellow ^
    --out-w 1080 ^
    --out-h 1920
```
*(use `\` instead of `^` for line continuation on macOS/Linux)*

### Arguments

| Argument       | Required | Description                                      |
|----------------|----------|---------------------------------------------------|
| `input_path`   | Yes      | Path to the source video                          |
| `output_path`  | Yes      | Path to write the resized video                   |
| `text`         | Yes      | Caption text to overlay                            |
| `--out-w`      | No       | Output width (default: 1080)                      |
| `--out-h`      | No       | Output height (default: 1920)                     |
| `--font-path`  | No       | Path to a `.ttf`/`.otf` font (default: `8bitoperator_jve.ttf`) |
| `--font-size`  | No       | Font size in px (default: 80)                      |
| `--font-color` | No       | Font color name or hex, e.g. `white`, `#FFAA00`    |

Run `python video_editor.py -h` at any time to see this in the terminal.

## Troubleshooting

- **`ffmpeg._run.Error: ffmpeg error`** — re-run with the script as-is; it now
  prints ffmpeg's actual stderr output, which will explain the real cause
  (usually a bad font path or missing input file).
- **`Cannot open font file`** — double check `--font-path` points to a real
  `.ttf`/`.otf` file. On Windows, use forward slashes (`C:/Fonts/...`) to
  avoid path-escaping issues.
- **Text not visible in output** — make sure the font color contrasts with
  your video/background, and that `--font-size` isn't too large for the
  1080x1920 canvas.

## Project structure

```
deltarune_capcutter/
├── video_editor.py       # main script
├── requirements.txt      # Python package dependencies
├── arial.ttf  # font used for text overlay (not tracked in git)
├── .gitignore
└── README.md
```

## .gitignore

Recommended contents, so the virtual environment and generated files never
get committed:

```
venv/
__pycache__/
*.pyc
output*.mp4
```