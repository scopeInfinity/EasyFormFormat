import logging
from data import entity
from data.exporter import generic


def export(e: entity.Entity, fname: str):
    opts = e.get_export_options()
    fmt = opts.get_format()
    res = opts.get_resolution()

    images = e.get_all_images_thumbnail(res)
    assert len(images) == 1

    image = images[0]

    generic.get_image_quality(
        fname,
        opts.get_size_min_kb(),
        opts.get_size_max_kb(),
        lambda fname, quality: image.save(fname, quality=quality),
        preserve_image=True,
    )
    logging.info(f"saved jpeg at {fname}")
