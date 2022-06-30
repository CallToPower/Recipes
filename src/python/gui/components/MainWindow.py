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
from gui.enums.Language import Language
from gui.components.TreeViewUI import TreeViewUI
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

    def init_settings(self):
        """Initializes the settings"""
        logging.debug('Initializing Settings')
        self.settings.load()
        if not self.settings.loaded_from_file:
            self.settings.save()
        self.i18n.change_language(self.settings.language)

    def init_ui(self):
        """Initiates application UI"""
        logging.debug('Initializing MainWindow GUI')

        self._init_menu()

        self.setWindowTitle(self.i18n.translate('GUI.MAIN.WINDOW.TITLE'))
        self.statusbar = self.statusBar()

        self.config = {}

        self._init_widgets()

        self.resize(self.settings.window['width'], self.settings.window['height'])

        self._center()

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
            logging.info('Cancelled selecting output directory')

    def _quit_application(self):
        """Quits the application"""
        logging.info('Quitting')
        QCoreApplication.exit(0)

    def _init_menu(self):
        """Initializes the menu bar"""
        logging.debug('Initializing the menu bar')

        self.menu_bar = QMenuBar() if is_macos() else self.menuBar()

        self.menu_bar.clear()

        menu_application = self.menu_bar.addMenu(self.i18n.translate('GUI.MAIN.MENU.APPNAME'))

        action_about = QAction(self.i18n.translate('GUI.MAIN.MENU.ITEM.ABOUT'), self)
        action_about.setShortcut('Ctrl+A')
        action_about.triggered.connect(self._show_about_dialog)

        action_quit = QAction(self.i18n.translate('GUI.MAIN.MENU.ITEM.QUIT'), self)
        action_quit.setShortcut('Ctrl+Q')
        action_quit.triggered.connect(self._quit_application)

        menu_application.addAction(action_about)
        menu_application.addAction(action_quit)

        menu_language = self.menu_bar.addMenu(self.i18n.translate('GUI.MAIN.MENU.LANGUAGE'))

        action_lang_de = QAction(self.i18n.translate('GUI.MAIN.MENU.ITEM.LANGUAGE.DE'), self)
        action_lang_de.setShortcut('Ctrl+1')
        action_lang_de.triggered.connect(self._change_language_lang_de)
        flag_de = self.image_cache.get_or_load_icon('img.flag.de', 'de.png', 'flags')
        action_lang_de.setIcon(flag_de)

        action_lang_en = QAction(self.i18n.translate('GUI.MAIN.MENU.ITEM.LANGUAGE.EN'), self)
        action_lang_en.setShortcut('Ctrl+2')
        action_lang_en.triggered.connect(self._change_language_lang_en)
        flag_en = self.image_cache.get_or_load_icon('img.flag.en', 'en.png', 'flags')
        action_lang_en.setIcon(flag_en)

        menu_language.addAction(action_lang_de)
        menu_language.addAction(action_lang_en)

        menu_settings = self.menu_bar.addMenu(self.i18n.translate('GUI.MAIN.MENU.SETTINGS'))

        action_settings_select_recipe_dir = QAction(self.i18n.translate('GUI.MAIN.MENU.ITEM.SETTINGS.SELECT_RECIPE_DIR'), self)
        action_settings_select_recipe_dir.setShortcut('Ctrl+R')
        action_settings_select_recipe_dir.triggered.connect(self._select_recipe_dir)
        
        menu_settings.addAction(action_settings_select_recipe_dir)

    def _center(self):
        """Centers the window on the screen"""
        screen = QDesktopWidget().screenGeometry()
        self.move(int((screen.width() - self.geometry().width()) / 2),
                  int((screen.height() - self.geometry().height()) / 2))

    def _set_state(self, state):
        """Sets the state

        :param state: The state
        """
        logging.debug('Setting phase: {}'.format(state.name))
        self.state = state

    def _is_in_state(self, state):
        """Checks whether is in a given state

        :param state: The state to check
        """
        return self.state == state

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

    def _prepare_widgets(self):
        """Prepares the widgets"""

    def _reset_phases(self):
        """Resets phases"""
        logging.info('Resetting phases')

        self.setCentralWidget(None)
        self.tree_view_ui = None

        self.config = {}

        self._init_widgets()

    def _init_widgets(self):
        """Initializes widgets"""
        logging.info('Initializing widgets')

        self.tree_view_ui = TreeViewUI(i18n=self.i18n,
                                       settings=self.settings,
                                       log=self.show_message,
                                       image_cache=self.image_cache)
        self.tree_view_ui.init_ui()
        self.setCentralWidget(self.tree_view_ui)

        self.show_message(self.i18n.translate('GUI.MAIN.LOG.TREEVIEW'))

    def show_message(self, msg=''):
        """Shows a message in the status bar

        :param msg: The message to be displayed
        """
        self.statusBar().showMessage(msg)
