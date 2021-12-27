import logging
from data import entity
from data.exporter import generic


def export(e: 'entity.Entity', fname: str):
    opts = e.get_export_options()
    res = opts.get_resolution()

    images = e.get_all_images_thumbnail(res)
    assert len(images) > 0

    generic.get_image_quality(
        fname,
        opts.get_size_min_kb(),
        opts.get_size_max_kb(),
        lambda fname, quality: images[0].save(
            fname, save_all=True, append_images=images[1:], quality=quality),
        preserve_image=True,
    )
    logging.info(f"saved pdf at {fname}")
