#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Denis Meyer
#
# This file is part of Rezepte.
#

"""Main window"""

import logging

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QMenuBar, QAction, QFileDialog

from lib.Utils import is_macos
from i18n.I18n import I18n

from gui.data.IconDefinitions import FLAG_DE, FLAG_EN, SELECT_RECIPE_DIR, ABOUT, QUIT
from gui.enums.Language import Language
from gui.components.Widget import Widget
from gui.components.AboutDialog import AboutDialog

from lib.AppConfig import app_conf_get


class MainWindow(QMainWindow):
    """Main window GUI"""

    def __init__(self, settings, i18n, image_cache):
        """Initializes the main window

        :param settings: The settings
        :param i18n: The i18n
        :param image_cache: The image cache
        """
        super().__init__()

        logging.debug('Initializing MainWindow')

        self.settings = settings
        self.i18n = i18n
        self.image_cache = image_cache

        self.state = None

    def init_ui(self):
        """Initiates application UI"""
        logging.debug('Initializing MainWindow GUI')

        self._init_menu()

        self.setWindowTitle(self.i18n.translate('GUI.MAIN.WINDOW.TITLE', 'Recipes'))
        self.statusbar = self.statusBar()

        self.config = {}

        self._init_widgets()

        self.resize(self.settings.window['width'], self.settings.window['height'])

        self._center()

    # @override
    def closeEvent(self, event):
        """Close Event
        :param event: The event
        """
        logging.info('Quitting')
        self._quit_application()

    def _show_about_dialog(self):
        """Displays the about dialog"""
        logging.debug('Displaying AboutDialog')
        about = AboutDialog(i18n=self.i18n, image_cache=self.image_cache)
        about.init_ui()
        about.exec_()

    def _change_language_lang_de(self):
        """Changes language to DE"""
        logging.info('Change language to DE')
        self._change_language(Language.DE)

    def _change_language_lang_en(self):
        """Changes language to EN"""
        logging.info('Change language to EN')
        self._change_language(Language.EN)

    def _select_recipe_dir(self):
        """Selects the recipe directory"""
        logging.info('Select recipe dir')

        dirname = QFileDialog.getExistingDirectory(self, self.i18n.translate('GUI.SELECT_RECIPE_DIR.DIALOG.SELECT'), self.settings.recipe_folder, QFileDialog.ShowDirsOnly)
        if dirname:
            logging.info('Selected recipe directory: "{}"'.format(dirname))
            self.settings.recipe_folder = dirname
            self.settings.save()

            self._reset_phases()
            self._init_menu()
            self._init_widgets()
        else:
            logging.debug('Cancelled selecting output directory')

    def _quit_application(self):
        """Quits the application"""
        logging.info('Quitting')
        QCoreApplication.exit(0)

    def _init_menu(self):
        """Initializes the menu bar"""
        logging.debug('Initializing the menu bar')

        menu_bar = QMenuBar() if is_macos() else self.menuBar()

        menu_bar.clear()

        menu_application = menu_bar.addMenu(self.i18n.translate('GUI.MAIN.MENU.APPNAME', 'Recipes'))

        action_about = QAction(self.i18n.translate('GUI.MAIN.MENU.ITEM.ABOUT', 'About'), self)
        action_about.setShortcut('Ctrl+A')
        action_about.triggered.connect(self._show_about_dialog)
        icon = self.image_cache.get_or_load_icon(ABOUT)
        action_about.setIcon(icon)

        action_quit = QAction(self.i18n.translate('GUI.MAIN.MENU.ITEM.QUIT', 'Quit'), self)
        action_quit.setShortcut('Ctrl+Q')
        action_quit.triggered.connect(self._quit_application)
        icon = self.image_cache.get_or_load_icon(QUIT)
        action_quit.setIcon(icon)

        menu_application.addAction(action_about)
        menu_application.addAction(action_quit)

        menu_language = menu_bar.addMenu(self.i18n.translate('GUI.MAIN.MENU.LANGUAGE', 'Language'))

        action_lang_de = QAction(self.i18n.translate('GUI.MAIN.MENU.ITEM.LANGUAGE.DE', 'Deutsch'), self)
        action_lang_de.setShortcut('Ctrl+1')
        action_lang_de.triggered.connect(self._change_language_lang_de)
        icon = self.image_cache.get_or_load_icon(FLAG_DE)
        action_lang_de.setIcon(icon)

        action_lang_en = QAction(self.i18n.translate('GUI.MAIN.MENU.ITEM.LANGUAGE.EN', 'English'), self)
        action_lang_en.setShortcut('Ctrl+2')
        action_lang_en.triggered.connect(self._change_language_lang_en)
        icon = self.image_cache.get_or_load_icon(FLAG_EN)
        action_lang_en.setIcon(icon)

        menu_language.addAction(action_lang_de)
        menu_language.addAction(action_lang_en)

        menu_settings = menu_bar.addMenu(self.i18n.translate('GUI.MAIN.MENU.SETTINGS', 'Settings'))

        action_settings_select_recipe_dir = QAction(self.i18n.translate('GUI.MAIN.MENU.ITEM.SETTINGS.SELECT_RECIPE_DIR', 'Select Recipe Directory'), self)
        action_settings_select_recipe_dir.setShortcut('Ctrl+O')
        action_settings_select_recipe_dir.triggered.connect(self._select_recipe_dir)
        icon = self.image_cache.get_or_load_icon(SELECT_RECIPE_DIR)
        action_settings_select_recipe_dir.setIcon(icon)

        menu_settings.addAction(action_settings_select_recipe_dir)

    def _center(self):
        """Centers the window on the screen"""
        screen = QDesktopWidget().screenGeometry()
        self.move(int((screen.width() - self.geometry().width()) / 2),
                  int((screen.height() - self.geometry().height()) / 2))

    def _change_language(self, lang):
        """Changes the language

        :param lang: The language
        """
        logging.info('Changing language to {}'.format(lang))
        self.i18n.change_language(lang)
        self.settings.save()

        self._reset_phases()
        self.setWindowTitle(self.i18n.translate('GUI.MAIN.WINDOW.TITLE'))
        self._init_menu()
        self._init_widgets()

    def _reset_phases(self):
        """Resets phases"""
        logging.info('Resetting phases')

        self.setCentralWidget(None)

        self.config = {}

        self._init_widgets()

    def _init_widgets(self):
        """Initializes widgets"""
        logging.info('Initializing widgets')

        widget = Widget(i18n=self.i18n,
                        settings=self.settings,
                        log=self.show_message,
                        image_cache=self.image_cache)
        widget.init_ui()
        self.setCentralWidget(widget)

        self.show_message(self.i18n.translate('GUI.MAIN.LOG.TREEVIEW'))

    def show_message(self, msg=''):
        """Shows a message in the status bar

        :param msg: The message to be displayed
        """
        self.statusBar().showMessage(msg)
