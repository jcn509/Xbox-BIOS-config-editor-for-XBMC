# coding: utf-8
# (c) 2020, Josh Neil <joshneil8@gmail.com>
# License: MIT

import os
from setuptools import setup, find_packages

setup(
    name="configeditor",
    author="Josh Neil",
    version="1.0.0",
    package_dir={"": "script.ind_bios_config_editor/resources"},
    packages=find_packages("./script.ind_bios_config_editor/resources"),
    extras_require={"dev": ["pytest", "pytype"]},
    install_requires=[
        "Kodistubs",
        "pyxbmct @ git+https://github.com/romanvm/script.module.pyxbmct@master",
    ],
    zip_safe=False,
)
