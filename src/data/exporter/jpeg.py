import logging
from data import image


def export(img: image.Image, fname: str):
    res = img.get_export_format().get_resolution()
    new_img = img.get_scaled_image(res)
    new_img.save(fname)
    # TODO: respect image quality
    logging.info(f"saved jpeg at {fname}")
