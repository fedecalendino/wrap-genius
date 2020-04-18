import json
import re
from typing import List

import requests
from bs4 import BeautifulSoup


def _get_soup(url: str, lower=False) -> BeautifulSoup:
    content = requests.get(url).text

    if lower:
        content = content.lower()

    return BeautifulSoup(content, features="html.parser")


def get_lyrics(url: str, attemps_left=3) -> List[str]:
    if not attemps_left:
        return []

    try:
        soup = _get_soup(url)
        div = soup.find("div", attrs={"class": "lyrics"})

        return div.text.strip().split("\n")
    except:
        return get_lyrics(url, attemps_left - 1)


def get_followers(url: str, handle: str) -> int:
    url = url.replace("facebook.com", "business.facebook.com")
    handle = handle.lower()
    soup = _get_soup(url, lower=True)

    if "facebook.com" in url:
        span = soup.find("span", attrs={"id": "pageslikescountdomid"})
        return int(re.sub(r"[^\d]", "", span.text))

    if "instagram.com" in url:
        script = soup.find("script", attrs={"type": "application/ld+json"})
        data = json.loads(script.string)
        return int(data["mainentityofpage"]["interactionstatistic"]["userinteractioncount"])

    if "twitter.com" in url:
        a = soup.find("a", attrs={"href": f"/{handle}/followers"})
        title = a.attrs.get("title", "0")
        return int(re.sub(r"[^\d]", "", title))

    return 0
