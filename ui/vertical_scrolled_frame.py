import tkinter as tk
from tkinter import ttk
from tkinter.constants import *

# Based on
#   https://web.archive.org/web/20170514022131id_/http://tkinter.unpythonic.net/wiki/VerticalScrolledFrame

class VerticalScrolledFrame(tk.Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame.
    * Construct and pack/place/grid normally.
    * This frame only allows vertical scrolling.
    """
    def __init__(self, parent, bg_color: str):
        tk.Frame.__init__(self, parent)
        self.configure(bg=bg_color)

        self.canvas = tk.Canvas(
            self, bd=0, highlightthickness=0, background=bg_color
        )
        self.canvas.pack(fill='x')

        # Reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with it.
        self.interior = interior = ttk.Frame(self.canvas)
        interior_id = self.canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

        def _on_mousewheel(event):
            self.canvas.yview_scroll(-1*int(event.delta/120), "units")
        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Track changes to the canvas and frame width and sync them,
        # also updating the scrollbar.
        def _configure_interior(event):
            # Update the scrollbars to match the size of the inner frame.
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            self.canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != self.canvas.winfo_width():
                # Update the canvas's width to fit the inner frame.
                self.canvas.config(width=interior.winfo_reqwidth())
            if interior.winfo_reqheight() != self.canvas.winfo_height():
                self.canvas.config(height=interior.winfo_reqheight())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != self.canvas.winfo_width():
                # Update the inner frame's width to fill the canvas.
                self.canvas.itemconfigure(interior_id, width=self.canvas.winfo_width())
        self.canvas.bind('<Configure>', _configure_canvas)