# Copyright 2020, Jan Ole von Hartz <hartzj@cs.uni-freiburg.de>.


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk  # noqa


outdated_str = "Out-dated"
uptodate_str = "Up-to-date"
column_list = ['URL', 'Up-to-Date']


class main_window(Gtk.Window):

    def __init__(self, gui_handler, window_title="ILIAS Downloader"):
        self.gui_handler = gui_handler
        Gtk.Window.__init__(self, title=window_title)
        self.set_default_size(1920, 1080)
        self.set_border_width(3)

        self.grid = Gtk.Grid()
        self.add(self.grid)

        self.menubar = self.create_menubar()
        self.loginbar = self.create_loginbar(self.gui_handler.get_username())
        self.toolbar = self.create_toolbar()
        self.browser_window = self.create_browser_window()
        self.url_view = url_view(self.gui_handler)

        self.grid.attach(self.menubar, 1, 1, 50, 1)
        self.grid.attach(self.loginbar, 1, 2, 50, 1)
        self.grid.attach(self.toolbar, 1, 3, 50, 1)
        self.url_view.attach_in_grid(self.grid, 1, 4, 2, 10)
        self.grid.attach(self.browser_window, 2, 4, 50, 1)

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
        add_url_item.connect('clicked', self.gui_handler.add_current_url)
        toolbar.insert(add_url_item, -1)

        bar_item = Gtk.ToolButton.new_from_stock(Gtk.STOCK_OK)
        bar_item.connect('clicked', self.gui_handler.revert_last_action)
        toolbar.insert(bar_item, -1)

        return toolbar

    def create_browser_window(self):
        sw = Gtk.ScrolledWindow(None, None)

        # browser_handle = self.gui_handler.get_browser_handle()
        # print(dir(browser_handle))
        # socket = Gtk.Socket()
        # socket.add_id(int(browser_handle))
        # sw.add_child(socket)
        # # browser_window = Gdk.window_foreign_new(browser_handle)
        # print(browser_handle)

        return sw

    def set_urls(self, urls):
        self.url_view.populate(urls)
        self.url_view.update_treeview()


class url_view(Gtk.Widget):

    def __init__(self, gui_handler):
        self.gui_handler = gui_handler
        super().__init__()
        self.populate([('bka', None), ('ba', True), ('ab', False)])
        self.create_filter_and_view()

        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.scrollable_treelist.set_hexpand(True)
        self.scrollable_treelist.add_with_viewport(self.treeview)

    def create_filter_and_view(self):
        self.filter_values = [outdated_str, uptodate_str]
        self.current_filter = None
        self.create_filter()
        self.create_treeview()
        self.create_buttons()

    def create_treeview(self):
        self.treeview = Gtk.TreeView.new_with_model(self.filter)

        for i, column_title in enumerate(column_list):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)

        # single click row
        self.selection = self.treeview.get_selection()
        self.selection.connect("changed", self.on_single_click)

        # double click row
        self.treeview.connect("row-activated", self.on_double_click)

    def create_buttons(self):
        self.buttons = list()
        for filter_value in self.filter_values:
            button = Gtk.Button(filter_value)
            self.buttons.append(button)
            button.connect("clicked", self.on_selection_button_clicked)

    def create_filter(self):
        self.filter = self.liststore.filter_new()
        self.filter.set_visible_func(self.filter_func)

    def attach_next_to_in_grid(self, grid, sibling, position, width, height):
        grid.attach_next_to(self.scrollable_treelist, sibling,
                            position, width, height)
        self.attach_buttons(grid)

    def attach_in_grid(self, grid, left, top, width, height):
        grid.attach(self.scrollable_treelist, left, top, width, height)
        self.attach_buttons(grid)

    def attach_buttons(self, grid):
        if len(self.buttons) > 0:
            grid.attach_next_to(self.buttons[0], self.scrollable_treelist,
                                Gtk.PositionType.BOTTOM, 1, 1)
            for i, button in enumerate(self.buttons[1:]):
                grid.attach_next_to(button, self.buttons[i],
                                    Gtk.PositionType.RIGHT, 1, 1)

    def populate(self, urls=None):
        self.liststore = Gtk.ListStore(str, bool)

        if urls is None:
            urls = self.gui_handler.get_urls()
        if not isinstance(urls, list):
            urls = [urls]
        for item in urls:
            self.liststore.append(list(item))

    def update_treeview(self):
        filtered_model = Gtk.TreeModelFilter()
        sorted_model = Gtk.TreeModelSort.sort_new_with_model(self.filter)

        filtered_model.set_visible_func(self.filter_func, self.liststore)

        self.treeview.set_model(sorted_model)

    def filter_func(self, model, iter, data):
        if ((self.current_filter is None) or (self.current_filter == "None")):
            return True
        else:
            return model[iter][1] == self.current_filter

    def on_selection_button_clicked(self, widget):
        label = widget.get_label()
        if label == outdated_str:
            self.current_filter = False
        elif label == uptodate_str:
            self.current_filter = True
        else:
            self.current_filter = None
        self.filter.refilter()
        self.update_treeview()

    def on_single_click(self, selection):
        (model, iter) = selection.get_selected()

        if iter is not None:
            print("\n %s" % (model[iter][0]))
        else:
            print("")
        return True

    def on_double_click(self, treeview, row_no, column):
        (model, iter) = self.selection.get_selected()

        print("\n %s" % (model[iter][0]))

        # TODO open edit window

        return True
