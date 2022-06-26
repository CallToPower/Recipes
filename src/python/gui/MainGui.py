#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Denis Meyer
#
# This file is part of Rezepte.
#

"""GUI"""

import logging
import sys

from PyQt5 import QtWidgets

from lib.ImageCache import ImageCache
from gui.components.MainWindow import MainWindow

class GUI():
    """Main GUI"""

    def __init__(self, basedir, settings, i18n):
        """Initializes the GUI
        
        :param basedir: The base directory
        :param settings: The settings
        :param i18n: The i18n
        """
        logging.debug('Initializing MainGUI')
        self.basedir = basedir
        self.settings = settings
        self.i18n = i18n

        self.image_cache = ImageCache(self.basedir)


    def run(self):
        """Initializes and shows the GUI"""
        logging.debug('Initializing AppContext GUI')

        app = QtWidgets.QApplication(sys.argv)

        self.main_window = MainWindow(self.settings, self.i18n, image_cache=self.image_cache)
        self.main_window.init_settings()
        self.main_window.init_ui()
        self.main_window.show()

        app.exec()

        sys.exit(0)
