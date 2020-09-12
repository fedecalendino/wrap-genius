from datetime import datetime
from typing import Dict, List, Optional

from genius.scraper import get_lyrics

from .album import Album
from .artist import Artist
from .commons import Base
from .media import Media


def lazy_property(prop):
    @property
    def wrapper(*args):
        self = args[0]
        if not self._fully_loaded_:
            data = self.genius.api.get_song(self.id)
            self.__init_extra_data__(data)
            self._fully_loaded_ = True
        return prop(self)

    return wrapper


class Song(Base):
    """
    Attributes
    ----------
    id: int
        id of the song.
    album*: genius.classes.album.Album
        album of the song.
    apple_music_id*: str
        id of the song in apple music.
    artist: genius.classes.artist.Artist
        primary artist of the song.
    cover_of* : List[genius.classes.song.Song]
        list of songs covered by the song.
    covered_by* : List[genius.classes.song.Song]
        list of songs that cover the song.
    description*: str
        information about the song.
    features*: List[genius.classes.artist.Artist]
        featured artists of the song.
    hot: bool
        flag to indicate if the song is populare in genius.
    interpolates* : List[genius.classes.song.Song]
        list of songs interpolated by the song.
    interpolated_by* : List[genius.classes.song.Song]
        list of songs that interpole the song.
    is_cover*: bool
        flag to indicate if the song is a cover.
    is_live*: bool
        flag to indicate if the song is a live performance.
    is_remix*: bool
        flag to indicate if the song is a remix.
    media*: Dict[str, genius.classes.media.Media]
        collection of multimedia related to the song.
    pageviews: int
        amount of page views of the song in genius.
    producers*: List[genius.classes.artist.Artist]
        producers of the song.
    recording_location*: str
        location where the song was recorded.
    release_date*: datetime
        released date of the song.
    release_date_for_display*: str
        formated released date "(MMM DD, YYYY)".
    remix_of* : List[genius.classes.song.Song]
        list of songs remixed in th song.
    remixed_by* : List[genius.classes.song.Song]
        list of songs that remixed the song.
    samples* : List[genius.classes.song.Song]
        list of songs sampled in the song.
    sampled_in* : List[genius.classes.song.Song]
        list of songs that sampled the song.
    live_version_of* : List[genius.classes.song.Song]
        list of songs that are a studio version of the song.
    performed_live_as* : List[genius.classes.song.Song]
        list of songs that a live performance of the song.
    song_art_image_url: str
        url of the songs's art image.
    title: str
        title of the song.
    title_with_featured: str
        title of the song including featured artists.
    url: str
        url of the song in genius.
    writers*: List[genius.classes.artist.Artist]
        writers of the song.
    note:
        **the attributes marked with a * will trigger one extra call to the api.**
    """
    def __init__(self, genius, data):
        super().__init__(genius)
        stats = data.get("stats", {})

        self.id: int = data["id"]
        self.artist: 'Artist' = Artist(self.genius, data["primary_artist"])
        self.hot: bool = stats.get("hot", False)
        self.pageviews: int = stats.get("pageviews", 0)
        self.song_art_image_url: str = data.get("song_art_image_url")
        self.title: str = data["title"]
        self.title_with_featured: str = data["title_with_featured"]
        self.url: str = data["url"]

        self.__init_extra_data__(data)

    def __init_extra_data__(self, data):
        album = data.get("album")
        if album:
            album = Album(self.genius, album)

        release_date = data.get("release_date")
        if release_date:
            release_date = datetime.strptime(release_date, "%Y-%m-%d")

        self.__album: Optional[Album] = album
        self.__description: str = data.get("description", {}).get("plain")
        self.__recording_location: str = data.get("recording_location")
        self.__release_date: Optional[datetime] = release_date
        self.__release_date_for_display: str = data.get("release_date_for_display")

        self.__media: Dict[str, Media] = dict(map(
            lambda m: (m["provider"], Media(self.genius, m)),
            data.get("media", [])
        ))

        apple_music_id = data.get("apple_music_id")
        if apple_music_id:
            self.__media["apple-music"] = Media(
                genius=self.genius,
                data={
                    "provider": "apple music",
                    "type": "audio",
                    "url": f"https://music.apple.com/station/ra.{apple_music_id}",
                }
            )

        self.__features: List['Artist'] = list(map(
            lambda fa: Artist(self.genius, fa),
            data.get("featured_artists", [])
        ))
        self.__producers: List['Artist'] = list(map(
            lambda pa: Artist(self.genius, pa),
            data.get("producer_artists", [])
        ))
        self.__writers: List['Artist'] = list(map(
            lambda wa: Artist(self.genius, wa),
            data.get("writer_artists", [])
        ))

        for relationship in data.get("song_relationships", []):
            type_ = relationship["type"]
            songs = list(map(
                lambda rs: Song(self.genius, rs),
                relationship.get("songs", [])
            ))

            if type_ == "samples":
                self.__samples: List['Song'] = songs
            elif type_ == "sampled_in":
                self.__sampled_in: List['Song'] = songs
            elif type_ == "interpolates":
                self.__interpolates: List['Song'] = songs
            elif type_ == "interpolated_by":
                self.__interpolated_by: List['Song'] = songs
            elif type_ == "cover_of":
                self.__cover_of: List['Song'] = songs
            elif type_ == "covered_by":
                self.__covered_by: List['Song'] = songs
            elif type_ == "remix_of":
                self.__remix_of: List['Song'] = songs
            elif type_ == "remixed_by":
                self.__remixed_by: List['Song'] = songs
            elif type_ == "live_version_of":
                self.__live_version_of: List['Song'] = songs
            elif type_ == "performed_live_as":
                self.__performed_live_as: List['Song'] = songs

    @lazy_property
    def description(self) -> str:
        return self.__description

    @lazy_property
    def recording_location(self) -> str:
        return self.__recording_location

    @lazy_property
    def release_date(self) -> datetime:
        return self.__release_date

    @lazy_property
    def release_date_for_display(self) -> str:
        return self.__release_date_for_display

    @lazy_property
    def album(self) -> 'Album':
        return self.__album

    @lazy_property
    def media(self) -> Dict[str, Media]:
        return self.__media

    @lazy_property
    def features(self) -> List['Artist']:
        return self.__features

    @lazy_property
    def producers(self) -> List['Artist']:
        return self.__producers

    @lazy_property
    def writers(self) -> List['Artist']:
        return self.__writers

    @lazy_property
    def samples(self) -> List['Song']:
        return self.__samples

    @lazy_property
    def sampled_in(self) -> List['Song']:
        return self.__sampled_in

    @lazy_property
    def interpolates(self) -> List['Song']:
        return self.__interpolates

    @lazy_property
    def interpolated_by(self) -> List['Song']:
        return self.__interpolated_by

    @lazy_property
    def cover_of(self) -> List['Song']:
        return self.__cover_of

    @lazy_property
    def covered_by(self) -> List['Song']:
        return self.__covered_by

    @lazy_property
    def remix_of(self) -> List['Song']:
        return self.__remix_of

    @lazy_property
    def remixed_by(self) -> List['Song']:
        return self.__remixed_by

    @lazy_property
    def live_version_of(self) -> List['Song']:
        return self.__live_version_of

    @lazy_property
    def performed_live_as(self) -> List['Song']:
        return self.__performed_live_as

    @property
    def is_cover(self):
        return len(self.cover_of) > 0

    @property
    def is_live(self):
        return len(self.live_version_of) > 0

    @property
    def is_remix(self):
        return len(self.remix_of) > 0

    @property
    def lyrics(self) -> List[str]:
        """
        Fetch the lyrics of the song using a scraper.

        Returns
        -------
        List[str]
            Lines of the lyrics.
        """
        return get_lyrics(self.url)

    def __repr__(self):  # pragma: no cover
        return f"{self.title} ({self.id})"
