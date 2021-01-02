import tkinter as tk
import threading

import ui_handler

SCREEN_SIZE = (640, 480)

class UI:
    """
    Manages Interaction with the User Interface.
    """
    __instance = None
    __singleton_lock = threading.Lock()

    @classmethod
    def getInstance(cls):
        with cls.__singleton_lock:
            if cls.__instance is None:
                cls.__instance = cls()
            return cls.__instance
    
    def __init__(self):
        """Not meant to be used directly, use getInstance() instead."""
        if not self.__class__.__singleton_lock.locked():
            raise AttributeError("Use UI.getInstance() instead of calling "
                "constructor.")
        self.window = tk.Tk()
        self.window_lock = threading.Lock()
        self.window.geometry('{}x{}'.format(SCREEN_SIZE[0], SCREEN_SIZE[1]))
        self.handler = ui_handler.UIHandler()

    def start(self):
        with self.window_lock:
            self.draw()
            self.window.mainloop()

    def draw(self):
        self.draw_upload()

    def draw_upload(self):
        button = tk.Button(self.window, text='Open File', command=self.handler.open_file)
        button.pack(side = tk.TOP)


if __name__ == "__main__":
    ui = UI.getInstance()
    ui.start()