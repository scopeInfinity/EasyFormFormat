from gui import ui, home
import EasyFormFormat

from typing import Type
import tkinter as tk
import threading
import signal
import logging

SCREEN_SIZE = (640, 480)


def register_signal_handlers(sigint_handler):
    def handler(*args):
        sigint_handler()
    signal.signal(signal.SIGINT, handler)


class Window:
    """
    Window Interface to interact with humans.
    """

    is_running = threading.Lock()
    current_ui = None  # type: Type[ui.UI]

    @classmethod
    def start(cls):
        logging.debug("")
        logging.info("waiting for is_running lock")
        with cls.is_running:
            # Only one instance of cls.window should be running at a time.
            logging.info("granted")
            cls.window = tk.Tk()
            cls.window.geometry('{}x{}'.format(SCREEN_SIZE[0], SCREEN_SIZE[1]))
            cls.window.title(EasyFormFormat.TITLE)
            register_signal_handlers(Window.kill)
            cls.update_window(home.Home)
            logging.info("executing mainloop")
            cls.window.mainloop()

    @classmethod
    def kill(cls):
        logging.debug("")
        cls.window.destroy()
        cls.window.quit()

    @classmethod
    def update_window(cls, ui: Type[ui.UI]):
        logging.debug("")
        cls.current_ui = ui
        cls.redraw()

    @classmethod
    def get_tk(cls) -> tk.Tk:
        return cls.window

    @classmethod
    def clear(cls):
        logging.debug("")
        for child in cls.window.winfo_children():
            child.destroy()

    @classmethod
    def redraw(cls):
        logging.debug("")
        cls.clear()
        cls.current_ui.draw()
