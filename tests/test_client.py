import unittest
import os
import json
import requests

import responses

import geniuses

TOKEN = "<your_token>"


class TestClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._client = geniuses.GeniusClient(TOKEN)
        replay_folder = os.path.join(os.path.dirname(__file__), "replay_data")
        print(replay_folder)
        for file_name in os.listdir(replay_folder):
            print(f"loading replay {file_name}")
            with open(os.path.join(replay_folder, file_name), "r+") as f:
                url, method, status, data, *_ = f.read().split("\n")
                status = int(status)
                data = json.loads(data)
                responses.add(method, url, json=data, status=status)
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

    def test_search(self):
        songs = self._client.search("king gizzard")
        self.assertEqual(len(songs), 10)
        self.assertEqual(songs[0].title, "Robot Stop")
        self.assertEqual(
            songs[0].primary_artist.name, "King Gizzard & The Lizard Wizard"
        )
        self.assertEqual(songs[0].primary_artist.id, 482418)
