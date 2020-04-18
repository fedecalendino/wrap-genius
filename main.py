import os
from genius.api import Genius

GENIUS_ACCESS_TOKEN = os.getenv("GENIUS_ACCESS_TOKEN")

genius = Genius(GENIUS_ACCESS_TOKEN, verbose=False)

song = genius.get_song(132997)

print("Song")
print(song)
print(song.release_date)

artist = song.primary_artist
print("Artist:")
print(artist)

for platform, name in artist.social_media.items():
    print(" -", platform, ":", name)

print("Featured Artists:")
for featured_artist in song.featured_artists:
    print("*", featured_artist)

