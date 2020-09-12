from .artist import Artist
from .commons import Base


class Album(Base):
    """
    Attributes
    ----------
    id: int
        id of the album.
    artist: genius.classes.artist.Artist
        artist of the album.
    cover_art_url: str
        url of the album's cover image.
    name: str
        name of the album.
    url: str
        url of the album in genius.
    """

    def __init__(self, genius, data):
        super().__init__(genius)

        self.id: int = data["id"]

        self.artist: 'Artist' = Artist(genius, data["artist"])
        self.cover_art_url: str = data.get("cover_art_url")
        self.name: str = data["name"]
        self.url: str = data["url"]

    def __repr__(self):  # pragma: no cover
        return f"{self.name} ({self.id})"
