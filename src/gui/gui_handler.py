# Copyright 2020, Jan Ole von Hartz <hartzj@cs.uni-freiburg.de>.


import logging

from cefpython3 import cefpython as cef # move!

from src.gui.main_window import main_window
from src.gui.file_chooser import file_choooser_window

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk  # noqa


class gui_handler:
    def __init__(self, runner, logger=None):
        cef.Initialize()
        self.runner = runner
        self.logger = logging.getLogger(logger.name + '.gui_handler')
        self.main_win = main_window(self)
        #self.main_win.connect("destroy", Gtk.main_quit)
        #self.main_win.show_all()

    def run(self):
        # Gtk.main()
        SystemExit(self.main_win.run())

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
        return self.runner.login(*args)

    # def run_meal_creator(self, *args):
    #     date = self.main_win.get_active_date()
    #     meal_editor(self, date)
    #
    # def update_day_view(self):
    #     self.main_win.update_day_view()
