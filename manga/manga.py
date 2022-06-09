import abc
from typing import Dict, Tuple, TypeVar

import requests
from bs4 import BeautifulSoup


class ConnectionException(Exception):
    pass


class PageParseException(Exception):
    pass


T = TypeVar("T", bound="Manga")

class Manga:
    __metaclass__ = abc.ABCMeta
    MANGA_FOX = "MangaFox"

    @abc.abstractmethod
    def __init__(self, name: str, link: str, latest_chapter: str, read: bool):
        self.name = name
        self.latest_chapter = latest_chapter
        self.read = read
        self.link = link
        self.website = None

    def _fetch_soup(self) -> BeautifulSoup:
        page = requests.get(self.link)
        if page.status_code != 200:
            raise ConnectionException
        return BeautifulSoup(page.text, "html.parser")

    @abc.abstractmethod
    def _get_page_specific_latest_chapter(self, soup: BeautifulSoup) -> Tuple[str, str]:
        pass

    def _get_latest_chapter(self) -> Tuple[str, str]:
        soup = self._fetch_soup()
        try:
            return self._get_page_specific_latest_chapter(soup)
        except Exception:
            raise PageParseException

    def update(self) -> bool:
        latest_chapter, link = self._get_latest_chapter()
        if latest_chapter == self.latest_chapter:
            return False
        self.latest_chapter = latest_chapter
        self.link = link
        self.read = False
        return True
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "latest_chapter": self.latest_chapter,
            "read": self.read,
            "link": self.link,
            "website": self.website
        }
