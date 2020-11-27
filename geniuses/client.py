from typing import List, Iterable
from urllib.parse import urljoin

from requests import Response, Session

from .model import Artist, Song
from .errors import UnauthorizedRequestError


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
        if response.status_code == 401:
            raise UnauthorizedRequestError
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
        headers = {
            "application": "geniuses",
            "User-Agent": "https://github.com/aksakalli/geniuses",
        }
        headers.update(kwargs.pop("headers", {}))
        kwargs["headers"] = headers
        response = super().request(method, urljoin(self.host, path), *args, **kwargs)
        response.raise_for_status()
        return response


class GeniusClient:
    def __init__(self, access_token: str):
        """Initialize the API Client to make requests

        :param access_token: Authentication token for the REST API
        """
        self._api_session = GeniusApiSession(access_token)
        self._web_session = GeniusWebSession()

    def search(self, query: str) -> List[Song]:
        """Search songs hosted on Genius.

        :param query: The term to search for
        :returns: A list of song results
        """
        response = self._api_session.request("get", "search", params={"q": query})
        data = response.json()
        return [
            Song(hit["result"], self._api_session, self._web_session)
            for hit in data["response"]["hits"]
            if hit["type"] == "song"
        ]

    def get_artist(self, id: int) -> Artist:
        """Get an artist object from ID

        :param id: ID of the artist
        :returns: Artist object
        """
        response = self._api_session.request(
            "get", f"artists/{id}", params={"text_format": "plain"}
        )
        data = response.json()
        return Artist(data["response"]["artist"], self._api_session, self._web_session)

    def get_song(self, id: int) -> Song:
        """Get an song object from ID

        :param id: ID of the song
        :returns: Song object
        """
        response = self._api_session.request(
            "get", f"songs/{id}", params={"text_format": "plain"}
        )
        data = response.json()["response"]["song"]
        return Song(data, self._api_session, self._web_session)

    def search_songs(self, q: str, per_page=10) -> Iterable[Song]:
        """Search songs hosted on Genius using https://genius.com/api/search/song

        :param query: The term to search for
        :param per_page: Number of results to return per request
        :returns: An Iterable of song results
        """
        page = 1
        while page != None:
            response = self._web_session.request(
                "GET",
                "/api/search/song",
                params={"page": page, "per_page": per_page, "q": q},
            )
            data = response.json()["response"]
            page = data["next_page"]
            for hit in data["sections"][0]["hits"]:
                yield Song(hit["result"], self._api_session, self._web_session)

    def search_artists(self, q: str, per_page=10) -> Iterable[Artist]:
        """Search artists hosted on Genius using https://genius.com/api/search/song

        :param query: The term to search for
        :param per_page: Number of results to return per request
        :returns: An Iterable of artist results
        """
        page = 1
        while page != None:
            response = self._web_session.request(
                "GET",
                "/api/search/artist",
                params={"page": page, "per_page": per_page, "q": q},
            )
            data = response.json()["response"]
            page = data["next_page"]
            for hit in data["sections"][0]["hits"]:
                yield Artist(hit["result"], self._api_session, self._web_session)
