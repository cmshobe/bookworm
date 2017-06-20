# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 15:10:15 2017

@author: Charlie

setup.py for bookworm
"""

from setuptools import setup, find_packages

setup(
    name="bookworm",
    version='0.1',
    py_modules=['bookworm'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        start_new_booklist=bookworm.bookworm:start_new_booklist
        add_new_book=bookworm.bookworm:add_new_book
        plot_author_gender=bookworm.bookworm:plot_author_gender
        export_to_csv=bookworm.bookworm:export_to_csv
    ''',
)