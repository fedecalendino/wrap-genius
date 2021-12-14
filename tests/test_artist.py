import os
from unittest import TestCase

from genius.api import Genius

GENIUS_ACCESS_TOKEN = os.getenv("GENIUS_ACCESS_TOKEN")


class ArtistTest(TestCase):
    def setUp(self) -> None:
        self.genius = Genius(GENIUS_ACCESS_TOKEN)

    def test_artist(self):
        artist = self.genius.get_artist(17237)

        self.assertEqual(artist.name, "Foo Fighters")
        self.assertFalse(artist._fully_loaded_)

        social_media = artist.social_media
        self.assertTrue(artist._fully_loaded_)

        facebook = social_media["facebook"]
        self.assertEqual(facebook.handle, "foofighters")

        instagram = social_media["instagram"]
        self.assertEqual(instagram.handle, "foofighters")

        twitter = social_media["twitter"]
        self.assertEqual(twitter.handle, "foofighters")

        for index, song in enumerate(artist.songs):
            self.assertEqual(song.artist.id, artist.id)
            self.assertEqual(song.artist.name, artist.name)

            if index > 10:
                break

        for index, song in enumerate(artist.songs_by_popularity):
            self.assertEqual(song.artist.id, artist.id)
            self.assertEqual(song.artist.name, artist.name)

            if index > 10:
                break
