import tkinter as tk
from playsound import playsound

from manage import get_manga_list, save_manga_list
from update_thread import UpdateThread

from ui.manga_frame import MangaFrame
from ui.vertical_scrolled_frame import VerticalScrolledFrame
from typing import List
from manga.manga import Manga


class MangaListFrame(VerticalScrolledFrame):
    def __init__(self, container: tk.Widget, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        #self.configure(bg=bg_color)
        self.manga_frames: List[MangaFrame] = []
        self._fill_frames()
        
        up_thread = UpdateThread(self.refresh)
        up_thread.daemon = True
        up_thread.start()
    
    def _fill_frames(self):
        self.manga_list = get_manga_list()
        for i, manga in enumerate(self.manga_list):
            if i % 2 == 0:
                frame = MangaFrame(self.interior, manga, bg="#333333")
            else:
                frame = MangaFrame(self.interior, manga, bg="#666666")
            frame.pack(fill="x")
            self.manga_frames.append(frame)
    
    def _clear_frames(self):
        for frame in self.manga_frames:
            frame.destroy()

    def refresh(self, mute=False):
        self.manga_list = get_manga_list()
        self._clear_frames()
        self._fill_frames()
        if not mute:
            try:
                playsound("ui/static/notification.mp3")
            except Exception:
                pass

    def save_mangas(self):
        save_manga_list(self.manga_list)

    def delete_manga(self, manga: Manga):
        self.manga_list.remove(manga)
        self.save_mangas()
        self._clear_frames()
        self._fill_frames()
