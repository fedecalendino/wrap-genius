from time import time
from typing import Any, Dict, Iterator, List, Optional

import requests

from genius.classes import Artist, Song
from genius.exceptions import APIException


class Genius:
    BASE_URL = "https://api.genius.com"

    def __init__(self, access_token: str, verbose: bool = False):
        self.access_token = f"Bearer {access_token}"
        self.verbose = verbose

    def _log(self, **kwargs):
        if not self.verbose:
            return

        print()

        for key, value in kwargs.items():
            print(">>>", key, ":", value)

        print()

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

        end = time()

        meta = response["meta"]

        if meta["status"] != 200:
            raise APIException(
                status=meta["status"],
                message=meta["message"],
                url=url
            )

        self._log(url=url, seconds=end - start)
        return response["response"]

    def search(
        self,
        text: str,
        page: int = 1,
        per_page: int = 20
    ) -> List[Song]:

        assert text
        assert page > 0
        assert 21 > per_page > 1

        result = self("search", q=text, page=page, per_page=per_page)

        return list(map(
            lambda hit: Song(self, hit["result"]),
            result.get("hits", [])
        ))

    def search_all(
        self,
        text: str,
        page_limit: int = 10
    ) -> Iterator[Song]:

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
        name = name.lower()

        for song in self.search_all(name):
            artist = song.primary_artist

            if name == artist.name.lower():
                return artist

        return None

    def search_songs(
        self,
        title: str,
        exact: bool = False,
        page_limit: int = 10
    ) -> Iterator[Song]:

        title = title.lower()

        for song in self.search_all(title, page_limit=page_limit):
            if not exact:
                if title in song.title.lower():
                    yield song
            else:
                titles = {
                    song.title.lower(),
                    song.title_with_featured.lower(),
                    song.full_title.lower(),
                }

                if title in titles:
                    yield song

    def get_artist_data(self, artist_id: int) -> Dict:
        return self(f"artists/{artist_id}")["artist"]

    def get_artist(self, artist_id: int) -> Artist:
        return Artist(self, self.get_artist_data(artist_id))

    def get_artist_songs(
        self,
        artist_id: int,
        page: int = 1,
        per_page: int = 50,
        sort: str = "title"
    ) -> List[Song]:
        
        assert page > 0
        assert 51 > per_page > 1

        result = self(f"artists/{artist_id}/songs", page=page, per_page=per_page, sort=sort)

        return list(map(
            lambda song: Song(self, song),
            result.get("songs", [])
        ))

    def get_song_data(self, song_id: int) -> Dict:
        return self(f"songs/{song_id}")["song"]

    def get_song(self, song_id: int) -> Song:
        return Song(self, self.get_song_data(song_id))
