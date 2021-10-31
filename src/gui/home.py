from gui import ui
from gui import window
from gui import fillform

import tkinter as tk


class Home(ui.UI):
    """
    Home GUI page
    """

    @classmethod
    def draw(cls):
        root = window.Window.get_tk()
        tk.Label(
            root,
            text="Easy Form Format",
            pady=ui.FRAME_BORDER*32,
            font=("Courier", 64),
        ).pack(side=tk.TOP)

        tk.Button(
            root,
            text="New Project",
            command=lambda: window.Window.update_window(fillform.FillForm),
            pady=ui.FRAME_BORDER*8,
        ).pack(side=tk.TOP)

        tk.Button(
            root,
            text="Load Project (same as new)",
            command=lambda: window.Window.update_window(fillform.FillForm),
            pady=ui.FRAME_BORDER*8,
        ).pack(side=tk.TOP)
