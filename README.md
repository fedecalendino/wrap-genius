 # wrap-genius

[![Version](https://img.shields.io/pypi/v/wrap-genius?logo=pypi)](https://pypi.org/project/wrap-genius)
[![Quality Gate Status](https://img.shields.io/sonar/alert_status/fedecalendino_wrap-genius?logo=sonarcloud&server=https://sonarcloud.io)](https://sonarcloud.io/dashboard?id=fedecalendino_wrap-genius)
[![CodeCoverage](https://img.shields.io/sonar/coverage/fedecalendino_wrap-genius?logo=sonarcloud&server=https://sonarcloud.io)](https://sonarcloud.io/dashboard?id=fedecalendino_wrap-genius)

Unofficial python wrapper for genius.com's API


## Setup

**wrap-genius** is supported on Python 3.8+ and it can be installed using [pip](https://pypi.python.org/pypi/pip).

```bash
pip install wrap-genius
```   

To be able to use it, you'll need to create an API client for [genius.com](https://genius.com/api-clients) and get a **CLIENT ACCESS TOKEN**.


## Quickstart

The `genius` wrapper library provides a convenient interface to interact with the Genius API, allowing you to search for songs, artists, and retrieve information about them. This documentation will guide you through the available functionalities of the library with examples.

### Initialization

To start using the `genius` wrapper library, you need to initialize an instance of the `Genius` class. This requires an access token, which you can obtain from the Genius API.

```python
from genius import Genius

g = Genius(access_token="YOUR_ACCESS_TOKEN")
```

### Search All

You can use the `search_all` method to search for songs or artists. It returns a generator that yields search results. Here are some examples:

```python
# Search for an artist
songs = g.search_all("Dua Lipa", page_limit=1) # page_limit is 10 by default, use conservatively if not needed
print(next(songs).title)  # Get the first song
print([song.title for song in songs])  # Get the rest of the songs

# Search for a song
songs = g.search_all("My Iron Lung", page_limit=1)
print(next(songs).title)

# Search for a song by an artist
songs = g.search_all("White Light Gorillaz", page_limit=1)
print(next(songs).title)
```
Output:
```
New Rules
['Scared to Be Lonely', 'Don’t Start Now', 'IDGAF', 'Levitating', 'One Kiss', 'Blow Your Mind (Mwah)', 'Break My Heart', 'Be the One', 'Kiss and Make Up', 'Physical', 'Levitating (Remix)', 'UN DÍA (ONE DAY)', 'Electricity', 'We’re Good', 'Homesick', 'Dua Lipa', 'Love Again', 'Dua Lipa & BLACKPINK - Kiss and Make Up (Romanized)', 'Hotter Than Hell']

My Iron Lung

White Light
```

### Search Artist

You can use the `search_artist` method to search for an artist by their name. It returns an `Artist` object representing the artist. Here is an example:

```python
artist = g.search_artist("Radiohead")
print(artist)  # Artist object
print(artist.alternate_names)
print(artist.followers_count)
print(artist.description[:100] + "..." if len(artist.description) > 100 else artist.description)
print(artist.header_image_url)
print(artist.id)
print(artist.name)
print(artist.is_verified)
print(list(itertools.islice(artist.songs, 5)))
print(list(itertools.islice(artist.songs_by_popularity, 5)))
print(artist.url)
```

## Search Song

You can use the `search_all` method to search for a specific song. It returns a generator that yields song objects. Here is an example:

```python
songs = g.search_all("Karma Police Radiohead", page_limit=1)
song = next(songs)
print(song)  # Song object
print(song.album)
print(song.artist)
print(song.pageviews)
print(song.song_art_image_url)
print(song.title)
print(song.title_with_featured)
print(song.hot)
print(song.description)
print(song.recording_location)
print(song.release_date)
print(song.release_date_for_display)
print(song.features)
print(song.media)
print(song.writers)
print(song.producers)
print(song.samples)
print(song.sampled_in)
print(song.interpolates)
print(song.interpolated_by)
print(song.is_cover)
print(song.is_live)
print(song.is_remix)
print(song.cover_of)
print(song.covered_by)
print(song.remix_of)
print(song.remixed_by)
print(song.live_version_of)
print(song.performed_live_as)
print("\n".join(song.lyrics))
```

