
from gui import ui
from gui import window
from gui import fillform
from gui import dialog
from gui import color
from data import state

import tkinter as tk


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
            bg=color.BG_PRIMARY,
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
            bg=color.BG_PRIMARY,
            fg=color.FG_PRIMARY,
        ).place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        lower_frame = tk.Frame(
            root,
            bg=color.BG_SECONDARY,
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
            bg=color.BG_PRIMARY,
            fg=color.FG_SECONDARY,
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
            bg=color.BG_PRIMARY,
            fg=color.FG_SECONDARY,
        ).place(
            relx=0.5,
            rely=0.6,
            relwidth=0.5,
            relheight=0.1,
            anchor="center",
        )
