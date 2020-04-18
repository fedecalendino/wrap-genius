from enum import Enum
from time import time
from typing import Any, Dict, Iterator, List, Optional

import requests

from genius.classes import Artist, Song
from genius.exceptions import APIException


class SortingKeys(str, Enum):
    TITLE = "title"
    POPULARITY = "popularity"

    def __str__(self):
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

        if self.verbose:
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
    ) -> List[Dict]:
        assert text
        assert page > 0
        assert 21 > per_page > 1

        result = self("search", q=text, page=page, per_page=per_page)

        return list(map(
            lambda hit: hit["result"],
            result.get("hits", [])
        ))


class Genius:
    def __init__(self, access_token: str, verbose: bool = False):
        self.api = API(access_token, verbose)

    def get_song(self, song_id: int) -> Song:
        return Song(self, self.api.get_song(song_id))

    def get_artist(self, artist_id: int) -> Artist:
        return Artist(self, self.api.get_artist(artist_id))

    def get_artist_songs(
        self,
        artist_id: int,
        page: int = 1,
        per_page: int = 50,
        sort: str = SortingKeys.TITLE
    ) -> List[Song]:
        return list(map(
            lambda song: Song(self, song),
            self.api.get_artist_songs(artist_id, page, per_page, sort)
        ))

    def get_all_artist_songs(
        self,
        artist_id: int,
        sort: str = "title"
    ) -> List[Song]:
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
    ) -> List[Song]:
        result = self.api.search(text=text, page=page, per_page=per_page)
        return list(map(lambda song: Song(self, song), result))

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


