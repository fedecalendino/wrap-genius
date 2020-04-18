from .commons import Base


class Media(Base):
    def __init__(self, genius, data):
        super().__init__(genius)

        self.native_uri: str = data.get("native_uri")
        self.provider: str = data.get("provider")
        self.start: int = data.get("start", 0)
        self.type: str = data.get("type")
        self.url: str = data.get("url")

    def __repr__(self):
        return self.url
