import tkinter as tk
from tkinter.messagebox import showerror
import requests
from manga.manga import Manga
from manage import add_manga, MangaAlreadyAddedException


class AddMangaFrame(tk.Frame):
    def __init__(self, container: tk.Widget, bg_color: str):
        super().__init__(container)
        self.bg_color = bg_color
        self.configure(bg=self.bg_color)
        self.grid_columnconfigure(1, weight=1)
    
    def build(self):
        self.name_label = tk.Label(self, text="Name", bg=self.bg_color, fg="#ffffff")
        self.name_label.grid(column=0, row=0, padx=5, pady=2)
        self.name_input = tk.Text(self, height=1)
        self.name_input.grid(column=1, row=0, padx=5, pady=2, columnspan=3)

        self.url_label = tk.Label(self, text="URL", bg=self.bg_color, fg="#ffffff")
        self.url_label.grid(column=0, row=1, padx=5, pady=2)
        self.url_input = tk.Text(self, height=1)
        self.url_input.grid(column=1, row=1, padx=5, pady=2, columnspan=3)

        self.cancel_button = tk.Button(self, text="Cancel", command=self.cancel_action)
        self.cancel_button.grid(column=2, row=2, pady=2)
        self.add_button = tk.Button(self, text="Add", command=self.add_action)
        self.add_button.grid(column=3, row=2, padx=5, pady=2)

    def _clear(self):
        for frame in self.winfo_children():
            frame.destroy()
        self.configure(height=1)
        

    def cancel_action(self):
        self._clear()
        self.configure(height=0)
    
    def add_action(self):
        name = self.name_input.get("1.0", "end")
        name = self._format_input(name)
        url = self.url_input.get("1.0", "end")
        url = self._format_input(url)
        type = Manga.MANGA_FOX  # TODO
        if not self._validate_input(name, url):
            return
        try:
            add_manga(name, url, type)
        except MangaAlreadyAddedException:
            showerror("Error", f"Manga named \"{name}\" already added to the watchlist.")
        self.master.refresh_manga_list()
        self._clear()
    
    def _format_input(self, input: str):
        input = input.replace("\n", "")
        input = input.strip()
        return input
        
    def _validate_input(self, name: str, url: str):
        if not name:
            showerror("Error", "No manga name entered.")
            return False
        if not url:
            showerror("Error", "No URL to manga site entered.")
            return False
        try:
            status_code = requests.get(url, timeout=7).status_code
        except requests.exceptions.RequestException:
            showerror(
                "Error", 
                "Could not connect to provided link. Please check your internet connection, " +\
                "or make sure the URL was entered properly."
            )
        if not status_code == 200:
            showerror("Error", "Could not connect to provided link. Please make sure it was entered properly.")
            return False
        return True
