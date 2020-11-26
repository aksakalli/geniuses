class Artist(object):
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

    def __init__(self, raw_dict):
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

    def get_songs(self):
        pass


class Song(object):
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

    def __init__(self, raw_dict):
        self._id = raw_dict["id"]
        self._title = raw_dict["title"]
        self._title_with_featured = raw_dict["title_with_featured"]
        self._full_title = raw_dict["full_title"].replace("\xa0", " ")
        self._lyrics_state = raw_dict["lyrics_state"]
        self._song_art_image_thumbnail_url = raw_dict["song_art_image_thumbnail_url"]
        self._song_art_image_url = raw_dict["song_art_image_url"]
        self._header_image_thumbnail_url = raw_dict["header_image_thumbnail_url"]
        self._header_image_url = raw_dict["header_image_url"]
        self._primary_artist = Artist(raw_dict["primary_artist"])
        self._url = raw_dict["url"]

    def __repr__(self) -> str:
        return "<{}(title={}, id={})>".format(
            self.__class__.__name__, self.title, self.id
        )
