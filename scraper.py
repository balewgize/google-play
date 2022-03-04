"""
Extract app information from Google Play Store
"""

import re
import sys
import json
import random
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter, Retry


# List of latest user agents for Firefox, Safari, Opera, Edge
with open("user_agents.txt") as f:
    user_agents = [line.strip() for line in f.readlines()]


def get_random_user_agent():
    """Randomly select a user agent on each request."""
    headers = {
        "User-Agent": random.choice(user_agents),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Alt-Used": "play.google.com",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Cache-Control": "max-age=0",
        "TE": "trailers",
    }
    return headers


def get_app_info(app_id, lang="en_US", country="US"):
    """Get required app info given the app id."""
    try:
        headers = get_random_user_agent()
        params = (("id", app_id), ("hl", lang), ("gl", country))

        # Retry failed requests up to three times
        session = requests.Session()
        retry_strategy = Retry(
            total=4,
            backoff_factor=1,
            status_forcelist=[413, 429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS"],
        )
        session.mount("https://", HTTPAdapter(max_retries=retry_strategy))
        session.mount("http://", HTTPAdapter(max_retries=retry_strategy))

        base_url = "https://play.google.com/store/apps/details"
        r = session.get(base_url, headers=headers, params=params, timeout=60)

        if r.status_code == 200:
            soup = BeautifulSoup(r.content, "lxml")
            # <script> position is not changing that's why [12] index being selected.
            # Other <script> tags position are changing.
            # [12] index is a basic app information
            basic_app_info = json.loads(
                re.findall(
                    r"<script nonce=\".*\" type=\"application/ld\+json\">(.*?)</script>",
                    str(soup.select("script")[12]),
                    re.DOTALL,
                )[0]
            )
            return {
                "icon": basic_app_info["image"],
            }
        elif r.status_code == 404:
            print("App not found. Skipping...")
            return None
        else:
            print("The server response was not OK (HTTP 200).")
            with open("source.html", "wb+") as f:
                f.write(r.content)
            return None
    except Exception as e:
        print("ERROR: ", e.with_traceback())
        sys.exit("Exiting the program...")
