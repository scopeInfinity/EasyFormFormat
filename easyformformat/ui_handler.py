import tkinter.filedialog

class UIHandler:
    def open_file(self):
        fnames = tkinter.filedialog.askopenfilenames(filetypes=[
            ('JPG', '*.jpg'),
            ('JPEG', '*.jpeg'),
            ('PNG', '*.png')
            ])
        if not fnames:
            return
        print("Selected files: {}".format(fnames))

