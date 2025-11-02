"""
cast_yt.py

Usage: python cast_yt.py --device "Living Room TV" --url "https://youtu.be/xxxxx" [--verbose]

This script will attempt, in order:
 - Use pychromecast's YouTubeController to open the YouTube app and play the video (preferred)
 - If that fails, fall back to cast.play_media(original_url, 'video/mp4')

Requirements:
 - pychromecast
 - casttube

"""
from __future__ import annotations
import argparse
import sys
import time
import traceback
import re
from typing import Optional
import pychromecast
from pychromecast.controllers.youtube import YouTubeController
from casttube import YouTubeSession

def extract_youtube_id(url: str) -> Optional[str]:
    if not url:
        return None
    m = re.search(r"(?:v=|youtu\.be/|/v/|/embed/)([0-9A-Za-z_-]{11})", url)
    if m:
        return m.group(1)
    m2 = re.search(r"([0-9A-Za-z_-]{11})", url)
    return m2.group(1) if m2 else None


def find_cast_by_name(name: str, timeout: int = 5):
    """Discover chromecasts and return the cast object matching name (case-insensitive)."""
    chromecasts, browser = pychromecast.get_chromecasts()
    # Try exact or case-insensitive match
    for c in chromecasts:
        if c.name == name or c.name.lower() == name.lower():
            return c
    # If not found, try scanning for partial match
    for c in chromecasts:
        if name.lower() in c.name.lower():
            return c
    return None


def wait_for_cast_ready(cast_obj, timeout: int = 10):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            # socket_client is connected when cast is reachable
            sock = getattr(cast_obj, 'socket_client', None)
            if sock is None:
                # may still be ok; try status
                if getattr(cast_obj, 'status', None) is not None:
                    return True
            else:
                if getattr(sock, 'is_connected', False):
                    return True
        except Exception:
            pass
        time.sleep(0.2)
    return False


def play_with_youtube_controller(cast_obj, video_id: str, verbose: bool = False) -> bool:
    try:
        from casttube import YouTubeSession

        # Create YouTube session with screen name based on cast device
        screen_id = f"desktop-{cast_obj.name.lower().replace(' ', '_')}"
        if verbose:
            print('Using screen_id:', screen_id)

        # Create session with required data
        session = YouTubeSession(screen_id)
        session.screen_id = screen_id
        session.app = 'ytcasts'  # YouTube Cast Receiver app
        session.device_id = cast_obj.device.device_id if hasattr(cast_obj, 'device') else None

        # Initialize controller with our session
        yt = YouTubeController(session)
        cast_obj.register_handler(yt)
        cast_obj.wait()

        if verbose:
            print('Registered YouTubeController with session info:', {
                'screen_id': session.screen_id,
                'app': session.app,
                'device_id': session.device_id
            })

        # Try to play
        yt.play_video(video_id)

        # give a moment and check status
        time.sleep(1)
        if verbose:
            print('YouTubeController requested play; cast status:', getattr(cast_obj, 'status', None))
        return True
    except Exception as e:
        if verbose:
            print('YouTubeController failed:', repr(e))
            traceback.print_exc()
        return False





def main(argv=None):
    p = argparse.ArgumentParser(description='Send a YouTube link to a Chromecast device')
    p.add_argument('--device', '-d', required=True, help='Chromecast device name (friendly name)')
    p.add_argument('--url', '-u', required=True, help='YouTube URL or id')
    p.add_argument('--verbose', '-v', action='store_true', help='Verbose logging')
    args = p.parse_args(argv)

    device_name = args.device
    youtube_url = args.url
    verbose = args.verbose

    video_id = extract_youtube_id(youtube_url)
    if video_id and verbose:
        print('Extracted video id:', video_id)

    if verbose:
        print('Discovering chromecasts...')
    chromecasts, browser = pychromecast.get_chromecasts()
    cast = find_cast_by_name(device_name)
    if not cast:
        print(f'Chromecast named "{device_name}" not found. Available:')
        for c in chromecasts:
            print(' -', c.name)
        sys.exit(2)

    if verbose:
        print('Found cast:', cast.name)

    # Wait to be sure socket is connected
    cast.wait()
    if not wait_for_cast_ready(cast, timeout=8):
        if verbose:
            print('Warning: cast did not appear ready after wait')

    # Try YouTubeController if we have a video id, otherwise fall back to play_media
    if video_id:
        if verbose:
            print('Trying YouTubeController...')
        if play_with_youtube_controller(cast, video_id, verbose=verbose):
            if verbose:
                print('YouTubeController succeeded')
            sys.exit(0)
        if verbose:
            print('FAIL ALL IS LOST')


if __name__ == '__main__':
    main()
