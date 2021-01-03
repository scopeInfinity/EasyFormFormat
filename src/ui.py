import tkinter as tk
import threading

import ui_handler

SCREEN_SIZE = (640, 480)

def destroyanddraw(func):
    """Decorator to destroy widgets before redrawing them."""
    def newfunc(self):
        attr = "__{}_pack".format(func.__name__)
        if hasattr(self, attr):
            for ele in getattr(self, attr):
                ele.destroy()

        setattr(self, attr, func(self))
    return newfunc


def drawonce(func):
    """Decorator to draw widgets once."""
    def newfunc(self):
        attr = "__{}_drawn".format(func.__name__)
        if hasattr(self, attr):
            return
        func(self)
        setattr(self, attr, True)
    return newfunc

def getInstance():
    return UI.getInstance()

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
        self.data = []

    def start(self):
        self.draw()
        self.window.mainloop()

    def update(self, filenames):
        self.data = list(filenames)
        self.draw()

    def draw(self):
        self.draw_buttons()
        self.draw_labels()

    @drawonce
    def draw_buttons(self):
        button = tk.Button(self.window, text='Open File', command=self.handler.open_file)
        button.pack(side=tk.TOP)

    @destroyanddraw
    def draw_labels(self):
        pack = []
        for d in self.data:
            label = tk.Label(self.window, text=d)
            label.pack(side=tk.TOP)
            pack.append(label)
        return pack
