from typing import Dict, Iterator, List, Optional

from .commons import Base
from .social_media import SocialMedia


def lazy_property(prop):
    @property
    def wrapper(*args):
        self = args[0]
        if not self._fully_loaded_:
            data = self.genius.api.get_artist(self.id)
            self.__init_extra_data__(data)
            self._fully_loaded_ = True
        return prop(self)
    return wrapper


class Artist(Base):
    def __init__(self, genius, data):
        super().__init__(genius)

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
        self.__description: str = data.get("description", {}).get("plain")
        self.__followers_count: int = data.get("followers_count", 0)

        self.__social_media: Dict[str, Optional[SocialMedia]] = {}

        for network in ["facebook", "instagram", "twitter"]:
            handle = data.get(f"{network}_name")
            self.__social_media[network] = SocialMedia(network, handle) if handle else None

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
    def social_media(self) -> Dict[str, SocialMedia]:
        return self.__social_media

    @property
    def songs(self) -> Iterator['Song']:
        yield from self.genius.get_all_artist_songs(self.id)

    @property
    def songs_by_popularity(self) -> Iterator['Song']:
        yield from self.genius.get_all_artist_songs(self.id, sort="popularity")

    def __repr__(self):
        return f"{self.name} ({self.id})"
