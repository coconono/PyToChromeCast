cast_yt.py

Usage: python cast_yt.py --device "Living Room TV" --url "https://youtu.be/xxxxx" [--verbose]

This script will attempt, in order:
 - Use pychromecast's YouTubeController to open the YouTube app and play the video (preferred)
 - If that fails, fall back to cast.play_media(original_url, 'video/mp4')

Requirements:
pychromecast
casttube