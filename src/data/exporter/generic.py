import os
import logging
from typing import Optional

from data import image
from data.exporter import pdf, simple_image_fmt


class ExportException(Exception):
    pass


class ExportFileAlreadyExistsException(Exception):
    pass


def get_image_quality(fname: str,
                      min_kb: int,
                      max_kb: int,
                      export_method,
                      min_quality: int = 1,
                      max_quality: int = 100,
                      preserve_image: Optional[bool] = False):
    """
    Returns quality parameter to be used by Pillow to export
    image of size between min_kb and max_kb.

    export_method(fname, quality) exports image based on argument
    this method is used to calculate the desired quality.

    The exported image file will persist under as fname.

    In case no quality exists to reach desired size, it will try
    closest match.

    If preserve_image is set, then temporarily exported images won't get
    deleted.
    """
    try:
        # min_quality defined in args
        # max_quality defined in args
        while min_quality <= max_quality:
            mid_quality = (min_quality + max_quality) // 2
            export_method(fname, mid_quality)
            sz = os.path.getsize(fname)
            if sz < min_kb * 1024:
                min_quality = mid_quality + 1
            elif sz > max_kb * 1024:
                max_quality = mid_quality - 1
            else:
                assert os.path.exists(fname)
                logging.info(
                    f"found quality for {fname} size: {min_kb} to {max_kb},"
                    f" quality: {mid_quality}")
                return mid_quality

        # atleast once exported file must have got created
        assert os.path.exists(fname)
        logging.warning(
            f"no found quality for {fname} size: {min_kb} to {max_kb},"
            f" using quality: {mid_quality}")
        return mid_quality
    finally:
        if (not preserve_image) and os.path.exists(fname):
            os.remove(fname)
