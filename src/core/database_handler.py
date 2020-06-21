# Copyright 2020, Jan Ole von Hartz <hartzj@cs.uni-freiburg.de>.


import logging
import pickle

from src.core.database import database


class database_handler:
    def __init__(self, runner, logger=None, default_db=None):
        self.runner = runner
        self.runner = runner
        self.logger = logging.getLogger(logger.name + '.database_handler')
        self.active_db_path = default_db
        if self.active_db_path is not None:
            self.load_file(self.active_db_path)
        else:
            self.active_database = database()

    def load_file(self, path, target=None):
        if target is None:
            target = self.active_database
        target = pickle.load(path)
        self.active_db_path = path

    def save_file(self, source=None):
        if source is None:
            source = self.active_database
        try:
            pickle.dump(source, self.active_db_path)
        except:
            raise

    def save_file_as(self, target, source=None):
        if source is None:
            source = self.active_database
        pickle.dump(source, target)
        self.active_db_path = target

    def new_file(self):
        self.active_database = database()
        self.active_db_path = None

    def db_saving_target_exist(self):
        return self.active_db_path is not None

    def get_username(self):
        return self.active_database.get_username()

    def set_username(self, name):
        return self.active_database.set_username(name)

    def add_url(self, url):
        return self.active_database.add_url(url)

    def get_urls(self):
        return self.active_database.get_urls()
