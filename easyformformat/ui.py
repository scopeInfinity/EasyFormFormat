import tkinter as tk
import threading

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
    
    def start(self):
        with self.window_lock:
            self.window.mainloop()


if __name__ == "__main__":
    ui = UI.getInstance()
    ui.start()