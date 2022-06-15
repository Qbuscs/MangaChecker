import enum
import json
import tkinter as tk


class GeometryAction(enum.Enum):
    DRAG = 0
    RESIZE_RIGHT = 1
    RESIZE_LEFT = 2
    RESIZE_BOTTOM = 3
    RESIZE_RIGHT_BOTTOM = 4
    RESIZE_LEFT_BOTTOM = 5


class WindowGeometryManager:
    def __init__(self, window: tk.Tk):
        self.window = window
        self.last_click_x = 0
        self.last_click_y = 0
        self.action = None

    def clear_action(self, event):
        self.save_position_config()
        self.action = None
    
    def save_position_config(self):
        with open("ui/config.json", "r+") as f:
            json_raw = f.read()
            config = json.loads(json_raw)
            config["pos_x"] = self.window.winfo_x()
            config["pos_y"] = self.window.winfo_y()
            config["width"] = self.window.winfo_width()
            config["height"] = self.window.winfo_height()
            f.seek(0)
            f.truncate()
            f.write(json.dumps(config))
    
    def save_last_click_pos(self, event):
        self.last_click_x = event.x
        self.last_click_y = event.y
        touched_bottom = event.y >= self.window.winfo_height() - 10
        touched_right = event.x >= self.window.winfo_width() - 10
        touched_left = event.x <= 10
        if touched_right and touched_bottom:
            self.action = GeometryAction.RESIZE_RIGHT_BOTTOM
        elif touched_left and touched_bottom:
            self.action = GeometryAction.RESIZE_LEFT_BOTTOM
        elif touched_right:
            self.action = GeometryAction.RESIZE_RIGHT
        elif touched_left:
            self.action = GeometryAction.RESIZE_LEFT
        elif touched_bottom:
            self.action = GeometryAction.RESIZE_BOTTOM
        else:
            self.action = GeometryAction.DRAG

    def geometry_manipulation(self, event):
        if self.action == GeometryAction.RESIZE_RIGHT:
            self.resize_right(event)
        elif self.action == GeometryAction.RESIZE_LEFT:
            self.resize_left(event)
        elif self.action == GeometryAction.RESIZE_BOTTOM:
            self.resize_bottom(event)
        elif self.action == GeometryAction.RESIZE_LEFT_BOTTOM:
            self.resize_left_bottom(event)
        elif self.action == GeometryAction.RESIZE_RIGHT_BOTTOM:
            self.resize_right_bottom(event)
        elif self.action == GeometryAction.DRAG:
            self.dragging(event)

    def resize_right(self, event):
        self.window.geometry(f"{event.x + 1}x{self.window.winfo_height()}")
    
    def resize_bottom(self, event):
        self.window.geometry(f"{self.window.winfo_width()}x{event.y + 1}")
    
    def resize_right_bottom(self, event):
        self.window.geometry(f"{event.x + 1}x{event.y + 1}")
    
    def resize_left_bottom(self, event):
        width = self.window.winfo_width() - event.x
        x = self.window.winfo_x() + event.x
        self.window.geometry(f"{width}x{event.y + 1}+{x}+{self.window.winfo_y()}")
    
    def resize_left(self, event):
        width = self.window.winfo_width() - event.x
        x = self.window.winfo_x() + event.x
        self.window.geometry(f"{width}x{self.window.winfo_height()}+{x}+{self.window.winfo_y()}")

    def dragging(self, event):
        x, y = event.x - self.last_click_x + self.window.winfo_x(), event.y - self.last_click_y + self.window.winfo_y()
        self.window.geometry("+%s+%s" % (x, y))
        