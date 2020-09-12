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
    List[str]:
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
