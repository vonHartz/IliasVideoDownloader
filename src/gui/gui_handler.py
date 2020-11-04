# Copyright 2020, Jan Ole von Hartz <hartzj@cs.uni-freiburg.de>.


import logging

from src.gui.main_window import main_window
from src.gui.file_chooser import file_choooser_window

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk  # noqa


class gui_handler:
    def __init__(self, runner, logger=None):
        self.runner = runner
        self.logger = logging.getLogger(logger.name + '.gui_handler')
        self.main_win = main_window(self)
        self.main_win.connect("destroy", Gtk.main_quit)
        self.refresh_urls()
        self.main_win.show_all()

    def run(self):
        Gtk.main()

    def load_file(self, *args):
        response = self.run_file_chooser()
        self.runner.load_file(response)

    def save_file(self, *args):
        if not self.runner.db_saving_target_exist():
            target = self.run_file_chooser("save")
            self.runner.save_file_as(target)
        else:
            self.runner.save_file()

    def save_file_as(self, *args):
        response = self.run_file_chooser("save")
        self.runner.save_file_as(response)

    def new_file(self, *args):
        self.runner.new_file()

    def run_file_chooser(self, action="open"):
        dialog = file_choooser_window(action)
        response = dialog.run()
        dialog.destroy()
        return response

    def read_login(self, *args):
        user = self.main_win.user_entry.get_text()
        pw = self.main_win.pw_entry.get_text()
        return user, pw

    def get_username(self):
        return self.runner.get_username()

    def set_username(self, name):
        return self.runner.set_username(name)

    def login(self, *args):
        self.set_status("logging in", 0.5)
        try:
            self.runner.login(*args)
            self.set_status("logged in", 1)
        except:
            raise

    def get_browser_handle(self, *args):
        return self.runner.get_browser_handle()

    def add_current_url(self, *args):
        self.runner.add_current_url()

    def revert_last_action(self, *args):
        return self.runner.revert_last_action()

    def get_urls(self):
        return self.runner.get_urls_from_db()

    def refresh_urls(self):
        urls = self.runner.get_urls_from_db()
        return self.main_win.set_urls(urls)

    def set_status(self, status_string, fractal):
        return self.main_win.set_status(status_string, fractal)
