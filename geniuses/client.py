from typing import List
from urllib.parse import urljoin

from requests import Response, Session

from .model import Artist, Song


class GeniusSession(Session):
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
        # headers = {"Authorization": f"Bearer {self.access_token}"}
        # headers.update(kwargs.pop("headers", {}))
        # kwargs["headers"] = headers
        response = super().request(method, urljoin(self.host, path), *args, **kwargs)
        response.raise_for_status()
        return response


class GeniusClient:
    def __init__(self, access_token: str):
        """Initialize the API Client to make requests

        Args:
            access_token: a string containing the authentication token for the REST API.
        """
        self._session = GeniusSession(access_token)

    def search(self, query: str) -> List[Song]:
        response = self._session.request("get", "search", params={"q": query})
        data = response.json()
        return [
            Song(hit["result"])
            for hit in data["response"]["hits"]
            if hit["type"] == "song"
        ]

    def get_artist(self, id: int) -> Artist:
        response = self._session.request(
            "get", f"artists/{id}", params={"text_format": "plain"}
        )
        data = response.json()
        return Artist(data["response"]["artist"])

    def get_song(self, id: int) -> Song:
        response = self._session.request(
            "get", f"songs/{id}", params={"text_format": "plain"}
        )
        data = response.json()["response"]["song"]
        return Song(data)
