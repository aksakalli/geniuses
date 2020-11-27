import os
from itertools import islice

from .client import GeniusClient


client = GeniusClient(os.environ.get("GENIUS_API_TOKEN"))

OPTIONS_WARNING_MSG = "Please enter a valid number for the given options"

artists = None
while not artists:
    query = input("Search an artist: ")
    artists = list(islice(client.search_artists(query), 10))

for i, artist in enumerate(artists, 1):
    print(f"{i}. {artist.name}")
selected_artist = None
while not selected_artist:
    artist_input = input("Select an artist: ")
    try:
        selected_artist = artists[int(artist_input) - 1]
    except (ValueError, IndexError):
        print(OPTIONS_WARNING_MSG)

print(f"Selected artist: {selected_artist.name}, here are the songs:")

i = 1
available_songs = []
selected_song = None
for song in selected_artist.get_songs(sort="popularity"):
    available_songs.append(song)
    print(f"{i}. {song.title}")
    if i % 10 == 0:
        while not selected_song and artist_input != "":
            artist_input = input("Select a song (or hit enter for more options): ")
            if artist_input == "":
                break
            try:
                selected_song = available_songs[int(artist_input) - 1]
            except (ValueError, IndexError):
                print(OPTIONS_WARNING_MSG)
        if selected_song:
            break
        else:
            artist_input = None
    i += 1
else:
    while selected_song:
        artist_input = input("These are all the songs, select one: ")
        try:
            selected_song = available_songs[int(artist_input) - 1]
        except (ValueError, IndexError):
            print(OPTIONS_WARNING_MSG)

print("here is the song Lyrics:\n\n")
print("-----------")
print(selected_song.full_title)
print("-----------")
print(selected_song.lyrics)
