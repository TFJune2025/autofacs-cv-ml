"""Example of a public-facing source-ingestion workflow.

This example is adapted from the project's API-based open-source image sourcing
work. It intentionally avoids private dataset paths and keeps the scope narrow:
fetch image metadata, download selected files, and pause politely between calls.
"""

from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Optional

import requests


def download_pexels_images(api_key: str, destination: str | Path, n: int = 100, per_page: int = 15) -> int:
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)

    headers = {"Authorization": api_key}
    page = 1
    downloaded = 0

    while downloaded < n:
        url = f"https://api.pexels.com/v1/curated?per_page={per_page}&page={page}"
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        payload = response.json()
        photos = payload.get("photos", [])
        if not photos:
            break

        for photo in photos:
            image_url = photo.get("src", {}).get("medium")
            if not image_url:
                continue
            filename = destination / f"pexels_{downloaded:05d}.jpg"
            binary = requests.get(image_url, timeout=30).content
            filename.write_bytes(binary)
            downloaded += 1
            if downloaded >= n:
                break

        page += 1
        time.sleep(0.7)

    return downloaded


if __name__ == "__main__":
    api_key = os.getenv("PEXELS_API_KEY")
    if not api_key:
        raise SystemExit("Set PEXELS_API_KEY before running this example.")
    count = download_pexels_images(api_key, destination="./downloads/pexels_unknown", n=25)
    print(f"Downloaded {count} images.")
