import tkinter.filedialog
from tkinter import messagebox


def load_images():
    fnames = tkinter.filedialog.askopenfilenames(filetypes=[
        ('Images', '*.jpg *.jpeg *.png')
    ])
    return fnames


def export_directory():
    dname = tkinter.filedialog.askdirectory()
    return dname


def popup(title, msg):
    messagebox.showerror(title, msg)
