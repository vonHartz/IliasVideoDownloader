# Copyright 2020, Jan Ole von Hartz <hartzj@cs.uni-freiburg.de>.


from cefpython3 import cefpython as cef

import os
import platform
import sys

from gi.repository import GObject, GdkPixbuf  # noqa


WINDOWS = (platform.system() == "Windows")
LINUX = (platform.system() == "Linux")
MAC = (platform.system() == "Darwin")

if LINUX:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk, GdkX11


# class main_window(Gtk.Window):
class main_window(Gtk.Application):

    def __init__(self, gui_handler, window_title="ILIAS Downloader"):
        self.gui_handler = gui_handler
        super().__init__(application_id='ilias_dl.gtk3')
        # Gtk.Window.__init__(self, title=window_title)
        self.browser = None
        self.window = None

    def run(self):
        GObject.threads_init()
        GObject.timeout_add(10, self.on_timer)
        self.connect("startup", self.on_startup)
        self.connect("activate", self.on_activate)
        self.connect("shutdown", self.on_shutdown)
        return super().run()

    def get_handle(self):
        if LINUX:
            return self.window.get_property("window").get_xid()
        else:
            raise NotImplementedError


    def on_timer(self):
        cef.MessageLoopWork()
        return True

    def on_startup(self, *_):
        self.window = Gtk.ApplicationWindow.new(self)
        self.window.set_title("GTK 3 example (PyGObject)")
        self.window.set_default_size(1600, 400)
        self.window.connect("configure-event", self.on_configure)
        self.window.connect("size-allocate", self.on_size_allocate)
        self.window.connect("focus-in-event", self.on_focus_in)
        self.window.connect("delete-event", self.on_window_close)
        self.add_window(self.window)
        self.setup_icon()

    def on_activate(self, *_):
        self.window.realize()
        self.embed_browser()
        print("after embed")
        self.window.show_all()
        print("after showall")
        # Must set size of the window again after it was shown,
        # otherwise browser occupies only part of the window area.
        self.window.resize(*self.window.get_default_size())

    def embed_browser(self):
        window_info = cef.WindowInfo()
        handle_to_use = self.get_handle()
        display = Gdk.Display.get_default()
        window = GdkX11.X11Window.foreign_new_for_display(display,handle_to_use)
        self.gtk_window = gtk_window = Gtk.Window()
        def callback(gtk_window,window):
          print("inside callback")
          gtk_window.set_window(window)
          gtk_window.set_visual( gtk_window.get_screen().lookup_visual(0x21))
        gtk_window.connect("realize",callback,window)
        gtk_window.set_has_window(True)
        gtk_window.show()

        sw = Gtk.ScrolledWindow()
        sw.show()
        gtk_window.add(sw)
        sw.set_visual( sw.get_screen().lookup_visual(0x21))
        self.sw = sw

        self.browser = cef.CreateBrowserSync(window_info,
                                             url="https://www.google.com/")

        window_info = cef.WindowInfo()
        window_info.SetAsChild(sw.get_window().get_xid(),
                               [0, 0, 1600, 400])

    def on_configure(self, *_):
        if self.browser:
            self.browser.NotifyMoveOrResizeStarted()
        return False

    def on_size_allocate(self, _, data):
        if self.browser:
            if WINDOWS:
                WindowUtils.OnSize(self.win32_handle, 0, 0, 0)
            elif LINUX:
                (x, y) = (0, 0)
                (width, height) = self.window.get_size()
                self.browser.SetBounds(x, y, width, height)
                self.sw.get_window().move_resize(x, y, width, height)
            self.browser.NotifyMoveOrResizeStarted()

    def on_focus_in(self, *_):
        if self.browser:
            self.browser.SetFocus(True)
            return True
        return False

    def on_window_close(self, *_):
        if self.browser:
            self.browser.CloseBrowser(True)
            self.clear_browser_references()

    def clear_browser_references(self):
        # Clear browser references that you keep anywhere in your
        # code. All references must be cleared for CEF to shutdown cleanly.
        self.browser = None

    def on_shutdown(self, *_):
        cef.Shutdown()

    def setup_icon(self):
        icon = os.path.join(os.path.dirname(__file__), "resources", "gtk.png")
        if not os.path.exists(icon):
            return
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(icon)
        transparent = pixbuf.add_alpha(True, 0xff, 0xff, 0xff)
        Gtk.Window.set_default_icon_list([transparent])

        # self.set_border_width(3)
        #
        # self.grid = Gtk.Grid()
        # self.add(self.grid)
        #
        # self.menubar = self.create_menubar()
        # self.loginbar = self.create_loginbar(self.gui_handler.get_username())
        # self.toolbar = self.create_toolbar()
        # self.browser_window = self.create_browser_window()
        #
        # self.grid.attach(self.menubar, 1, 1, 50, 1)
        # self.grid.attach(self.loginbar, 1, 2, 50, 1)
        # self.grid.attach(self.toolbar, 1, 3, 50, 1)
        # self.grid.attach(self.browser_window, 1, 4, 50, 1)

    def create_loginbar(self, username):
        login_label = Gtk.Label('Login:')
        self.user_entry = Gtk.Entry()
        self.user_entry.set_text(username or 'username')
        self.pw_entry = Gtk.Entry()
        self.pw_entry.set_visibility(False)
        self.pw_entry.connect('activate', self.gui_handler.login)
        login_button = Gtk.Button('Login')
        login_button.connect('clicked', self.gui_handler.login)

        loginbar = Gtk.HBox(False, 2)
        for item in [login_label, self.user_entry, self.pw_entry,
                     login_button]:
            loginbar.pack_start(item, True, True, 10)

        return loginbar

    def create_menubar(self):
        load_item = Gtk.MenuItem.new_with_label('Load')
        load_item.connect('activate', self.gui_handler.load_file)

        save_item = Gtk.MenuItem.new_with_label('Save')
        save_item.connect('activate', self.gui_handler.save_file)

        save_as_item = Gtk.MenuItem.new_with_label('Save as ...')
        save_as_item.connect('activate', self.gui_handler.save_file_as)

        new_item = Gtk.MenuItem.new_with_label('New')
        new_item.connect('activate', self.gui_handler.new_file)

        file_menu = Gtk.Menu.new()
        for item in [load_item, save_item, save_as_item, new_item]:
            file_menu.append(item)

        file_item = Gtk.MenuItem.new_with_label('File')
        file_item.set_submenu(file_menu)

        # the menubar itself
        menubar = Gtk.MenuBar.new()
        menubar.append(file_item)

        return menubar

    def create_toolbar(self):
        toolbar = Gtk.Toolbar.new()

        add_url_item = Gtk.ToolButton.new(None, 'Add current URL')
        # new_meal_item.connect('clicked', self.gui_handler.run_meal_creator)
        toolbar.insert(add_url_item, -1)

        bar_item = Gtk.ToolButton.new_from_stock(Gtk.STOCK_OK)
        bar_item.connect('clicked', self.on_menu)
        toolbar.insert(bar_item, -1)

        return toolbar

    def create_browser_window(self):
        sw = Gtk.ScrolledWindow(None, None)
        sw.show()
        sw.set_visual(sw.get_screen().lookup_visual(0x21))

        return sw

        sys.excepthook = cef.ExceptHook  # To shutdown CEF processes on error
        cef.Initialize()
        window_info = cef.WindowInfo()
        self.get_window().get_xid()
        window_info = cef.WindowInfo()
        self.browser = cef.CreateBrowserSync(window_info,
                                             url="https://www.google.com/")

        return sw

    def on_menu(self, caller):
        print(caller)

    def get_active_date(self):
        return self.calendar.get_date()

    def update_day_view(self):
        date = self.get_active_date()
        self.day_view.populate(date)
        self.day_view.create_or_update_filter_and_view()
