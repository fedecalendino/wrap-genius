from itertools import count
from typing import Dict, Iterator, List


def lazy_property(prop):
    @property
    def wrapper(*args):
        self = args[0]
        if not self._fully_loaded_:
            data = self.api.get_artist_data(self.id)
            self.__init_extra_data__(data)
            self._fully_loaded_ = True
        return prop(self)
    return wrapper


class Artist:
    _fully_loaded_: bool = False

    def __init__(self, api, data):
        self.api = api

        self.id: int = data["id"]
        self.api_path: str = data["api_path"]
        self.name: str = data["name"]
        self.url: str = data["url"]

        self.header_image_url: str = data.get("header_image_url")
        self.image_url: str = data.get("image_url")
        self.iq: int = data.get("iq", 0)
        self.is_meme_verified: bool = data.get("is_meme_verified", False)
        self.is_verified: bool = data.get("is_verified", False)

        self.__init_extra_data__(data)

    def __init_extra_data__(self, data):
        self.__alternate_names: List[str] = data.get("alternate_names", [])
        self.__description: str = data.get("description")
        self.__followers_count: int = data.get("followers_count", 0)
        self.__social_media = {
            "facebook": data.get("facebook_name"),
            "instagram": data.get("instagram_name"),
            "twitter": data.get("twitter_name"),
        }

    @lazy_property
    def alternate_names(self) -> List[str]:
        return self.__alternate_names

    @lazy_property
    def description(self) -> str:
        return self.__description

    @lazy_property
    def followers_count(self) -> int:
        return self.__followers_count

    @lazy_property
    def social_media(self) -> Dict[str, str]:
        return self.__social_media

    @property
    def songs(self) -> Iterator['Song']:
        page = count(1)

        while True:
            songs = self.api.get_artist_songs(self.id, next(page))

            if not songs:
                break

            yield from songs

    def __repr__(self):
        return f"{self.name} ({self.id})"
