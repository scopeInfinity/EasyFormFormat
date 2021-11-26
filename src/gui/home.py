from os import stat
from pickle import load
from gui import ui
from gui import window
from gui import fillform
from gui import dialog
from data import state

import tkinter as tk

BG_COLOR_UPPER = "#40B5BC"
FG_COLOR_UPPER = "WHITE"
BG_COLOR_LOWER = "#D3DACE"
BG_COLOR_BUTTON = BG_COLOR_UPPER
FG_COLOR_TEXT = "WHITE"


@dialog.dec_useraction
def new_project():
    state.get_state().create_new_project()
    window.Window.update_window(fillform.FillForm)


@dialog.dec_useraction
def load_project():
    fname = dialog.load_project()
    if not fname:
        return
    state.get_state().load_project(fname)
    window.Window.update_window(fillform.FillForm)


class Home(ui.UI):
    """
    Home GUI page
    """

    @classmethod
    def draw(cls):
        root = window.Window.get_tk()

        upper_frame = tk.Frame(
            root,
            bg=BG_COLOR_UPPER,
        )
        upper_frame.pack(
            side=tk.LEFT,
            fill='both',
            expand=True,
        )

        tk.Label(
            upper_frame,
            text="Easy\nForm\nFormat",
            font=("Roboto", 48, "bold"),
            bg=BG_COLOR_UPPER,
            fg=FG_COLOR_UPPER,
        ).place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        lower_frame = tk.Frame(
            root,
            bg=BG_COLOR_LOWER,
        )
        lower_frame.pack(
            side=tk.LEFT,
            fill='both',
            expand=True,
        )

        tk.Button(
            lower_frame,
            text="New Project",
            command=new_project,
            font=("Roboto", 16),
            bg=BG_COLOR_BUTTON,
            fg=FG_COLOR_TEXT,
        ).place(
            relx=0.5,
            rely=0.4,
            relwidth=0.5,
            relheight=0.1,
            anchor="center",
        )

        tk.Button(
            lower_frame,
            text="Load Project",
            command=load_project,
            font=("Roboto", 16),
            bg=BG_COLOR_BUTTON,
            fg=FG_COLOR_TEXT,
        ).place(
            relx=0.5,
            rely=0.6,
            relwidth=0.5,
            relheight=0.1,
            anchor="center",
        )
