import logging
from data import image
from data.exporter import generic


def export(img: image.Image, fname: str):
    fmt = img.get_export_format()
    res = fmt.get_resolution()
    new_img = img.get_scaled_image(res)

    def tmp_exporter(fname, quality):
        return new_img.save(fname, quality=quality)

    generic.get_image_quality(
        fname,
        fmt.get_quality_minsize_kb(),
        fmt.get_quality_maxsize_kb(),
        tmp_exporter,
        preserve_image=True,
    )
    logging.info(f"saved jpeg at {fname}")
