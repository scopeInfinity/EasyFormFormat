from data.exporter import generic
from data import image, entity
from data import state
from gui import ui, window, dialog, color

from functools import partial
from PIL import ImageTk
from typing import Optional
import logging
import tkinter as tk
from tkinter import ttk

ENTRY_IMAGE_SZ = (60, 60)
THUMBNAIL_IMAGE_SZ = (320, 320)

COLOR_TITLE_BG = color.BG_SECONDARY
COLOR_TITLE_FG = color.FG_SECONDARY

COLOR_LEFT_BG = color.BG_PRIMARY
COLOR_LEFT_TEXT = 'BLACK'

COLOR_RIGHT_BG = color.BG_SECONDARY
COLOR_RIGHT_TEXT = color.FG_SECONDARY


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

    radio_selected_index = 0  # type: int

    @classmethod
    @dialog.dec_ui_useraction
    def save_project(cls):
        fname = dialog.save_project()
        if not fname:
            return
        state.get_state().get_project().save(fname)

    @classmethod
    @dialog.dec_ui_useraction
    def load_project(cls):
        fname = dialog.load_project()
        if not fname:
            return
        # TODO: ask user if they want to continue during pending changes
        state.get_state().load_new_project(fname)

    @classmethod
    @dialog.dec_ui_useraction
    def new_project(cls):
        # TODO: ask user if they want to continue during pending changes
        state.get_state().reset_project()

    @classmethod
    @dialog.dec_ui_useraction_noredraw
    def _exit(cls):
        # TODO: ask user if they want to continue during pending changes
        exit(0)

    @classmethod
    @dialog.dec_ui_useraction_noredraw
    def show_about(cls):
        # TODO: Add more details
        dialog.popup("About", "EasyFormFormat v1.0")

    @classmethod
    @dialog.dec_ui_useraction
    def add_entries(cls):
        fnames = dialog.load_images()
        if not fnames:
            return
        state.get_state().get_project().add_entity(fnames)

    @classmethod
    @dialog.dec_ui_useraction_noredraw
    def update_entity(cls,
                      e: entity.Entity,
                      name: Optional[str] = None,
                      fmt: Optional[str] = None,
                      w_str: Optional[str] = None,
                      h_str: Optional[str] = None,
                      sz_min_str: Optional[str] = None,
                      sz_max_str: Optional[str] = None,
                      ):
        if (w_str is None) ^ (h_str is None):
            raise Exception(
                "Only one among w_str or h_str provided in update_entity")
        if (sz_min_str is None) ^ (sz_max_str is None):
            raise Exception(
                "Only one among sz_min_str or sz_max_str provided in update_entity")

        try:
            w = int(w_str)
            h = int(h_str)
        except ValueError as err:
            logging.error(
                f"invalid resolution: '{w_str}'x'{h_str}', err: {err}")
            raise ValueError(f"Invalid resolution provided '{w_str}x{h_str}'")

        try:
            sz_min = int(sz_min_str)
            sz_max = int(sz_max_str)
        except ValueError as err:
            logging.error(
                f"invalid filesize: '{sz_min_str}...{sz_max_str}', err: {err}")
            raise ValueError(
                f"Invalid resolution provided '{sz_min_str}...{sz_max_str}'")

        e.set_name(name)
        opts = e.get_export_options()
        opts.set_resolution((w, h))
        opts.set_format(image.ImageFormat[fmt])
        opts.set_filesize(sz_min, sz_max)

    @classmethod
    @dialog.dec_ui_useraction
    def add_image_in_entity(cls, e: entity.Entity):
        fnames = dialog.load_images()
        e.add_images(fnames)

    @classmethod
    @dialog.dec_ui_useraction
    def entity_image_del(cls, e: entity.Entity, index: int):
        e.remove_image(index)

    @classmethod
    @dialog.dec_ui_useraction
    def entity_image_move_up(cls, e: entity.Entity, index: int):
        if index > 0:
            e.swap_images(index, index-1)

    @classmethod
    @dialog.dec_ui_useraction
    def entity_image_move_down(cls, e: entity.Entity, index: int):
        if index < e.get_images_count() - 1:
            e.swap_images(index, index+1)

    @classmethod
    @dialog.dec_ui_useraction
    def select_entity(cls, index: int):
        cls.radio_selected_index = index

    @classmethod
    @dialog.dec_ui_useraction
    def export_all(cls):
        try:
            dname = dialog.export_directory()
            p = state.get_state().get_project()
            try:
                p.export_prep(dname)
            except generic.ExportFileAlreadyExistsException:
                # TODO: ask user if they are ok with overwrite.
                pass
            p.export(dname)
        except generic.ExportException as e:
            dialog.popup_error("Export Failed", str(e))
            return
        dialog.popup("Export", "Successful")

    @classmethod
    def populate_entity(cls, index: int, pframe: tk.Tk, e: entity.Entity):
        frame = tk.Frame(
            pframe,
            bg=COLOR_LEFT_BG,
        )

        radio = tk.Radiobutton(
            frame,
            value=index,
            text=e.get_name(max_length=40),
            command=partial(cls.select_entity, index),
            bg=COLOR_LEFT_BG,
            fg=COLOR_LEFT_TEXT,
            highlightthickness=0,
        )
        if cls.radio_selected_index == index:
            radio.select()
        else:
            radio.deselect()
        radio.pack(side=tk.LEFT)

        img = ImageTk.PhotoImage(e.get_thumbnail(ENTRY_IMAGE_SZ))
        image_holder = tk.Label(
            frame,
            image=img,
        )
        image_holder.img = img  # hold reference
        image_holder.pack(side=tk.RIGHT)

        frame.pack(side=tk.TOP, anchor='n', fill='x')

    @classmethod
    def populate_entity_details(cls, pframe: tk.Tk, e: entity.Entity):
        mframe = tk.Frame(
            pframe,
            bg=COLOR_RIGHT_BG,
        )
        mframe.pack(side=tk.LEFT, expand=True, fill='y')
        rframe = tk.Frame(
            pframe,
            bg=COLOR_RIGHT_BG,
        )
        rframe.pack(side=tk.RIGHT, expand=True, fill='both')

        if e is None:
            tk.Label(
                pframe,
                text="Please select a option",
                bg=COLOR_RIGHT_BG,
            ).pack(side=tk.TOP)
            return
        img_format = tk.StringVar()
        name_var = tk.StringVar()
        res_w_var = tk.StringVar()
        res_h_var = tk.StringVar()
        size_min_kb = tk.StringVar()
        size_max_kb = tk.StringVar()

        name_var.set(e.get_name())
        fmt = e.get_export_options()

        img_format.set(fmt.get_format().name)
        res_w_var.set(str(fmt.get_resolution()[0]))
        res_h_var.set(str(fmt.get_resolution()[1]))
        size_min_kb.set(str(fmt.get_size_min_kb()))
        size_max_kb.set(str(fmt.get_size_max_kb()))

        def save_details():
            cls.update_entity(
                e,
                name=name_var.get(),
                fmt=img_format.get(),
                w_str=res_w_var.get(),
                h_str=res_h_var.get(),
                sz_min_str=size_min_kb.get(),
                sz_max_str=size_max_kb.get(),
            )

        # TODO: We should have auto save for entities.
        tk.Button(
            mframe,
            text='Save',
            command=save_details,
            borderwidth=ui.FRAME_BORDER,
        ).pack(side=tk.TOP)

        tk.Button(
            mframe,
            text='Add Image',
            command=partial(cls.add_image_in_entity, e),
            borderwidth=ui.FRAME_BORDER,
        ).pack(side=tk.TOP)

        tk.Entry(
            mframe,
            textvariable=name_var,
            borderwidth=ui.FRAME_BORDER,
        ).pack(side=tk.TOP)

        tk.Label(
            mframe,
            text="resolution WxH",
            borderwidth=ui.FRAME_BORDER,
            bg=COLOR_RIGHT_BG,
        ).pack(side=tk.TOP)
        tk.Entry(
            mframe,
            textvariable=res_w_var,
            borderwidth=ui.FRAME_BORDER,
        ).pack(side=tk.TOP)
        tk.Entry(
            mframe,
            textvariable=res_h_var,
            borderwidth=ui.FRAME_BORDER,
        ).pack(side=tk.TOP)

        tk.Label(
            mframe,
            text="quality min_size max_size in KB",
            borderwidth=ui.FRAME_BORDER,
            bg=COLOR_RIGHT_BG,
        ).pack(side=tk.TOP)
        tk.Entry(
            mframe,
            textvariable=size_min_kb,
            borderwidth=ui.FRAME_BORDER,
        ).pack(side=tk.TOP)
        tk.Entry(
            mframe,
            textvariable=size_max_kb,
            borderwidth=ui.FRAME_BORDER,
        ).pack(side=tk.TOP)

        drop = tk.OptionMenu(
            mframe,
            img_format,
            *[fmt.name for fmt in e.get_allowed_fmts()],
        )
        drop.pack(side=tk.TOP)

        scrollview_bar = tk.Scrollbar(rframe, orient='vertical')
        scrollview_bar.pack(
            side=tk.RIGHT,
            fill='y',
        )
        scrollview_canvas = tk.Canvas(
            rframe,
            yscrollcommand=scrollview_bar.set,
            bg=COLOR_RIGHT_BG,
        )
        scrollview_canvas.pack(
            side=tk.RIGHT,
            fill='y')

        scrollview_frame = ttk.Frame(
            scrollview_canvas,
        )

        scrollview_bar.config(command=scrollview_canvas.yview)
        scrollview_frame.bind(
            "<Configure>",
            lambda e: scrollview_canvas.configure(
                scrollregion=scrollview_canvas.bbox("all")
            )
        )
        scrollview_canvas.create_window(
            0, 0, anchor="nw", window=scrollview_frame)
        scrollview_canvas.configure(yscrollcommand=scrollview_bar.set)

        thumbnails_count = e.get_images_count()
        thumbnails = e.get_all_images_thumbnail(THUMBNAIL_IMAGE_SZ)
        for it, t in enumerate(thumbnails):
            fr = tk.Frame(
                scrollview_frame,
                bg=COLOR_RIGHT_BG,
            )
            img = ImageTk.PhotoImage(t)
            image_holder = tk.Label(
                fr,
                image=img,
                borderwidth=ui.FRAME_BORDER,
            )
            image_holder.img = img  # hold reference
            image_holder.pack(side=tk.LEFT)

            fr_subbuttons = tk.Frame(fr)
            tk.Button(fr_subbuttons,
                      text="x",
                      state=tk.DISABLED if thumbnails_count == 1 else None,
                      command=partial(cls.entity_image_del, e, it),
                      ).pack(
                          side=tk.TOP,
            )
            tk.Button(fr_subbuttons,
                      text="^",
                      state=tk.DISABLED if it == 0 else None,
                      command=partial(cls.entity_image_move_up, e, it),
                      ).pack(side=tk.TOP)
            tk.Button(fr_subbuttons,
                      text="v",
                      state=tk.DISABLED if it == thumbnails_count-1 else None,
                      command=partial(cls.entity_image_move_down, e, it),
                      ).pack(side=tk.TOP)
            fr_subbuttons.pack(side=tk.RIGHT)

            fr.pack(side=tk.TOP)

    @classmethod
    def draw(cls):
        root = window.Window.get_tk()
        p = state.get_state().get_project()

        # Menu bar
        menubar = tk.Menu(
            root,
            bg=COLOR_TITLE_BG,
            fg=COLOR_TITLE_FG,
        )
        root.config(menu=menubar)
        m_file = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='File', menu=m_file)
        m_file.add_command(label='New Project', command=cls.new_project)
        # TODO: Currently we have "save as", we should also have simple save.
        m_file.add_command(label='Save Project', command=cls.save_project)
        m_file.add_command(label='Load Project', command=cls.load_project)
        m_file.add_separator()
        # TODO: human can export all where there
        # are unsaved changes for current image.
        m_file.add_command(label='Export All', command=cls.export_all)
        m_file.add_separator()
        m_file.add_command(label='Exit', command=cls._exit)

        m_help = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Help', menu=m_help)
        # TODO: implement help support
        m_help.add_command(label='Get Started')
        m_help.add_command(label='About', command=cls.show_about)

        # Frames
        lframe = tk.Frame(
            root,
            borderwidth=ui.FRAME_BORDER,
            bg=COLOR_LEFT_BG,
        )
        rframe = tk.Frame(
            root,
            borderwidth=ui.FRAME_BORDER,
            bg=COLOR_RIGHT_BG,
        )
        lframe.place(
            relheight=1,
            relwidth=0.3,
            relx=0,
            rely=0)
        rframe.place(
            relheight=1,
            relwidth=0.7,
            relx=0.3,
            rely=0)

        # Left side

        tk.Button(
            lframe,
            text="Add entries",
            command=cls.add_entries,
            pady=ui.FRAME_BORDER,
            borderwidth=ui.FRAME_BORDER,
        ).pack(side=tk.TOP)
        for it, e in enumerate(p.get_entities()):
            cls.populate_entity(it, lframe, e)

        # Right Side
        selected_entity = None
        if cls.radio_selected_index >= 0 and cls.radio_selected_index < len(p.get_entities()):
            selected_entity = p.get_entities()[cls.radio_selected_index]
        cls.populate_entity_details(rframe, selected_entity)
