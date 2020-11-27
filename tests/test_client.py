import unittest
import os
import json
import requests

import responses

from geniuses import GeniusClient

TOKEN = "<your_token>"


class TestClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._client = GeniusClient(TOKEN)

        replay_folder = os.path.join(os.path.dirname(__file__), "replay_data")
        for file_name in os.listdir(replay_folder):
            with open(os.path.join(replay_folder, file_name), "r+") as f:
                url, method, status, data, *_ = f.read().split("\n")
                status = int(status)
                data = json.loads(data)
                responses.add(method, url, json=data, status=status)
                print(f"replay loaded: {url} {method}")
        replay_folder = os.path.join(os.path.dirname(__file__), "replay_pages")
        for file_name in os.listdir(replay_folder):
            with open(os.path.join(replay_folder, file_name), "r+") as f:
                url = "https://genius.com/" + file_name
                responses.add("GET", url, body=f.read(), status=status)
        responses.start()

    @classmethod
    def tearDownClass(cls):
        responses.stop()
        responses.reset()

    def test_get_artist(self):
        artist = self._client.get_artist(482418)
        self.assertEqual(artist.name, "King Gizzard & The Lizard Wizard")
        self.assertEqual(artist.id, 482418)
        self.assertEqual(
            artist.image_url,
            "https://images.genius.com/44f7d4461b96531b596c6d2608357d3c.1000x1000x1.jpg",
        )
        self.assertEqual(artist.is_verified, False)

    def test_get_song(self):
        song = self._client.get_song(2905339)
        self.assertEqual(song.id, 2905339)
        self.assertEqual(song.title, "Rattlesnake")
        self.assertEqual(
            song.url,
            "https://genius.com/King-gizzard-and-the-lizard-wizard-rattlesnake-lyrics",
        )
        self.assertEqual(
            song.full_title, "Rattlesnake by King Gizzard & The Lizard Wizard"
        )
        self.assertEqual(
            song.path, "/King-gizzard-and-the-lizard-wizard-rattlesnake-lyrics"
        )

    def test_search(self):
        songs = self._client.search("king gizzard")
        self.assertEqual(len(songs), 10)
        self.assertEqual(songs[0].title, "Robot Stop")
        self.assertEqual(
            songs[0].primary_artist.name, "King Gizzard & The Lizard Wizard"
        )
        self.assertEqual(songs[0].primary_artist.id, 482418)

    def test_search_songs(self):
        songs = list(self._client.search_songs("sagapo", per_page=17))
        self.assertEqual(len(songs), 24)
        self.assertEqual(songs[0].title, "Sagapò")
        self.assertEqual(songs[0].title_with_featured, "Sagapò")
        self.assertEqual(songs[0].lyrics_state, "complete")
        self.assertEqual(
            songs[0].song_art_image_thumbnail_url,
            "https://images.genius.com/fe1f9dc6ce12688088f73c3bc842ee3a.300x305x1.jpg",
        )
        self.assertEqual(
            songs[0].song_art_image_url,
            "https://images.genius.com/fe1f9dc6ce12688088f73c3bc842ee3a.720x731x1.jpg",
        )
        self.assertEqual(
            songs[0].header_image_thumbnail_url,
            "https://images.genius.com/fe1f9dc6ce12688088f73c3bc842ee3a.300x305x1.jpg",
        )
        self.assertEqual(
            songs[0].header_image_url,
            "https://images.genius.com/fe1f9dc6ce12688088f73c3bc842ee3a.720x731x1.jpg",
        )

    def test_search_artists(self):
        artists = list(self._client.search_artists("khruangbin"))
        self.assertEqual(len(artists), 3)
        self.assertEqual(artists[0].is_meme_verified, False)
        self.assertEqual(
            artists[0].header_image_url,
            "https://images.genius.com/ed71b56e3cfb02c0065484270520e815.885x410x1.jpg",
        )
        self.assertEqual(artists[0].url, "https://genius.com/artists/Khruangbin")

    def test_get_artist_songs(self):
        artist = self._client.get_artist(672700)
        songs = list(artist.get_songs(per_page=19))
        self.assertEqual(len(songs), 59)
        self.assertEqual(songs[11].title, "Cómo Te Quiero")

    def test_get_song_lyrics(self):
        song = self._client.get_song(2905339)
        self.assertEqual(song.lyrics.lower().count("rattlesnake"), 51)
        self.assertTrue(song.lyrics.startswith("[Hook]\nRattlesnake, rattlesnake"))
