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
        self.assertEqual(song.artist.name, "Gorillaz")
        self.assertFalse(song._fully_loaded_)

        self.assertEqual(song.album.name, "Humanz (Deluxe)")
        self.assertEqual(song.album.artist.name, "Gorillaz")

        self.assertEqual(song.release_date_for_display, "March 23, 2017")
        self.assertTrue(song._fully_loaded_)

        featured = song.features[0]
        self.assertEqual(featured.id, 241761)
        self.assertEqual(featured.name, "DRAM")

        writers = {writer.id: writer.name for writer in song.writers}

        self.assertIn(1974, writers)
        self.assertEqual(writers[1974], "Damon Albarn")

        self.assertIn(241761, writers)
        self.assertEqual(writers[241761], "DRAM")

        media = song.media
        self.assertIn("1217912232", media["apple-music"].url)
        self.assertIn("9W44NWYwa1g", media["youtube"].url)

    def test_lyrics(self):
        self.skipTest("Flaky test")

        song = self.genius.get_song(3027414)

        self.assertEqual(song.title, "Andromeda")
        self.assertEqual(song.artist.name, "Gorillaz")
        self.assertFalse(song._fully_loaded_)

        lyrics = song.lyrics
        self.assertNotEqual(lyrics, [])
        self.assertIn("Take it in your heart now, love her", lyrics)

        self.assertFalse(song._fully_loaded_)
