from data import image
from data.exporter import pdf, jpeg


def export(img: image.Image, fname: str):
    fmt = img.get_export_format().get_format()
    if fmt == image.ImageFormat.PDF:
        return pdf.export(img, fname)

    if fmt == image.ImageFormat.JPEG:
        return jpeg.export(img, fname)

    raise ValueError(f"No exporter defined for {fmt}")
