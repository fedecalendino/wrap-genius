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
    """
    Looks for the lyrics of a song in genius.

    Parameters
    ----------
    url: str
        Url of the song in genius.

    Returns
    -------
    list of str:
        Lines of the lyrics.

    """
    if not attemps_left:
        return []

    try:
        soup = _get_soup(url)
        div = soup.find("div", attrs={"class": "lyrics"})

        return div.text.strip().split("\n")
    except:
        return get_lyrics(url, attemps_left - 1)


def get_followers(url: str, handle: str) -> int:
    """
    Looks for the amount of followers in a given social medial.

    Parameters
    ----------
    url: str
        Url of the profile.
    handle: str
        Username of the account.

    Returns
    -------
    int
        Amount of followers.

    """
    url = url.replace("facebook.com", "business.facebook.com")
    handle = handle.lower()
    soup = _get_soup(url, lower=True)

    if "facebook.com" in url:
        span = soup.find("span", attrs={"id": "pageslikescountdomid"})
        return int(re.sub(r"[^\d]", "", span.text))

    if "instagram.com" in url:
        script = next(
            filter(
                lambda s: len(s.contents) and handle in s.contents[0],
                soup.find_all("script", attrs={"type": "text/javascript"})
            )
        )
        content = json.loads(script.contents[0].replace("window._shareddata = ", "")[:-1])
        return content["entry_data"]["profilepage"][0]["graphql"]["user"]["edge_followed_by"]["count"]

    if "twitter.com" in url:
        a = soup.find("a", attrs={"href": f"/{handle}/followers"})
        title = a.attrs.get("title", "0")
        return int(re.sub(r"[^\d]", "", title))

    return 0
