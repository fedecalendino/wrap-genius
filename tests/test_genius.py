import os
from unittest import TestCase

import ddt

from genius.api import Genius
from genius.exceptions import APIException

GENIUS_ACCESS_TOKEN = os.getenv("GENIUS_ACCESS_TOKEN")


@ddt.ddt
class GeniusTest(TestCase):
    def setUp(self) -> None:
        self.genius = Genius(GENIUS_ACCESS_TOKEN)

    @ddt.data(
        (860, "Gorillaz"),
        (13585, "Daft Punk"),
    )
    @ddt.unpack
    def test_get_artist(self, artist_id, artist_name):
        artist = self.genius.get_artist(artist_id)
        self.assertEqual(artist.name, artist_name)

    @ddt.data(
        (860, "Gorillaz"),
        (13585, "Daft Punk"),
    )
    @ddt.unpack
    def test_search_artist(self, artist_id, artist_name):
        artist = self.genius.search_artist(artist_name)
        self.assertEqual(artist.id, artist_id)

    @ddt.data(
        (3027437, "Saturnz Barz", "Gorillaz"),
        (3027418, "Ascension", "Gorillaz"),
        (53533, "On Melancholy Hill", "Gorillaz"),
        (3027414, "Andromeda", "Gorillaz"),
        (151355, "Instant Crush", "Daft Punk"),
        (151349, "Giorgio by Moroder", "Daft Punk"),
        (151385, "Fragments of Time", "Daft Punk"),
        (72011, "Digital Love", "Daft Punk"),
    )
    @ddt.unpack
    def test_get_song(self, song_id, song_title, artist_name):
        song = self.genius.get_song(song_id)
        self.assertEqual(song.title, song_title)
        self.assertEqual(song.artist.name, artist_name)

    @ddt.data(
        (3027437, "Saturnz Barz", "Gorillaz"),
        (3027418, "Ascension", "Gorillaz"),
        (53533, "On Melancholy Hill", "Gorillaz"),
        (3027414, "Andromeda", "Gorillaz"),
        (151355, "Instant Crush", "Daft Punk"),
        (151349, "Giorgio by Moroder", "Daft Punk"),
        (151385, "Fragments of Time", "Daft Punk"),
        (72011, "Digital Love", "Daft Punk"),
    )
    @ddt.unpack
    def test_search_songs(self, song_id, song_title, artist_name):
        song = next(self.genius.search_all(song_title))

        self.assertEqual(song.id, song_id)
        self.assertEqual(song.artist.name, artist_name)

    def test_api_exception(self):
        with self.assertRaises(APIException):
            self.genius.get_song(2678345123867)

        with self.assertRaises(APIException):
            self.genius.get_artist(2678345123867)
