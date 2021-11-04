import logging
from data import image, processor
from gui import ui, window, dialog
import tkinter as tk
from PIL import ImageTk

from typing import List
import os

ENTRY_IMAGE_SZ = (80, 80)


def get_resolution(width: str, height: str):
    try:
        w = int(width)
        h = int(height)
        if w <= 0 or h <= 0:
            raise ValueError("negative width/height provided")
        return (w, h)
    except ValueError as err:
        logging.error(
            f"called with width:'{width}', height:'{height}', err: {err}")
        return None


class FillForm(ui.UI):
    """
    Fill Form page
    """

    entries = []  # type: List[image.Image]
    radio_selection = tk.IntVar
    radion_selected_image = None  # type: image.Image

    @classmethod
    def add_entries(cls, fnames=None):
        if fnames is None:
            fnames = dialog.load_images()
        for fname in fnames:
            cls.entries.append(image.Image(fname))
        cls.redraw()

    @classmethod
    def export_all(cls):
        try:
            dname = dialog.export_directory()
            processor.export_all(cls.entries, os.path.join(dname, "eff"))
        except ValueError as e:
            dialog.popup("Export Failed", str(e))
            return
        dialog.popup("Export", "Success!")

    @classmethod
    def populate_entry(cls, pframe: tk.Tk, entry: image.Image):
        frame = tk.Frame(
            pframe,
            height='100',
        )

        radio = tk.Radiobutton(
            frame,
            variable=cls.radio_selection,
            value=id(entry),
            text=entry.get_name(max_length=40),
            command=lambda: cls.update_entry(entry),
        )
        radio.pack(side=tk.LEFT)

        img = ImageTk.PhotoImage(entry.get_scaled_image(ENTRY_IMAGE_SZ))
        image_holder = tk.Label(
            frame,
            image=img,
        )
        image_holder.img = img  # hold reference
        image_holder.pack(side=tk.RIGHT)

        frame.pack(side=tk.TOP, anchor='n', fill='x')

    @classmethod
    def update_entry(cls, entry: image.Image):
        cls.radion_selected_image = entry
        cls.redraw()

    @classmethod
    def populate_entry_details(cls, pframe: tk.Tk, entry: image.Image):
        if entry is None:
            tk.Label(
                pframe,
                text="Please select a option",
            ).pack(side=tk.TOP)
            return
        img_format = tk.StringVar()
        name_var = tk.StringVar()
        res_w_var = tk.StringVar()
        res_h_var = tk.StringVar()
        size_min_kb = tk.StringVar()
        size_max_kb = tk.StringVar()

        name_var.set(entry.get_name())
        fmt = entry.get_export_format()
        img_format.set(fmt.get_format().name)
        res_w_var.set(str(fmt.get_resolution()[0]))
        res_h_var.set(str(fmt.get_resolution()[1]))
        size_min_kb.set(str(fmt.get_quality_minsize_kb()))
        size_max_kb.set(str(fmt.get_quality_maxsize_kb()))

        def save_details():
            try:
                entry.set_name(name_var.get())
                fmt = entry.get_export_format()
                fmt.set_format(image.ImageFormat[img_format.get()])
                fmt.set_resolution_str(res_w_var.get(), res_h_var.get())
                fmt.set_quality_str(size_min_kb.get(), size_max_kb.get())
            except ValueError as e:
                dialog.popup("Invalid Input",
                             f"Failed to save all details: {e}")
            cls.redraw()

        tk.Button(
            pframe,
            text='Save',
            command=lambda: save_details(),
            borderwidth=ui.FRAME_BORDER,
        ).pack(side=tk.TOP)

        tk.Entry(
            pframe,
            textvariable=name_var,
            borderwidth=ui.FRAME_BORDER,
        ).pack(side=tk.TOP)

        img = ImageTk.PhotoImage(entry.get_scaled_image(ENTRY_IMAGE_SZ))
        image_holder = tk.Label(
            pframe,
            image=img,
            borderwidth=ui.FRAME_BORDER,
        )
        image_holder.img = img  # hold reference
        image_holder.pack(side=tk.TOP)

        tk.Label(
            pframe,
            text="resolution WxH",
            borderwidth=ui.FRAME_BORDER,
        ).pack(side=tk.TOP)
        tk.Entry(
            pframe,
            textvariable=res_w_var,
            borderwidth=ui.FRAME_BORDER,
        ).pack(side=tk.TOP)
        tk.Entry(
            pframe,
            textvariable=res_h_var,
            borderwidth=ui.FRAME_BORDER,
        ).pack(side=tk.TOP)

        tk.Label(
            pframe,
            text="quality min_size max_size in KB",
            borderwidth=ui.FRAME_BORDER,
        ).pack(side=tk.TOP)
        tk.Entry(
            pframe,
            textvariable=size_min_kb,
            borderwidth=ui.FRAME_BORDER,
        ).pack(side=tk.TOP)
        tk.Entry(
            pframe,
            textvariable=size_max_kb,
            borderwidth=ui.FRAME_BORDER,
        ).pack(side=tk.TOP)

        options = [fmt.name for fmt in image.ImageFormat]
        drop = tk.OptionMenu(
            pframe,
            img_format,
            *options,
        )
        drop.pack(side=tk.TOP)

    @classmethod
    def draw(cls):
        root = window.Window.get_tk()

        # Note: human can press "export all" where there
        # are unsaved changes for current image
        tk.Button(
            root,
            text='Export All',
            command=lambda: cls.export_all(),
            borderwidth=ui.FRAME_BORDER,
            pady=ui.FRAME_BORDER,
        ).pack(side=tk.BOTTOM)

        # Left Side
        frame_entry = tk.Frame(
            root,
            borderwidth=ui.FRAME_BORDER,
        )

        tk.Button(
            frame_entry,
            text="Add entries",
            command=lambda: cls.add_entries(),
            pady=ui.FRAME_BORDER,
            borderwidth=ui.FRAME_BORDER,
        ).pack(side=tk.TOP)
        for entry in cls.entries:
            cls.populate_entry(frame_entry, entry)
        frame_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Right Side
        frame_details = tk.Frame(
            root,
            borderwidth=ui.FRAME_BORDER,
        )
        cls.populate_entry_details(frame_details, cls.radion_selected_image)
        frame_details.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
