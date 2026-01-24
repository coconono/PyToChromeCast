cast_yt.py

## Usage

```sh
python cast_yt.py --device "Living Room TV" --url "https://youtu.be/xxxxx" [--verbose]
```

### Flags

- `--device`, `-d` (required): Chromecast device name (friendly name)
- `--url`, `-u` (required): YouTube URL or video ID
- `--verbose`, `-v`: Enable verbose logging

### Example

```sh
python cast_yt.py --device "Music Barn TV" --url "https://youtu.be/x1t-z4QO4-M?si=m1H0Jfuk_GcSOt6j" --verbose
```

## How it works

This script will attempt, in order:
- Use pychromecast's YouTubeController to open the YouTube app and play the video (preferred)
- If that fails, fall back to `cast.play_media(original_url, 'video/mp4')`

## Requirements

- pychromecast
- casttube

## Python Environment Setup

It is recommended to use a virtual environment for isolation:

```sh
# Create a virtual environment (Python 3.14+ recommended)
python3 -m venv .venv

# Activate the environment (macOS/Linux)
source .venv/bin/activate
# On Windows, use:
# .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the script
python cast_yt.py --device "Your Chromecast Name" --url "https://youtu.be/xxxxx" [--verbose]
```