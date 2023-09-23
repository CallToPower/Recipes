#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Denis Meyer
#
# This file is part of Rezepte.
#

"""About dialog"""

import logging

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QDialog, QDesktopWidget, QGridLayout, QLabel

from lib.AppConfig import app_conf_get

class AboutDialog(QDialog):
    """Main window GUI"""

    def __init__(self, i18n, image_cache):
        """Initializes the about dialog
        
        :param i18n: The I18n
        :param image_cache: The image cache
        """
        super(AboutDialog, self).__init__()

        logging.debug('Initializing AboutDialog')

        self.i18n = i18n
        self.image_cache = image_cache

        self.font_label = QFont()
        self.grid = QGridLayout()

        self.setModal(True)

    def init_ui(self):
        """Initiates about dialog UI"""
        logging.debug('Initializing AboutDialog GUI')

        self.setWindowTitle(self.i18n.translate('GUI.ABOUT.TITLE', 'About'))

        logo = self.image_cache.get_or_load_pixmap('img.logo_app', 'logo-app.png')
        if logo is not None:
            self.setWindowIcon(QIcon(logo))

        self.resize(450, 250)

        self.font_label.setBold(True)
        self.font_label.setPointSize(10)

        self._center()
        self._init_ui()

    def _init_ui(self):
        """Initializes the UI"""
        logging.debug('Initializing AboutDialog defaults')

        self.grid.setSpacing(10)

        label_empty = QLabel(' ')
        label_author = QLabel(self.i18n.translate('GUI.ABOUT.LABEL.AUTHOR', 'Author'))
        label_author.setFont(self.font_label)
        label_author_val = QLabel(app_conf_get('author'))
        label_copyright = QLabel(self.i18n.translate('GUI.ABOUT.LABEL.COPYRIGHT', 'Copyright'))
        label_copyright.setFont(self.font_label)
        label_copyright_val = QLabel(app_conf_get('copyright'))
        label_version = QLabel(self.i18n.translate('GUI.ABOUT.LABEL.VERSION', 'Version'))
        label_version.setFont(self.font_label)
        label_version_val = QLabel(app_conf_get('version'))
        label_build = QLabel(self.i18n.translate('GUI.ABOUT.LABEL.BUILD', 'Build'))
        label_build.setFont(self.font_label)
        label_build_val = QLabel(app_conf_get('build'))

        logo = self.image_cache.get_or_load_pixmap(f'img.logo_app-{self.i18n.language_main.lower()}', f'logo-app-{self.i18n.language_main.lower()}.png')
        if logo is not None:
            label_img = QLabel()
            label_img.setPixmap(logo.scaled(app_conf_get('about.logo.scaled.width', 280), app_conf_get('about.logo.scaled.height', 80), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            curr_gridid = 1
            self.grid.addWidget(label_img, curr_gridid, 1, 1, 2)

            curr_gridid += 1
            self.grid.addWidget(label_empty, curr_gridid, 0, 1, 3)
        else:
            curr_gridid = 0

        curr_gridid += 1
        self.grid.addWidget(label_author, curr_gridid, 0)
        self.grid.addWidget(label_author_val, curr_gridid, 1, 1, 3)

        curr_gridid += 1
        self.grid.addWidget(label_copyright, curr_gridid, 0)
        self.grid.addWidget(label_copyright_val, curr_gridid, 1, 1, 3)

        curr_gridid += 1
        self.grid.addWidget(label_version, curr_gridid, 0)
        self.grid.addWidget(label_version_val, curr_gridid, 1, 1, 3)

        curr_gridid += 1
        self.grid.addWidget(label_build, curr_gridid, 0)
        self.grid.addWidget(label_build_val, curr_gridid, 1, 1, 3)

        self.setLayout(self.grid)

    def _center(self):
        """Centers the window on the screen"""
        screen = QDesktopWidget().screenGeometry()
        self.move(int((screen.width() - self.geometry().width()) / 2),
                  int((screen.height() - self.geometry().height()) / 2))
