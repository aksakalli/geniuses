from abc import ABC, abstractmethod
from typing import Iterable

import re

from bs4 import BeautifulSoup


class GeniusBase(object):
    def __init__(self, raw_dict, api_session, web_session):
        self._api_session = api_session
        self._web_session = web_session
        self._init_attributes(raw_dict)

    @abstractmethod
    def _init_attributes(self, raw_dict):
        return


class Artist(GeniusBase):
    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def image_url(self) -> str:
        return self._image_url

    @property
    def header_image_url(self) -> str:
        return self._header_image_url

    @property
    def is_verified(self) -> bool:
        return self._is_verified

    @property
    def is_meme_verified(self) -> bool:
        return self._is_meme_verified

    @property
    def url(self) -> str:
        return self._url

    def get_songs(self, per_page=10, sort="title") -> "Iterable[Song]":
        assert sort in ["title", "popularity"]
        page = 1
        while page != None:
            response = self._api_session.request(
                "GET",
                f"artists/{self.id}/songs",
                params={"page": page, "per_page": per_page, "sort": sort},
            )
            data = response.json()["response"]
            page = data["next_page"]
            for song in data["songs"]:
                yield Song(song, self._api_session, self._web_session)

    def _init_attributes(self, raw_dict):
        self._id = raw_dict["id"]
        self._name = raw_dict["name"]
        self._image_url = raw_dict["image_url"]
        self._header_image_url = raw_dict["header_image_url"]
        self._is_verified = raw_dict["is_verified"]
        self._is_meme_verified = raw_dict["is_meme_verified"]
        self._url = raw_dict["url"]

    def __repr__(self) -> str:
        return "<{}(name={}, id={})>".format(
            self.__class__.__name__, self.name, self.id
        )


class Song(GeniusBase):
    @property
    def id(self) -> int:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @property
    def title_with_featured(self) -> str:
        return self._title_with_featured

    @property
    def full_title(self) -> str:
        return self._full_title

    @property
    def lyrics_state(self) -> str:
        return self._lyrics_state

    @property
    def song_art_image_thumbnail_url(self) -> str:
        return self._song_art_image_thumbnail_url

    @property
    def song_art_image_url(self) -> str:
        return self._song_art_image_url

    @property
    def header_image_thumbnail_url(self) -> str:
        return self._header_image_thumbnail_url

    @property
    def header_image_url(self) -> str:
        return self._header_image_url

    @property
    def primary_artist(self) -> Artist:
        return self._primary_artist

    @property
    def url(self) -> str:
        return self._url

    @property
    def path(self) -> str:
        return self._path

    @property
    def lyrics(self) -> str:
        if self._lyrics == None:
            response = self._web_session.request("GET", self.path)
            soup = BeautifulSoup(response.content, "html.parser")
            lyrics_div = soup.find("div", class_=re.compile("^lyrics$|Lyrics__Root"))
            if lyrics_div:
                self._lyrics = lyrics_div.get_text(separator="\n")
            else:
                self._lyrics = ""

        return self._lyrics

    def _init_attributes(self, raw_dict):
        self._id = raw_dict["id"]
        self._title = raw_dict["title"]
        self._title_with_featured = raw_dict["title_with_featured"]
        self._full_title = raw_dict["full_title"].replace("\xa0", " ")
        self._lyrics_state = raw_dict["lyrics_state"]
        self._song_art_image_thumbnail_url = raw_dict["song_art_image_thumbnail_url"]
        self._song_art_image_url = raw_dict["song_art_image_url"]
        self._header_image_thumbnail_url = raw_dict["header_image_thumbnail_url"]
        self._header_image_url = raw_dict["header_image_url"]
        self._primary_artist = Artist(
            raw_dict["primary_artist"], self._api_session, self._web_session
        )
        self._url = raw_dict["url"]
        self._path = raw_dict["path"]
        self._lyrics = None

    def __repr__(self) -> str:
        return "<{}(title={}, id={})>".format(
            self.__class__.__name__, self.title, self.id
        )
