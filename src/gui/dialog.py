import tkinter.filedialog
from tkinter import messagebox

import logging


def load_images():
    fnames = tkinter.filedialog.askopenfilenames(filetypes=[
        ('Images', '*.jpg *.jpeg *.png')
    ])
    return fnames if fnames else None


def load_project():
    fname = tkinter.filedialog.askopenfilename(filetypes=[
        ('EFF Project', '*.eff')
    ])
    return fname if fname else None


def save_project():
    fname = tkinter.filedialog.asksaveasfile(filetypes=[
        ('EFF Project', '*.eff')
    ])
    return fname.name if fname else None


def export_directory():
    dname = tkinter.filedialog.askdirectory()
    return dname if dname else None


def popup(title, msg):
    messagebox.showinfo(title, msg)


def popup_error(title, msg):
    messagebox.showerror(title, msg)


def dec_useraction(f):
    def new_f(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            # invalid user input
            popup_error("Invalid Input", str(e))
    return new_f


def dec_ui_useraction(f):
    # dec_useraction + finally redraw
    def new_f(cls, *args, **kwargs):
        try:
            return f(cls, *args, **kwargs)
        except ValueError as e:
            # invalid user input
            popup_error("Invalid Input", str(e))
        except Exception as e:
            logging.error("Internal error: %s", e)
            popup_error("Internal Error", str(e))
        finally:
            cls.redraw()
    return new_f

# TODO: merge with dec_ui_useraction


def dec_ui_useraction_noredraw(f):
    # dec_useraction + finally redraw
    def new_f(cls, *args, **kwargs):
        try:
            return f(cls, *args, **kwargs)
        except ValueError as e:
            # invalid user input
            popup_error("Invalid Input", str(e))
        except Exception as e:
            logging.error("Internal error: %s", e)
            popup_error("Internal Error", str(e))
    return new_f
