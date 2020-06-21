# Copyright 2020, Jan Ole von Hartz <hartzj@cs.uni-freiburg.de>.


class database:
    """Class managing all data.

    Parameters
    ----------
    title : str
        Name of the db.
    username : str
        ILIAS user name.

    Attributes
    ----------
    title
    username

    """

    def __init__(self, title='standard', username=None):
        self.title = title
        self.username = username
        self.urls = []

    def get_username(self):
        return self.username

    def set_username(self, name):
        self.username = name

    def add_url(self, url):
        self.urls.append(ilias_object(url))

    def get_urls(self):
        return [i.tree_repr() for i in self.urls]


class ilias_object:
    def __init__(self, url, up_to_date=None):
        self.url = url
        self.up_to_date = up_to_date

    def tree_repr(self):
        return (self.url, self.up_to_date)
