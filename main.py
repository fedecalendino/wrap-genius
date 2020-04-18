import os

from genius.api import Genius

GENIUS_ACCESS_TOKEN = os.getenv("GENIUS_ACCESS_TOKEN")

genius = Genius(GENIUS_ACCESS_TOKEN, verbose=False)

artist = genius.search_artist("Gorillaz")

for song in artist.songs:
    print(song.title, song.stats.pageviews)

