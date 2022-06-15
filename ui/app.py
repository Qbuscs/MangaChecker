import json
import tkinter as tk
from ctypes import windll
from typing import Dict

from ui.list_frame import MangaListFrame
from ui.add_manga_frame import AddMangaFrame
from ui.top_menu_frame import TopMenuFrame
from ui.window_geometry_manager import WindowGeometryManager


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.bg_color = "#333333"

        self.title("Manga Watcher")
        self._set_starting_geometry()
        self.iconbitmap("ui/static/icon.ico")
        self.configure(bg=self.bg_color)

        self.hide_windows_toolbar()

        self.top_menu_frame = TopMenuFrame(self, self.bg_color)
        self.top_menu_frame.pack(fill="x")

        self.add_manga_frame = AddMangaFrame(self, "#555555")
        self.add_manga_frame.pack(side="top", fill="x", pady=10)

        self.manga_list_frame = MangaListFrame(self, self.bg_color)
        self.manga_list_frame.pack(fill="x", pady=10)

    def show_add_manga_frame(self):
        self.add_manga_frame.build()
    
    def refresh_manga_list(self):
        self.manga_list_frame.refresh(mute=True)
        
    def hide_windows_toolbar(self):
        self.overrideredirect(True)
        self.after(10, self._set_appwindow)

        self.geometry_manager = WindowGeometryManager(self)
        self.bind("<Button-1>", self.geometry_manager.save_last_click_pos)
        self.bind("<B1-Motion>", self.geometry_manager.geometry_manipulation)
        self.bind("<ButtonRelease-1>", self.geometry_manager.clear_action)
    
    def _set_appwindow(self):
        GWL_EXSTYLE = -20
        WS_EX_APPWINDOW = 0x00040000
        WS_EX_TOOLWINDOW = 0x00000080
        hwnd = windll.user32.GetParent(self.winfo_id())
        style = windll.user32.GetWindowLongPtrW(hwnd, GWL_EXSTYLE)
        style = style & ~WS_EX_TOOLWINDOW
        style = style | WS_EX_APPWINDOW
        windll.user32.SetWindowLongPtrW(hwnd, GWL_EXSTYLE, style)
        # re-assert the new window style
        self.withdraw()
        self.after(10, self.deiconify)
    
    def _set_starting_geometry(self):
        with open("ui/config.json", "r") as f:
            config: Dict = json.loads(f.read())
        if not isinstance(config, dict):
            return

        if "width" in config and "height" in config:
            self.geometry(f"{config['width']}x{config['height']}")
        else:
            self.geometry("185x300")
        
        if "pos_x" in config and "pos_y" in config:
            self.geometry(f"+{config['pos_x']}+{config['pos_y']}")
