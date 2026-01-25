import argparse
import requests
import yaml
import os

YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_VIDEO_URL = "https://www.youtube.com/watch?v={video_id}"


def load_api_key(config_path="config.yaml"):
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file '{config_path}' not found. Please create it with your YouTube API key.")
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    api_key = config.get("youtube_api_key")
    if not api_key:
        raise ValueError("'youtube_api_key' not found in config.yaml.")
    return api_key


def search_youtube(query, api_key, max_results=5):
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": max_results,
        "key": api_key,
    }
    resp = requests.get(YOUTUBE_SEARCH_URL, params=params)
    resp.raise_for_status()
    data = resp.json()
    results = []
    for item in data.get("items", []):
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        description = item["snippet"]["description"]
        url = YOUTUBE_VIDEO_URL.format(video_id=video_id)
        results.append({
            "title": title,
            "url": url,
            "description": description,
        })
    return results


def main():
    parser = argparse.ArgumentParser(description="Search YouTube and return links and summaries.")
    parser.add_argument("query", help="Search query for YouTube.")
    parser.add_argument("--max", type=int, default=5, help="Max results to return (default: 5)")
    args = parser.parse_args()

    api_key = load_api_key()
    results = search_youtube(args.query, api_key, max_results=args.max)
    for i, r in enumerate(results, 1):
        print(f"{i}. {r['title']}")
        print(f"   {r['url']}")
        print(f"   {r['description'][:120]}{'...' if len(r['description']) > 120 else ''}\n")

if __name__ == "__main__":
    main()
