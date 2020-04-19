from .commons import Base


class Media(Base):
    """
    Attributes
    ----------
    provider: str
        provider of the media (youtube, spotify, etc.)
    type: str
        media type (audio/video).
    url: str
        url of the media.
    """

    def __init__(self, genius, data):
        super().__init__(genius)

        self.provider: str = data.get("provider")
        self.type: str = data.get("type")
        self.url: str = data.get("url")

    def __repr__(self):  # pragma: no cover
        return self.url
