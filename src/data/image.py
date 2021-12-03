import logging
from PIL import Image as PILImage
from enum import Enum

from typing import Tuple

from util.serialization import Serializable


class ImageFormat(Enum):
    JPEG = 1
    PNG = 2
    PDF = 3


def get_extension(fmt: ImageFormat) -> str:
    return fmt.name.lower()


class ExportOption(Serializable):
    def __init__(self,
                 format: ImageFormat,
                 resolution: Tuple[int, int],
                 min_size: int,
                 max_size: int):
        self.format = format  # type: ImageFormat
        self.resolution = resolution  # type: Tuple[int, int]
        self.min_size = min_size  # type: int
        self.max_size = max_size  # type: int

    def unmarshal(self, data):
        self.format = ImageFormat[self.unmarshal_get_value(data, "fmt", str)]
        w = self.unmarshal_get_value(data, "res_w", int)
        h = self.unmarshal_get_value(data, "res_h", int)
        self.resolution = w, h
        self.min_size = self.unmarshal_get_value(data, "min_size", int)
        self.max_size = self.unmarshal_get_value(data, "max_size", int)

    def marshal(self):
        data = {}
        data["fmt"] = self.format.name
        data["res_w"] = self.resolution[0]
        data["res_h"] = self.resolution[1]
        data["min_size"] = self.min_size
        data["max_size"] = self.max_size
        return data

    def get_resolution(self) -> Tuple[int, int]:
        return self.resolution

    def set_resolution(self, resolution: Tuple[int, int]):
        if len(resolution) != 2:
            raise ValueError(f"invalid resolution: '{resolution}'")
        if not all(type(x) == int for x in resolution):
            raise ValueError(f"invalid resolution: '{resolution}'")
        if resolution[0] <= 0 or resolution[1] <= 0:
            raise ValueError(
                "invalid resolution: '{resolution}', negative width/height")
        self.resolution = resolution

    def set_filesize(self, min_size_kb: int, max_size_kb: int):
        self.min_size = min_size_kb
        self.max_size = max_size_kb

    def set_quality_str(self, min_size_kb: str, max_size_kb: str):
        '''
        Set export quality range by min_size_kb and max_size_kb.
        '''
        try:
            min_s = int(min_size_kb)
            max_s = int(max_size_kb)

            self.min_size = min_s
            self.max_size = max_s
        except ValueError as err:
            logging.error(
                f"invalid quality: '{min_size_kb}' to '{max_size_kb}' kb, err: {err}")

    def get_size_min_kb(self):
        return self.min_size

    def get_size_max_kb(self):
        return self.max_size

    def get_format(self) -> ImageFormat:
        return self.format

    def set_format(self, format: ImageFormat):
        self.format = format


DEFAULT_EXPORT_OPTION = ExportOption(ImageFormat.JPEG, (640, 480), 100, 400)


class Image:
    """
    Hold one image in any format.
    """

    def __init__(self, fname: str):
        self.__fname = None  # type: str
        self.__image = None  # type: PILImage.Image
        self.load_image(fname)

    def get_fname(self):
        return self.__fname

    def load_image(self, fname: str):
        logging.info(f"loading: {fname}")
        self.__fname = fname
        self.__image = PILImage.open(self.__fname)

    def get_image(self) -> PILImage.Image:
        return self.__image

    def get_original_size(self) -> Tuple[int, int]:
        return self.__image.size

    def get_scaled_image(self, sz) -> PILImage.Image:
        return self.get_image().resize(sz, PILImage.ANTIALIAS)
