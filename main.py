import os

from genius.api import Genius

GENIUS_ACCESS_TOKEN = os.getenv("GENIUS_ACCESS_TOKEN")

genius = Genius(GENIUS_ACCESS_TOKEN, verbose=True)

artist = genius.search_artist("Daft Punk")
print(artist)
print(artist.social_media["instagram"])
print(artist.social_media["instagram"].followers)

for song in artist.songs_by_popularity:
    print(song.title, song.stats.pageviews)
    print(song.featured_artists)

    break


song = genius.get_song(10)
print(song)
print(song.primary_artist)
