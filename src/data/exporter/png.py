from data import entity
from data.exporter import generic

import math
import logging


def export(e: 'entity.Entity', fname: str):
    opts = e.get_export_options()
    res = opts.get_resolution()

    images = e.get_all_images_thumbnail(res)
    assert len(images) == 1

    image = images[0]

    def exporter(fname, quality):
        print(type(image))
        print(image)
        sz = image.size
        print(sz)
        print([int(math.ceil(d*quality)) for d in sz])
        new_size = tuple([int(math.ceil(d*quality/100)) for d in sz])
        print(new_size)
        new_image = image.resize(new_size)
        new_image.save(fname)

    generic.get_image_quality(
        fname,
        opts.get_size_min_kb(),
        opts.get_size_max_kb(),
        exporter,
        preserve_image=True,
    )
    logging.info(f"saved jpeg at {fname}")
