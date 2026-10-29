#!/usr/bin/env python3
import json
import os
import time
from pathlib import Path
import feedparser
import requests

# Feed configuration
FEED_URL = "https://blog.centos.org/feed"
OUTPUT_DIR = Path("centos")
OUTPUT_FILE = OUTPUT_DIR / "blog.json"
MAX_ITEMS = 10  # Set to None to fetch all available entries


def fetch_wordpress_feed():
    # A standard User-Agent prevents servers and CDNs from rejecting automated scrapers
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; JekyllFeedBot/1.0; +https://jekyllrb.com)"
    }

    response = requests.get(FEED_URL, headers=headers, timeout=15)
    response.raise_for_status()

    # Parse RSS XML content
    feed = feedparser.parse(response.content)

    entries = feed.entries if MAX_ITEMS is None else feed.entries[:MAX_ITEMS]
    posts = []

    for entry in entries:
        # Convert parsed time tuple to ISO-8601 for easy Jekyll Liquid formatting
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            iso_date = time.strftime(
                "%Y-%m-%dT%H:%M:%SZ", entry.published_parsed
            )
        else:
            iso_date = entry.get("published", "")

        posts.append(
            {
                "id": entry.get("id", entry.get("link", "")),
                "title": entry.get("title", "").strip(),
                "url": entry.get("link", "").strip(),
                "date": iso_date,
                "author": entry.get("author", "CentOS Team"),
                "summary": entry.get("summary", "").strip(),
                "categories": [
                    tag.term for tag in entry.get("tags", []) if "term" in tag
                ],
            }
        )

    # Ensure the _data directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)

    print(f"Exported {len(posts)} posts to {OUTPUT_FILE}")


if __name__ == "__main__":
    fetch_wordpress_feed()

