import tkinter.filedialog

import ui

class UIHandler:
    def open_file(self):
        fnames = tkinter.filedialog.askopenfilenames(filetypes=[
            ('JPG', '*.jpg'),
            ('JPEG', '*.jpeg'),
            ('PNG', '*.png')
            ])
        if not fnames:
            return
        ui_obj = ui.getInstance()
        print("Selected files: {}".format(fnames))
        ui_obj.update(fnames)

