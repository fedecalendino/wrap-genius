 # wrap-genius

[![Version](https://img.shields.io/pypi/v/wrap-genius?logo=pypi)](https://pypi.org/project/wrap-genius)
[![Quality Gate Status](https://img.shields.io/sonar/alert_status/fedecalendino_wrap-genius?logo=sonarcloud&server=https://sonarcloud.io)](https://sonarcloud.io/dashboard?id=fedecalendino_wrap-genius)
[![CodeCoverage](https://img.shields.io/sonar/coverage/fedecalendino_wrap-genius?logo=sonarcloud&server=https://sonarcloud.io)](https://sonarcloud.io/dashboard?id=fedecalendino_wrap-genius)

Python wrapper for genius.com's API


## Setup

**wrap-genius** is supported on Python 3.8+ and it can be installed using [pip](https://pypi.python.org/pypi/pip).

```bash
pip install wrap-genius
```   

To be able to use it, you'll need to create an API client for [genius.com](https://genius.com/api-clients) and get a **CLIENT ACCESS TOKEN**.


## Quickstart

Assuming you already have you access token, get an instance of the genius wrapper as follows:

```python
from genius import Genius
g = Genius(access_token="YOUR-TOKEN")
```   

With this instance you can interact with genius in many ways:

```python
# Search for an artist by name
artist = g.search_artist("Gorillaz")
print(artist)
```
```text
>> "Gorillaz (860)"
```


```python
# Get the artist's song by popularity
for song in artist.songs_by_popularity:
    print(song)
```
```text
>> "Feel Good Inc. (21569)"
>> "Clint Eastwood (1698)"
>> "Saturnz Barz (3027437)"
>> "Ascension (3027418)"
>> "On Melancholy Hill (53533)"
>> ...
```


```python
# Get the details of a song by its id
song = g.get_song(song_id=3027414)
print(song.title_with_featured)
print(song.release_date_for_display)
```
```text
>> "Andromeda (Ft. DRAM)"
>> "March 23, 2017"
```


```python
# Get the song album, or the featured artists
print(song.album)
for featured in song.features:
    print(featured.name)
```
```text
>> "Humanz (335930)"
>> "DRAM (241761)"
```

```python
# And even, a song's lyrics
lyrics = song.lyrics
print('\n'.join(lyrics))
```
```text
>> "[Verse 1: 2-D]"
>> "When the pulsing looks to die for"
>> "Take it in your heart now, lover"
>> "When the case is out"
>> "And tired and sodden"
>> "Take it in your heart"
>> "Take it in your heart"
>> ...
```