import time

from manage import MangaAlreadyAddedException, add_manga, remove_manga
from manga.manga import Manga
from update_thread import UpdateThread


def add(name: str, url: str, website: str) -> bool:
    try:
        add_manga(name, url, website)
        return True
    except MangaAlreadyAddedException:
        print("Manga already in list. Aborting.")
        return False

def main():
    add("Onepunch-man", "http://fanfox.net/manga/onepunch_man/vTBD/c164.2/1.html", Manga.MANGA_FOX)
    add("One Piece", "http://fanfox.net/manga/one_piece/vTBE/c1051/1.html#itop", Manga.MANGA_FOX)
    up_thread = UpdateThread()
    up_thread.daemon = True
    up_thread.start()
    #remove_manga("One Piece")
    time.sleep(30)

if __name__ == "__main__":
    main()
    print("main finished")
