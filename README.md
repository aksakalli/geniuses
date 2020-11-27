# Genius Lyrics API Python Client

[![Travis (.org)](https://img.shields.io/travis/aksakalli/geniuses)](https://travis-ci.org/aksakalli/geniuses)
[![Coverage Status](https://img.shields.io/codecov/c/github/aksakalli/geniuses/master.svg)](https://codecov.io/github/aksakalli/geniuses?branch=master)

A Lightweight client for typed interaction with [Genius API](https://docs.genius.com/).

## Examples

```
from geniuses import GeniusClient

client = GeniusClient("<your_token>")
songs = client.search("Cariñito los hijos")

print(songs[0].primary_artist.name)  # Los hijos del sol
print(songs[0].lyrics)  # Lloro por quererte ...

songs_from_artist = list(songs[0].primary_artist.get_songs())
print(songs_from_artist)  # [<Song(title=Cariñito, id=1949442)>, <Song(title=Si Me Quieres, id=2078361)>]
```

## CLI

WIP

## Development

This project uses [tox](https://tox.readthedocs.io/en/latest/) for running tests and
other things (style check, coverage reports).

It is recommended to install [conda](https://docs.conda.io/en/latest/miniconda.html)
along with [tox-conda](https://github.com/tox-dev/tox-conda) for using tox.
Afterwards, `tox` command will run all the steps for you.

This project strictly uses [black](https://github.com/psf/black) as an opinionated code style.
Any written line should comply with that (don’t forget to run `black .` for PRs).


## License

Released under [the Apache License](LICENSE).
