import os
from unittest import TestCase

import ddt

from genius.api import Genius


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
