from gui import window

import abc
import tkinter as tk

class UI(abc.ABC):
    """
    Base class screen populated over Window.
    """

    @classmethod
    @abc.abstractmethod
    def draw(cls):
        pass

    @classmethod
    def redraw(cls):
        window.Window.redraw()

