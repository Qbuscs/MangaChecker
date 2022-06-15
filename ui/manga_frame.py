import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from list_frame import MangaListFrame

from manga.manga import Manga
from manage import read_file_binary
import webbrowser


class MangaFrame(tk.Frame):
    read_icon_bytes = read_file_binary("ui/static/green_dot.png")
    not_read_icon_bytes = read_file_binary("ui/static/yellow_dot.png")
    cross_icon_bytes = read_file_binary("ui/static/cross.png")

    def __init__(self, container: ttk.Widget, manga: Manga, bg: str):
        super().__init__(container)
        self.manga = manga
        self.parent: MangaListFrame = self.master.master.master
        self.columnconfigure(0, weight=6)
        self.columnconfigure(1, weight=1)
        self.config(bg=bg)
        self.name_label = tk.Label(self, text=self.manga.name, bg=bg, fg="#ffffff")
        self.name_label.grid(column=0, row=0, sticky=tk.W)

        self.chapter_label = tk.Label(self, text=self.manga.latest_chapter, bg=bg, fg="#ffffff")
        self.chapter_label.grid(column=0, row=1, sticky=tk.W)

        self.not_read_icon = tk.PhotoImage(data=self.not_read_icon_bytes, format="png")
        self.read_icon = tk.PhotoImage(data=self.read_icon_bytes, format="png")
        if self.manga.read:
            self.read_anchor = tk.Label(self, image=self.read_icon, bg=bg)
        else:
            self.read_anchor = tk.Label(self, image=self.not_read_icon, bg=bg)
        self.read_anchor.grid(column=1, row=0, sticky=tk.E)
        self.read_anchor.bind("<Button-1>", self._mark_as_read)

        self.cross_icon = tk.PhotoImage(data=self.cross_icon_bytes, format="png")
        self.cross_anchor = tk.Label(self, image=self.cross_icon, bg=bg)
        self.cross_anchor.grid(column=1, row=1, sticky=tk.E)
        self.cross_anchor.bind("<Button-1>", self._delete)

        self.bind("<Double-Button-1>", lambda e: webbrowser.open(self.manga.link))
    
    def _mark_as_read(self, event):
        self.manga.read = not self.manga.read
        self.parent.save_mangas()
        if self.manga.read:
            self.read_anchor["image"] = self.read_icon
        else:
            self.read_anchor["image"] = self.not_read_icon
    
    def _delete(self, event):
        if askyesno("Removal", f"Are you sure you want to remove \"{self.manga.name}\" from the watchlist?"):
            self.parent.delete_manga(self.manga)
            self.destroy()
