import json
import re
from typing import List

import requests
from bs4 import BeautifulSoup


def _get_soup(url: str) -> BeautifulSoup:
    content = requests.get(url)
    return BeautifulSoup(content.text.lower(), features="html.parser")


def get_lyrics(url: str) -> List[str]:
    soup = _get_soup(url)
    div = soup.find("div", attrs={"class": "lyrics"})

    return div.text.strip().split("\n")


def get_followers(url: str, handle: str) -> int:
    url = url.replace("facebook.com", "business.facebook.com")

    soup = _get_soup(url)

    if "facebook.com" in url:
        span = soup.find("span", attrs={"id": "pageslikescountdomid"})
        return int(re.sub(r"[^\d]", "", span.text))

    if "instagram.com" in url:
        script = soup.find("script", attrs={"type": "application/ld+json"})
        data = json.loads(script.string)

        return int(data["mainentityofpage"]["interactionstatistic"]["userinteractioncount"])

    if "twitter.com" in url:
        a = soup.find("a", attrs={"href": f"/{handle}/followers"})
        title = a.attrs["title"]

        return int(re.sub(r"[^\d]", "", title))

    return -1
