from gui import window

import abc


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
