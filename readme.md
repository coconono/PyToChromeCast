## cast_yt.py

This script sends a youtube link to a casting device via python. It works best when you already have the youtube app open on your cast target. 

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

## list_cast.py

This script lists all available Chromecast devices on your local network.

### Usage

```sh
python list_cast.py
```

This will output a list of Chromecast device names and their IP addresses, for example:

```
Searching for Chromecast devices on the local network...
Found 2 device(s):
- Music Barn TV (192.168.0.165)
- Living Room TV (192.168.0.181)
```

Use this script to discover the exact device names to use with `cast_yt.py`.

## search_yt.py

This script searches YouTube and returns video links and short text summaries for a given query.

### Usage

```sh
python search_yt.py "cool RC cars"
```

#### Optional arguments
- `--max N` : Maximum number of results to return (default: 5)

### YouTube API Key Setup

1. Copy `config.yaml.example` to `config.yaml`:
   ```sh
   cp config.yaml.example config.yaml
   ```
2. Follow the instructions in `config.yaml.example` to obtain a YouTube Data API v3 key and paste it into `config.yaml`.
3. **Do not commit your real API key!** `config.yaml` is already in `.gitignore`.

### Example Output
```
1. Cool RC Cars Compilation
   https://www.youtube.com/watch?v=XXXXXXXXXXX
   A fun compilation of cool RC cars in action...

2. Best RC Cars 2024
   https://www.youtube.com/watch?v=YYYYYYYYYYY
   Our picks for the best RC cars this year...
```

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

# Run the scripts
python list_cast.py
python cast_yt.py --device "Your Chromecast Name" --url "https://youtu.be/xxxxx" [--verbose]
```
