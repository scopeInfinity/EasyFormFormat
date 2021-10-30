import logging
from data import image
from data.exporter import generic

from typing import List
import os

def get_entity_basename(entity: image.Image, dir: str):
    return os.path.join(
        dir,
        entity.get_name() + "_" + str(id(entity)) + "." + entity.get_export_format().get_format().name.lower()
    )

def export_all(entries: List[image.Image], dir: str):
    logging.info(f"exporting {entries} to {dir}")
    os.makedirs(dir, exist_ok=True)
    for entry in entries:
        generic.export(entry, get_entity_basename(entry, dir))
