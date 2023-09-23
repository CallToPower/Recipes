#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Denis Meyer
#
# This file is part of Rezepte.
#

"""Main GUI"""

import logging
import sys

from PyQt5 import QtWidgets

from i18n.I18n import I18n
from gui.components.MainWindow import MainWindow

from lib.ImageCache import ImageCache
from lib.Utils import _load_conf_from_home_folder, save_conf, update_logging, verify_recipes_dir
from lib.AppConfig import app_conf_get, app_conf_set, get_public_values

class MainGUI():
    """Main GUI"""

    def __init__(self, basedir):
        """Initializes the GUI
        
        :param basedir: The base directory
        """
        logging.debug('Initializing MainGUI')

        self.basedir = basedir
        self.main_window = None

        self._init()

    def _init(self):
        """Initializes the GUI"""
        conf_loaded, conf = _load_conf_from_home_folder()

        if conf_loaded:
            for key, val in conf.items():
                logging.debug('Overwriting config entry "%s": "%s"', key, val)
                app_conf_set(key, val)
        else:
            save_conf(get_public_values())

        verify_recipes_dir()

        update_logging(app_conf_get('logging.loglevel'), logtofile=app_conf_get('logging.log_to_file'))

        self.image_cache = ImageCache(self.basedir)
        self.i18n = I18n(self.basedir, lang=app_conf_get('language.main'))

    def run(self):
        """Initializes and shows the GUI"""
        logging.debug('Initializing AppContext GUI')

        app = QtWidgets.QApplication(sys.argv)

        self.main_window = MainWindow(i18n=self.i18n, image_cache=self.image_cache)
        self.main_window.init_ui()
        self.main_window.show()

        app.exec()

        sys.exit(0)
