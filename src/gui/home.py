from os import stat
from pickle import load
from gui import ui
from gui import window
from gui import fillform
from gui import dialog
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
        tk.Label(
            root,
            text="Easy Form Format",
            pady=ui.FRAME_BORDER*32,
            font=("Courier", 64),
        ).pack(side=tk.TOP)

        tk.Button(
            root,
            text="New Project",
            command=new_project,
            pady=ui.FRAME_BORDER*8,
        ).pack(side=tk.TOP)

        tk.Button(
            root,
            text="Load Project",
            command=load_project,
            pady=ui.FRAME_BORDER*8,
        ).pack(side=tk.TOP)
