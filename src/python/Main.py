#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Denis Meyer
#
# This file is part of Rezepte.
#

"""Main"""

import os
import logging

from lib.AppConfig import app_conf_get, get_loglevel
from gui.MainGui import MainGUI

def _initialize_logger():
    """Initializes the logger"""
    if app_conf_get('logging.log_to_file'):
        basedir = os.path.dirname(app_conf_get('logging.logfile'))

        if not os.path.exists(basedir):
            os.makedirs(basedir)

    _lvl = get_loglevel()

    logging.basicConfig(level=_lvl,
                        format=app_conf_get('logging.format'),
                        datefmt=app_conf_get('logging.datefmt'))

    if app_conf_get('logging.log_to_file'):
        handler_file = logging.FileHandler(app_conf_get('logging.logfile'), mode='w', encoding=None, delay=False)
        handler_file.setLevel(_lvl)
        handler_file.setFormatter(logging.Formatter(fmt=app_conf_get('logging.format'), datefmt=app_conf_get('logging.datefmt')))
        logging.getLogger().addHandler(handler_file)

if __name__ == '__main__':
    print('Current working directory: {}'.format(os.getcwd()))

    _initialize_logger()

    basedir = os.path.dirname(__file__)

    gui = MainGUI(basedir)
    gui.run()
