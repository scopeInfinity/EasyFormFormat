from data import entity
from data.exporter import generic
from util import serialization

import logging
from typing import List
import os
import json


class Project(serialization.Serializable):
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

    def unmarshal(self, data):
        self.entities.clear()
        for d in data:
            # lookahead within d
            e = entity.Entity(self.unmarshal_get_value(d, "name", str))
            e.unmarshal(d)
            self.entities.append(e)

    def marshal(self):
        lst = []
        for e in self.entities:
            lst.append(e.marshal())
        return lst

    def save_project(self, fname: str) -> None:
        logging.info(f"saving project to {fname}")
        with open(fname, 'w', encoding='utf-8') as f:
            json.dump(self.marshal(), f, indent=4)

    def load_project(self, fname: str) -> None:
        logging.info(f"loading project from {fname}")
        with open(fname, 'r', encoding='utf-8') as f:
            self.unmarshal(json.load(f))

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
