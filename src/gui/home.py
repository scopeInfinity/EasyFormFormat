from gui import ui
from gui import window
from gui import fillform

import tkinter as tk

from typing import Type


class Home(ui.UI):
    """
    Home GUI page
    """

    @classmethod
    def draw(cls):
        root = window.Window.get_tk()
        tk.Button(
            root,
            text="Fill form",
            command=lambda: window.Window.update_window(fillform.FillForm)
        ).pack(side = tk.TOP)

