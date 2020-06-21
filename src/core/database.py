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

    def get_username(self):
        return self.username

    def set_username(self, name):
        self.username = name
