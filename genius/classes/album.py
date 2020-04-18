from .artist import Artist


class Album:
    def __init__(self, api, data):
        self.api = api

        self.id: int = data["id"]
        self.api_path: str = data["api_path"]
        self.name: str = data["name"]
        self.url: str = data["url"]

        self.artist: 'Artist' = Artist(api, data["artist"])

        self.cover_art_url: str = data.get("cover_art_url")
        self.full_title: str = data.get("full_title")

    def __repr__(self):
        return f"{self.name} ({self.id})"
