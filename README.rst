wrap-genius
===========

Python wrapper for genius.com's API
-----------------------------------

.. image:: https://img.shields.io/pypi/v/wrap-genius?logo=pypi
    :target: https://pypi.org/project/wrap-genius

.. image:: https://img.shields.io/readthedocs/wrap-genius?logo=read%20the%20docs
    :target: https://wrap-genius.readthedocs.io/en/latest/

.. image:: https://img.shields.io/travis/federicocalendino/wrap-genius/master?logo=travis
    :target: https://travis-ci.com/federicocalendino/wrap-genius

.. image:: https://img.shields.io/sonar/alert_status/federicocalendino_wrap-genius?logo=sonarcloud&server=https://sonarcloud.io
    :target: https://sonarcloud.io/dashboard?id=federicocalendino_wrap-genius

.. image:: https://img.shields.io/codecov/c/gh/federicocalendino/wrap-genius?logo=codecov
    :target: https://codecov.io/gh/federicocalendino/wrap-genius


Installation
------------

**wrap-genius** is supported on Python 3.6+ and it can be installed using `pip <https://pypi.python.org/pypi/pip>`_

.. code-block:: bash

   pip install wrap-genius

To be able to use it, you'll need to create an API client for `genius.com <https://genius.com/api-clients>`_ and get a **CLIENT ACCESS TOKEN**.

Quickstart
----------

Assuming you already have you access token, get an instance of the genius wrapper as follows:

.. code-block:: python

    from genius import Genius
    g = Genius(access_token="YOUR-TOKEN")


With this instance you can interact with genius in many ways:

.. code-block:: python

    # Search for an artist by name
    artist = g.search_artist("Gorillaz")
    print(artist)

    >> "Gorillaz (860)"



.. code-block:: python

    # Get the artist's social media accounts
    instagram = artist.social_media["instagram"]
    print(instagram.handle, instagram.followers)

    >> "gorillaz 2277483"


.. code-block:: python

    # Get the artist's song by popularity
    for song in artist.songs_by_popularity:
        print(song)

    >> "Feel Good Inc. (21569)"
    >> "Clint Eastwood (1698)"
    >> "Saturnz Barz (3027437)"
    >> "Ascension (3027418)"
    >> "On Melancholy Hill (53533)"
    >> ...


.. code-block:: python

    # Get the details of a song by its id
    song = g.get_song(song_id=3027414)
    print(song.title_with_featured)
    print(song.release_date_for_display)

    >> "Andromeda (Ft. DRAM)"
    >> "March 23, 2017"


.. code-block:: python

    # Get the song album, or the featured artists
    print(song.album)
    for featured in song.features:
        print(featured.name)

    >> "Humanz (335930)"
    >> "DRAM (241761)"


.. code-block:: python

    # And even, a song's lyrics
    lyrics = song.lyrics
    print('\n'.join(lyrics))

    >> "[Verse 1: 2-D]"
    >> "When the pulsing looks to die for"
    >> "Take it in your heart now, lover"
    >> "When the case is out"
    >> "And tired and sodden"
    >> "Take it in your heart"
    >> "Take it in your heart"
    >> ...

