from data import entity
from data.exporter import generic

import logging
from typing import Optional, List
import pickle
import os


class Project:
    def __init__(self) -> None:
        logging.info("project created")
        self.entities = []  # type: List[entity.Entity]

    def add_entity(self, fnames: List[str]):
        for fname in fnames:
            # TODO: ensure entity name is unique
            # create entity with one image each by default
            self.entities.append(entity.Entity(
                os.path.basename(fname), [fname]))

    def get_entities(self) -> List[entity.Entity]:
        return self.entities

    def save(self, fname: str) -> None:
        logging.info(f"saving project to {fname}")
        with open(fname, 'wb') as f:
            pickle.dump(self.__dict__, f)

    def load(self, fname: str) -> None:
        logging.info(f"loading project from {fname}")

        with open(fname, 'rb') as f:
            # unsafe operation
            self.__dict__ = pickle.load(f)

    def export_prep(self, dname: str) -> None:
        for e in self.entities:
            ofname = e.get_export_filename(dname)
            if os.path.exists(ofname):
                raise generic.ExportFileAlreadyExistsException(
                    f"{ofname} already exists.")
        return True

    def export(self, dname: str) -> None:
        # export with overwrite_file=true.
        for e in self.entities:
            e.export(dname)
