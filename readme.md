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