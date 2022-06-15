import tkinter as tk


class TopMenuFrame(tk.Frame):
    def __init__(self, container: tk.Widget, bg_color: str):
        super().__init__(container)

        self.configure(bg=bg_color)

        self.exit_icon = tk.PhotoImage(file="ui/static/exit.png")
        self.exit_anchor = tk.Label(self, image=self.exit_icon, bg=bg_color)
        self.exit_anchor.pack(side="right")
        self.exit_anchor.bind("<Button-1>", lambda e: container.quit())

        self.add_icon = tk.PhotoImage(file="ui/static/add.png")
        self.add_anchor = tk.Label(self, image=self.add_icon, bg=bg_color)
        self.add_anchor.pack(side="right")
        self.add_anchor.bind("<Button-1>", self._add_manga)
    
    def _add_manga(self, event):
        self.master.show_add_manga_frame()
