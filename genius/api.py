from enum import Enum
from time import time
from typing import Any, Dict, Iterator, List, Optional

import requests

from genius.classes import Artist, Song
from genius.exceptions import APIException


class SortingKeys(str, Enum):
    """Valid sorting keys."""

    POPULARITY = "popularity"
    TITLE = "title"

    def __str__(self):  # pragma: no cover
        return self.value


class API:
    BASE_URL = "https://api.genius.com"

    def __init__(self, access_token: str, verbose: bool = False):
        assert access_token

        self.access_token = f"Bearer {access_token}"
        self.verbose = verbose

    def __call__(
        self,
        service: str,
        **params
    ) -> Dict[str, Any]:
        start = time()
        url = f"{self.BASE_URL}/{service}"

        params["text_format"] = "plain"

        response = requests.get(
            url=url,
            params=params,
            headers={"Authorization": self.access_token}
        ).json()

        if self.verbose:  # pragma: no cover
            total = time() - start
            print(f">>> queried {url} in {total:0.4f} seconds")

        meta = response["meta"]

        if meta["status"] != 200:
            raise APIException(
                status=meta["status"],
                message=meta["message"],
                url=url
            )

        return response["response"]

    def get_song(self, song_id: int) -> Optional[Dict]:
        assert song_id

        return self(f"songs/{song_id}").get("song")

    def get_artist(self, artist_id: int) -> Optional[Dict]:
        assert artist_id

        return self(f"artists/{artist_id}").get("artist")

    def get_artist_songs(
        self,
        artist_id: int,
        page: int = 1,
        per_page: int = 50,
        sort: str = SortingKeys.TITLE
    ) -> List[Dict]:
        assert artist_id
        assert page > 0
        assert 51 > per_page > 1
        assert sort in list(SortingKeys)

        return self(
            service=f"artists/{artist_id}/songs",
            page=page,
            per_page=per_page,
            sort=sort
        ).get("songs", [])

    def search(
        self,
        text: str,
        page: int = 1,
        per_page: int = 20
    ) -> Iterator[Dict]:
        assert text
        assert page > 0
        assert 21 > per_page > 1

        result = self("search", q=text, page=page, per_page=per_page)

        return map(
            lambda hit: hit["result"],
            result.get("hits", [])
        )


class Genius:
    def __init__(self, access_token: str, verbose: bool = False):
        self.api = API(access_token, verbose)

    def get_song(self, song_id: int) -> Song:
        """
        Retrieve the information of a song.

        Parameters
        ----------
        song_id: int
            ID of the song.

        Returns
        -------
        genius.classes.song.Song
        """
        return Song(self, self.api.get_song(song_id))

    def get_artist(self, artist_id: int) -> Artist:
        """
        Retrieve the information of an artist.

        Parameters
        ----------
        artist_id: int
            ID of the artist.

        Returns
        -------
        genius.classes.artist.Artist
        """
        return Artist(self, self.api.get_artist(artist_id))

    def get_artist_songs(
        self,
        artist_id: int,
        page: int = 1,
        per_page: int = 50,
        sort: str = SortingKeys.TITLE
    ) -> Iterator[Song]:
        """
        Retrieve the songs of an artist.

        Parameters
        ----------
        artist_id: int
            ID of the artist.
        page: int
            Desired page.
        per_page: int
            Amount of songs per page.
        sort: string
            Sort key for the songs (title/popularity).

        Returns
        -------
        Iterator[genius.classes.song.Song]
            Songs of the artist.
        """

        return map(
            lambda song: Song(self, song),
            self.api.get_artist_songs(artist_id, page, per_page, sort)
        )

    def get_all_artist_songs(
        self,
        artist_id: int,
        sort: str = "title"
    ) -> Iterator[Song]:
        """
        Retrieve the all the songs of an artist.

        Parameters
        ----------
        artist_id: int
            ID of the artist.
        sort: string
            Sort key for the songs (title/popularity).

        Yields
        -------
        genius.classes.song.Song
            Song of the artist.
        """
        page = 0

        while True:
            page += 1
            songs = self.get_artist_songs(artist_id, page=page, sort=sort)

            if not songs:
                break

            yield from songs

    def search(
        self,
        text: str,
        page: int = 1,
        per_page: int = 20
    ) -> Iterator[Song]:
        """
        Search for songs that match with the provided text.

        Parameters
        ----------
        text: str
            Text to search.
        page: int
            Desired page.
        per_page: int
            Amount of songs per page.

        Returns
        -------
        Iterator[genius.classes.song.Song]
            Songs that match the search text.
        """

        result = self.api.search(text=text, page=page, per_page=per_page)
        return map(lambda song: Song(self, song), result)

    def search_all(
        self,
        text: str,
        page_limit: int = 10
    ) -> Iterator[Song]:
        """
        Search for all the songs that match with the provided text.

        Parameters
        ----------
        text: str
            Text to search.
        page_limit: int
            Limit of pages in the search.

        Yields
        -------
        genius.classes.song.Song
            Song that matches the search text.
        """

        page = 0

        while True:
            page += 1

            if page_limit and page > page_limit:
                break

            songs = self.search(text, page=page)

            if not songs:
                break

            yield from songs

    def search_artist(self, name: str) -> Optional[Artist]:
        """
        Search for an artist that match with the provided text.

        Parameters
        ----------
        name: str
            Name of the artist to search.

        Returns
        -------
        genius.classes.artist.Artist
            Artist that matches the search.
        """
        name = name.lower()

        for song in self.search_all(name):
            artist = song.artist

            if name == artist.name.lower():
                return artist

        return None
