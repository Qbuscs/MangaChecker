from typing import Tuple

from bs4 import BeautifulSoup

from .manga import Manga


class MangaFox(Manga):
    def __init__(self, name: str, link: str, latest_chapter: str, read: bool):
        super().__init__(name, link, latest_chapter, read)
        self.website = Manga.MANGA_FOX
        self.base_url = "http://fanfox.net"

    def _get_page_specific_latest_chapter(self, soup: BeautifulSoup) -> Tuple[str, str]:
        chapters = soup.find(class_="reader-header-title-list")
        chapters = chapters.find_all("a")
        latest = chapters[-1]
        link = self.base_url + latest["href"]
        chapter = latest.text
        return chapter, link
