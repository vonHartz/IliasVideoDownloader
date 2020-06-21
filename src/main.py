# Copyright 2020, Jan Ole von Hartz <hartzj@cs.uni-freiburg.de>.


import logging

from src.core.browser_handler import browser_handler
from src.core.database_handler import database_handler
from src.gui.gui_handler import gui_handler

logger_name = 'ilias_dl_runner'
log_file_name = 'ilias_dl.log'


class runner:
    def __init__(self, logger=None):
        self.logger = logger
        self.database_handler = database_handler(self, logger=logger)
        self.browser_handler = browser_handler(self, logger=logger)
        self.browser_handler.create_driver()
        self.gui_handler = gui_handler(self, logger=logger)

    def run(self):
        self.gui_handler.run()

    def load_file(self, response):
        self.database_handler.load_file(response)

    def save_file(self):
        self.database_handler.save_file()

    def save_file_as(self, response):
        self.database_handler.save_file_as(response)

    def new_file(self):
        self.database_handler.new_file()

    def db_saving_target_exist(self):
        return self.database_handler.db_saving_target_exist()

    def get_username(self):
        return self.database_handler.get_username()

    def set_username(self, name):
        return self.database_handler.set_username(name)

    def login(self, *args):
        username, pw = self.gui_handler.read_login()
        self.database_handler.set_username(username)
        self.browser_handler.login(username, pw)

    def get_browser_handle(self):
        return self.browser_handler.get_browser_handle()

    def add_current_url(self):
        url = self.browser_handler.get_current_url()
        self.database_handler.add_url(url)
        self.gui_handler.refresh_urls()

    def revert_last_action(self):
        return self.runner.revert_last_action()

    def get_urls_from_db(self):
        return self.database_handler.get_urls()


def main():
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(log_file_name)
    fh.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)

    r = runner(logger=logger)
    r.run()


if __name__ == "__main__":
    main()
