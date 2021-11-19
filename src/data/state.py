from data import project

from typing import Optional
import logging


class State:
    def __init__(self):
        logging.info("state created")
        self.project = None  # type: Optional[project.Project]

    def create_new_project(self):
        assert self.project is None, "one project is already open"
        logging.info("")
        self.project = project.Project()

    def reset_project(self):
        logging.info("")
        self.project = project.Project()

    def get_project(self) -> project.Project:
        assert self.project is not None, "no project are open"
        logging.info("")
        return self.project

    def load_project(self, fname: str):
        '''Expect no project to be loaded at calling time.'''
        assert self.project is None, "one project is already open"
        logging.info("")
        self.create_new_project()
        self.load_new_project(fname)

    def load_new_project(self, fname: str):
        '''Expect the current project to be already open.'''
        logging.info("")
        self.get_project().load(fname)


instance = State()


def get_state():
    return instance
