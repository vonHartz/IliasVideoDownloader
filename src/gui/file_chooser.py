# taken from <https://python-gtk-3-tutorial.readthedocs.io/en/latest/dialogs.ht
# ml>

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk  # noqa


class file_choooser_window(Gtk.Window):

    def __init__(self, action="open"):
        Gtk.Window.__init__(self, title="Choose a file.")

        if action == "open":
            gtk_action = Gtk.FileChooserAction.OPEN
        elif action == "save":
            gtk_action = Gtk.FileChooserAction.SAVE
        else:
            raise ValueError("unkown action for custom file chooser")

        self.dialog = Gtk.FileChooserDialog(
            "Please choose a file", self, gtk_action,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        self.add_filters(self.dialog)

    def run(self):
        response = self.dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Open clicked")
            print("File selected: " + self.dialog.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        return response

    def destroy(self):
        self.dialog.destroy()

    def add_filters(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Pickle files")
        filter_text.add_pattern("*.pkl")
        dialog.add_filter(filter_text)

        filter_py = Gtk.FileFilter()
        filter_py.set_name("ilias-downloader files")
        filter_py.add_mime_type("*.idf")
        dialog.add_filter(filter_py)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("All files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)
