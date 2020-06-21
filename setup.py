# Copyright 2018, Jan Ole von Hartz <hartzj@cs.uni-freiburg.de>.

import setuptools


setuptools.setup(
    name='ilias-downloader',
    url='https://github.com/vonHartz/IliasVideoDownloader',
    description="Simple PyGtk application to download material from ILIAS",
    classifiers=['Programming Language :: Python :: 3.7.1'],
    author='Jan Ole von Hartz',
    author_email='hartzj@cs.uni-freiburg.de',
    entry_points={
        'console_scripts': """
            ilias-downloader = src.main:main
        """
    }
)
