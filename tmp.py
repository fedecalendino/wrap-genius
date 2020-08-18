import os
from genius.api import Genius


GENIUS_ACCESS_TOKEN = os.getenv("GENIUS_ACCESS_TOKEN")

genius = Genius(GENIUS_ACCESS_TOKEN)
song = genius.get_song(3027414)