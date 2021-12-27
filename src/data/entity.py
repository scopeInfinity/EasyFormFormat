from data import image
from data.exporter import pdf, jpeg, png
from util.serialization import Serializable

from PIL import Image as PILImage
from typing import List, Optional, Tuple
import os
import copy


class Entity(Serializable):
    def __init__(self, name: str, fnames: Optional[List[str]] = None) -> None:
        self.name = name
        self.images = []  # type: List[image.Image]
        self.opts = copy.deepcopy(image.DEFAULT_EXPORT_OPTION)
        if fnames:
            self.add_images(fnames, update_resolution=True)

    def unmarshal(self, data):
        # data["name"] is also unsed in project.py as lookahead.
        self.set_name(self.unmarshal_get_value(data, "name", str))
        self.images.clear()
        files = []
        for f in self.unmarshal_get_value(data, "images"):
            files.append(self.unmarshal_value(f, str))
        self.add_images(files)
        self.opts.unmarshal(self.unmarshal_get_value(data, "opts"))

    def marshal(self):
        d = {}
        d["name"] = self.get_name()
        d["images"] = [d.get_fname() for d in self.images]
        d["opts"] = self.opts.marshal()
        return d

    def set_name(self, name: str) -> None:
        self.name = name
        # TODO: ensure name uniqueness

    def get_name(self, max_length: Optional[str] = None) -> str:
        if max_length is None:
            return self.name
        return self.name[:max_length]

    def get_raw_images(self) -> List[PILImage.Image]:
        return self.images

    def get_thumbnail(self, sz: Tuple[int, int]) -> PILImage.Image:
        assert len(self.images) > 0, "atleast one image is expected for thumbnail"
        return self.images[0].get_scaled_image(sz)

    def get_all_images_thumbnail(self, sz: Tuple[int, int]) -> List[PILImage.Image]:
        lst = []  # type: List[PILImage.Image]
        for img in self.images:
            lst.append(img.get_scaled_image(sz))
        return lst

    def add_images(self, fnames: List[str], update_resolution: Optional[bool] = False) -> None:
        for fname in fnames:
            self.images.append(image.Image(fname))

        if self.images and update_resolution:
            self.opts.set_resolution(self.images[0].get_original_size())

        # Auto convert image format to PDF if there are more than one image.
        if len(self.images) > 1:
            self.update_export_options(fmt=image.ImageFormat.PDF)

    def remove_image(self, index: int) -> None:
        assert len(
            self.images) > 1, ("can't remove last image from the entity, "
                               "entity itself should be deleted")
        self.images.pop(index)

    def swap_images(self, index_a: int, index_b: int) -> None:
        if index_a == index_b:
            return
        self.images[index_a], self.images[index_b] = self.images[index_b], self.images[index_a]

    def get_images_count(self) -> int:
        return len(self.images)

    def get_allowed_fmts(self) -> List[image.ImageFormat]:
        opts = [image.ImageFormat.PDF]
        if len(self.images) == 1:
            opts.extend([
                image.ImageFormat.JPEG,
                image.ImageFormat.PNG,
            ])
        return opts

    def get_export_options(self) -> image.ExportOption:
        return self.opts

    def update_export_options(self, fmt: Optional[image.ImageFormat] = None) -> None:
        if fmt is not None:
            if fmt not in self.get_allowed_fmts():
                raise ValueError("Unsupported format option provided")
            self.opts.format = fmt

    def get_export_filename(self, dir: str) -> str:
        opts = self.get_export_options()
        fmt = opts.format
        extension = image.get_extension(fmt)
        ofname = os.path.join(dir, "{}.{}".format(
            self.name, extension))
        return ofname

    def export(self, dir: str) -> None:
        ofname = self.get_export_filename(dir)
        opts = self.get_export_options()
        fmt = opts.format

        if fmt not in self.get_allowed_fmts():
            raise ValueError("Invalid export type provided, please reselect.")

        if fmt in [image.ImageFormat.JPEG]:
            return jpeg.export(self, ofname)

        if fmt in [image.ImageFormat.PNG]:
            return png.export(self, ofname)

        if fmt in [image.ImageFormat.PDF]:
            return pdf.export(self, ofname)

        assert False, f"no export redirector for {fmt}"

    def __str__(self) -> str:
        return "[entity/%s]" % self.get_name()
