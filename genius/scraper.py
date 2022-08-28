import logging
from typing import List

import requests
from bs4 import BeautifulSoup, NavigableString

logger = logging.getLogger(__name__)


def _get_soup(url: str, lower=False) -> BeautifulSoup:
    content = requests.get(url).text

    if lower:
        content = content.lower()

    return BeautifulSoup(content, features="html.parser")


def _extract_lyrics(current) -> List[str]:
    if type(current) is NavigableString:
        return [str(current)]

    lines = []

    for children in current.children:
        lines += _extract_lyrics(children)

    return lines


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
        soup = _get_soup(f"{url}")
        div = soup.find("div", attrs={"data-lyrics-container": "true"})
        return _extract_lyrics(div)
    except Exception as exc:
        logger.error("Failed to fetch lyrics: %s", exc)
        return get_lyrics(url, attemps_left - 1)
