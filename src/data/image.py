import logging
from PIL import Image as PILImage
from enum import Enum

from typing import Tuple
import os
import copy

class ImageFormat(Enum):
    JPEG = 1
    PNG = 2
    PDF = 3

class ExportFormat:
    def __init__(self,
        format: ImageFormat,
        resolution: Tuple[int, int],
        min_size: int,
        max_size: int):
        self.format = format  # type: ImageFormat
        self.resolution = resolution # type: Tuple[int, int]
        self.min_size = min_size  # type: int
        self.max_size = max_size  # type: int

    def get_resolution(self) -> Tuple[int, int]:
        return self.resolution

    def set_resolution(self, resolution: Tuple[int, int]):
        if len(resolution) != 2:
            raise ValueError(f"invalid resolution: '{resolution}'")
        if not all(type(x) == int for x in resolution):
            raise ValueError(f"invalid resolution: '{resolution}'")
        if resolution[0] <= 0 or resolution[1] <= 0:
            raise ValueError("invalid resolution: '{resolution}', negative width/height")
        self.resolution = resolution

    def set_resolution_str(self, width: str, height: str):
        try:
            w = int(width)
            h = int(height)
            self.set_resolution((w, h))
        except ValueError as err:
            logging.error(f"invalid resolution: '{width}'x'{height}', err: {err}")

    def set_quality_str(self, min_size: str, max_size: str):
        '''
        Set export quality range by min_size and max_size in kb.
        '''
        try:
            min_s = int(min_size)
            max_s = int(max_size)

            self.min_size = min_s
            self.max_size = max_s
        except ValueError as err:
            logging.error(f"invalid quality: '{min_size}' to '{max_size}' kb, err: {err}")

    def get_quality_minsize(self):
        return self.min_size

    def get_quality_maxsize(self):
        return self.max_size

    def get_format(self) -> ImageFormat:
        return self.format

    def set_format(self, format: ImageFormat):
        self.format = format


DEFAULT_EXPORT_FORMAT = ExportFormat(ImageFormat.JPEG, (640,480), 100, 400)

class Image:
    """
    Hold one image in any format.
    """

    def __init__(self, fname: str):
        self.__fname = None  # type: str
        self.__image = None  # type: PILImage.Image
        self.__name = os.path.basename(fname)
        self.export_format = copy.deepcopy(DEFAULT_EXPORT_FORMAT)
        self.load_image(fname)

    def get_fname(self):
        return self.__fname

    def get_name(self, max_length = None):
        if max_length is None:
            return self.__name
        return self.__name[:max_length]

    def set_name(self, name):
        self.__name = name

    def update_export_format(self, fmt: ExportFormat):
        self.export_format = fmt

    def get_export_format(self) -> ExportFormat:
        return self.export_format

    def load_image(self, fname: str):
        logging.info(f"loading: {fname}")
        self.__fname = fname
        self.__image = PILImage.open(self.__fname)
        self.get_export_format().set_resolution(self.__image.size)

    def get_image(self) -> PILImage.Image:
        return self.__image

    def get_scaled_image(self, sz) -> PILImage.Image:
        return self.get_image().resize(sz)

    def __str__(self) -> str:
        return "[%s]" % self.get_name()
