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
import urllib.request
import json
from pathlib import Path

from lib.AppConfig import app_conf_get
from lib.Settings import Settings
from gui.MainGui import GUI
from i18n.I18n import I18n
from gui.enums.Language import Language


def _initialize_logger():
    """Initializes the logger"""
    if app_conf_get('logging.log_to_file'):
        basedir = os.path.dirname(app_conf_get('logging.logfile'))

        if not os.path.exists(basedir):
            os.makedirs(basedir)

    logging.basicConfig(level=app_conf_get('logging.loglevel'),
                        format=app_conf_get('logging.format'),
                        datefmt=app_conf_get('logging.datefmt'))

    if app_conf_get('logging.log_to_file'):
        handler_file = logging.FileHandler(
            app_conf_get('logging.logfile'), mode='w', encoding=None, delay=False)
        handler_file.setLevel(app_conf_get('logging.loglevel'))
        handler_file.setFormatter(logging.Formatter(
            fmt=app_conf_get('logging.format'), datefmt=app_conf_get('logging.datefmt')))
        logging.getLogger().addHandler(handler_file)


if __name__ == '__main__':
    print('Current working directory: {}'.format(os.getcwd()))

    _initialize_logger()

    
    i18n = I18n(Language.DE)
    settings_basedir = str(Path.home())
    settings = Settings(settings_basedir, app_conf_get('settings.filename'), i18n)

    basedir = os.path.dirname(__file__)
    gui = GUI(basedir, settings, i18n)
    gui.run()
