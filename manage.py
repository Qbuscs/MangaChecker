import json
from typing import List, Tuple

from manga.manga import ConnectionException, Manga, PageParseException
from manga.manga_fox import MangaFox


class MangaAlreadyAddedException(Exception):
    pass

def get_manga_list() -> List[Manga]:
    with open("manga/manga_progress.json", "r") as file:
        manga_json = file.read()
    manga_list_raw = json.loads(manga_json)
    manga_list = []

    for manga in manga_list_raw:
        if manga["website"] == Manga.MANGA_FOX:
            manga_list.append(MangaFox(
                manga["name"], manga["link"], manga["latest_chapter"], manga["read"]
            ))
    
    return manga_list

def save_manga_list(manga_list: List[Manga]) -> None:
    with open("manga/manga_progress.json", "w") as file:
        manga_dict_list = [m.to_dict() for m in manga_list]
        file.write(json.dumps(manga_dict_list, indent=4, separators=(", ", ": ")))

def add_manga(name: str, url: str, website: str) -> None:
    manga_list = get_manga_list()
    if name in [m.name for m in manga_list]:
        raise MangaAlreadyAddedException
    if website == Manga.MANGA_FOX:
        new_manga = MangaFox(name, url, None, False)

    new_manga.update()
    manga_list.append(new_manga)
    save_manga_list(manga_list)
    

def update_manga() -> Tuple[bool, List[str]]:
    manga_list = get_manga_list()
    errors = []
    updated = False
    for manga in manga_list:
        try:
            if manga.update():
                updated = True
        except ConnectionException:
            errors.append(f"Connection error while trying to reach {manga.link}")
        except PageParseException:
            errors.append(f"Error while parsing page {manga.link}")
    save_manga_list(manga_list)
    return updated, errors

def remove_manga(name: str) -> None:
    manga_list = get_manga_list()
    for i, manga in enumerate(manga_list):
        if manga.name == name:
            manga_list.pop(i)
    save_manga_list(manga_list)

def set_as_read(name: str) -> None:
    manga_list = get_manga_list()
    for manga in manga_list:
        if manga.name == name:
            manga.read = True
    save_manga_list(manga_list)

def read_file_binary(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()
