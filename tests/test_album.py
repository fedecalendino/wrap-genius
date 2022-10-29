import os
from unittest import TestCase

from genius.api import Genius

GENIUS_ACCESS_TOKEN = os.getenv("GENIUS_ACCESS_TOKEN")


class AlbumTest(TestCase):
    def setUp(self) -> None:
        self.genius = Genius(GENIUS_ACCESS_TOKEN)

    def test_album(self):
        song = self.genius.get_song(3027414)

        self.assertEqual(song.title, "Andromeda")
        self.assertEqual(song.artist.name, "Gorillaz")
        self.assertFalse(song._fully_loaded_)

        self.assertEqual(song.album.name, "Humanz (Deluxe)")
        self.assertEqual(song.album.artist.name, "Gorillaz")

        expected = [
            (3029506, "Intro: I Switched My Robot Off"),
            (3027418, "Ascension"),
            (3027446, "Strobelite"),
            (3027437, "Saturnz Barz"),
            (3027432, "Momentz"),
            (3029507, "Interlude: The Non-Conformist Oath"),
            (3027447, "Submission"),
            (3027424, "Charger"),
            (3029508, "Interlude: Elevator Going Up"),
            (3027414, "Andromeda"),
            (3027420, "Busted and Blue"),
            (3029510, "Interlude: Talk Radio"),
            (3027422, "Carnival"),
            (3027431, "Let Me Out"),
            (3029514, "Interlude: Penthouse"),
            (3027443, "Sex Murder Party"),
            (3027445, "She’s My Collar"),
            (3029516, "Interlude: The Elephant"),
            (2960570, "Hallelujah Money"),
            (3027453, "We Got the Power"),
            (3029517, "Interlude: New World"),
            (3027448, "The Apprentice"),
            (3027427, "Halfway to the Halfway House"),
            (3027435, "Out of Body"),
            (3027451, "Ticker Tape"),
            (3027425, "Circle of Friendz"),
        ]

        for (id, title), song in zip(expected, song.album.songs):
            self.assertEqual(id, song.id)
            self.assertEqual(title, song.title)
