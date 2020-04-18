import os
from unittest import TestCase

from genius.api import Genius


GENIUS_ACCESS_TOKEN = os.getenv("GENIUS_ACCESS_TOKEN")


class SongTest(TestCase):

    def setUp(self) -> None:
        self.genius = Genius(GENIUS_ACCESS_TOKEN)

    def test_song(self):
        song = self.genius.get_song(3027414)

        self.assertEqual(song.title, "Andromeda")
        self.assertEqual(song.primary_artist.name, "Gorillaz")
        self.assertFalse(song._fully_loaded_)

        self.assertEqual(song.album.name, "Humanz")
        self.assertEqual(song.album.artist.name, "Gorillaz")

        self.assertEqual(song.release_date_for_display, "March 23, 2017")
        self.assertTrue(song._fully_loaded_)

        featured = song.featured_artists[0]
        self.assertEqual(featured.id, 241761)
        self.assertEqual(featured.name, "DRAM")

        writer = song.writer_artists[0]
        self.assertEqual(writer.id, 241761)
        self.assertEqual(writer.name, "DRAM")

        writer = song.writer_artists[1]
        self.assertEqual(writer.id, 1974)
        self.assertEqual(writer.name, "Damon Albarn")

        media = song.media
        self.assertIn("9W44NWYwa1g", media["youtube"].url)

    def test_lyrics(self):
        song = self.genius.get_song(3027414)

        self.assertEqual(song.title, "Andromeda")
        self.assertEqual(song.primary_artist.name, "Gorillaz")
        self.assertFalse(song._fully_loaded_)

        lyrics = song.lyrics
        self.assertNotEqual(lyrics, [])
        self.assertIn("Take it in your heart now, love her", lyrics)

        self.assertFalse(song._fully_loaded_)
