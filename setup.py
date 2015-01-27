#!/usr/bin/env python

# -*- coding: utf-8 -*-
# setup.py

from distutils.core import setup
import glob
import py2exe

options = {
    "py2exe":
    {
        "compressed": 1,
        "optimize": 2,
        "bundle_files": 1,
    }
}

data_files = ['conf_zdd.txt','conf_zmj.txt']

setup(
    console=[
        {
            'script':"heji_main.py",
            "icon_resources": [(1, "main.ico")]
        }],
    name = 'heji',
    options=options,
    zipfile=None,
    data_files=data_files,
)

