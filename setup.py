# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='table copy',
    version='0.2',
    url='http://github.com/gonzomember/table-copy',
    author=u'Paweł Gorzelany',
    author_email='pawel.gorzelany@gmail.com',
    description='Allows for copying database tables.',
    packages=['table_copy'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'MySQL-python'
    ],
    tests_require=[
        'mock'
    ],
    entry_points={
        'console_scripts': [
            'table-copy = table_copy:main'
        ]
    },
    test_suite='tests',
)
