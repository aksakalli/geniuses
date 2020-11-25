from typing import List, Iterable
from urllib.parse import urljoin

from requests import Response, Session

from .model import Artist, Song


class GeniusApiSession(Session):
    """HTTP session for Genius API calls

    It helps with hostname and token.
    """

    host: str = "https://api.genius.com"

    def __init__(self, access_token: str) -> None:
        """Initialize the authentication.
        Args:
            access_token: a string containing the authentication token for the REST API.
        """
        super().__init__()
        self.access_token = access_token

    def request(self, method: str, path: str, *args: str, **kwargs: int) -> Response:
        """Make a HTTP request to API"""
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/json",
        }
        headers.update(kwargs.pop("headers", {}))
        kwargs["headers"] = headers
        response = super().request(method, urljoin(self.host, path), *args, **kwargs)
        response.raise_for_status()
        return response


class GeniusWebSession(Session):
    """HTTP session for Genius API calls

    It helps with hostname and token.
    """

    host: str = "https://genius.com"

    def __init__(self) -> None:
        """Initialize the authentication.
        Args:
            access_token: a string containing the authentication token for the REST API.
        """
        super().__init__()

    def request(self, method: str, path: str, *args: str, **kwargs: int) -> Response:
        """Make a HTTP request to API"""
        response = super().request(method, urljoin(self.host, path), *args, **kwargs)
        response.raise_for_status()
        return response


class GeniusClient:
    def __init__(self, access_token: str):
        """Initialize the API Client to make requests

        Args:
            access_token: a string containing the authentication token for the REST API.
        """
        self._apiSession = GeniusApiSession(access_token)
        self._webSession = GeniusWebSession()

    def search(self, query: str) -> List[Song]:
        response = self._apiSession.request("get", "search", params={"q": query})
        data = response.json()
        return [
            Song(hit["result"])
            for hit in data["response"]["hits"]
            if hit["type"] == "song"
        ]

    def get_artist(self, id: int) -> Artist:
        response = self._apiSession.request(
            "get", f"artists/{id}", params={"text_format": "plain"}
        )
        data = response.json()
        return Artist(data["response"]["artist"])

    def get_song(self, id: int) -> Song:
        response = self._apiSession.request(
            "get", f"songs/{id}", params={"text_format": "plain"}
        )
        data = response.json()["response"]["song"]
        return Song(data)

    def search_songs(self, q: str, per_page=10) -> List[Song]:
        page = 1
        while page != None:
            response = self._webSession.request(
                "GET",
                "/api/search/song",
                params={"page": page, "per_page": per_page, "q": q},
            )
            data = response.json()["response"]
            page = data["next_page"]
            for song_hits in data["sections"][0]["hits"]:
                yield Song(song_hits["result"])

    def search_artists(self, q: str, per_page=10) -> List[Artist]:
        page = 1
        while page != None:
            response = self._webSession.request(
                "GET",
                "/api/search/artist",
                params={"page": page, "per_page": per_page, "q": q},
            )
            data = response.json()["response"]
            page = data["next_page"]
            for song_hits in data["sections"][0]["hits"]:
                yield Artist(song_hits["result"])
