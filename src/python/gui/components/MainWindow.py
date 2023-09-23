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
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QMenuBar, QAction, QFileDialog

from gui.data.IconDefinitions import SELECT_RECIPE_DIR, ABOUT, QUIT, get_flag
from gui.components.Widget import Widget
from gui.components.AboutDialog import AboutDialog
 
from lib.Utils import is_macos, save_conf
from lib.AppConfig import app_conf_get, app_conf_set, get_public_values

class MainWindow(QMainWindow):
    """Main window GUI"""

    def __init__(self, i18n, image_cache):
        """Initializes the main window

        :param i18n: The i18n
        :param image_cache: The image cache
        """
        super(MainWindow, self).__init__()

        logging.debug('Initializing MainWindow')

        self.i18n = i18n
        self.image_cache = image_cache

        self.statusbar = None

    def init_ui(self):
        """Initiates application UI"""
        logging.debug('Initializing MainWindow GUI')

        self._init_menu()

        self.setWindowTitle(self.i18n.translate('GUI.MAIN.WINDOW.TITLE', 'Recipes'))
        self.statusbar = self.statusBar()

        logo = self.image_cache.get_or_load_pixmap('img.logo_app', 'logo-app.png')
        if logo is not None:
            self.setWindowIcon(QIcon(logo))

        self._init_widgets()

        self.resize(app_conf_get('window.recipe.width', 800), app_conf_get('window.recipe.height', 600))

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

    def _select_recipe_dir(self):
        """Selects the recipe directory"""
        logging.info('Select recipe dir')

        dirname = QFileDialog.getExistingDirectory(self, self.i18n.translate('GUI.SELECT_RECIPE_DIR.DIALOG.SELECT'), app_conf_get('recipes.folder'), QFileDialog.ShowDirsOnly)
        if dirname:
            logging.info('Selected recipe directory: "%s"', dirname)
            app_conf_set('recipes.folder', dirname)
            save_conf(get_public_values())

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

        if len(self.i18n.languages) > 1:
            menu_language = menu_bar.addMenu(self.i18n.translate('GUI.MAIN.MENU.LANGUAGE', 'Language'))

            for lang in self.i18n.languages:
                action = QAction(lang, self)
                flag = self.image_cache.get_or_load_icon(get_flag(lang))
                if flag:
                    action.setIcon(flag)
                action.triggered.connect(self._action_change_language)
                menu_language.addAction(action)

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

    def _action_change_language(self):
        self._change_language(self.sender().text())

    def _change_language(self, lang):
        """Changes the language

        :param lang: The language
        """
        if lang == self.i18n.language_main:
            return

        self.i18n.change_language(lang)
        app_conf_set('language.main', lang)
        save_conf(get_public_values())

        self._reset_phases()
        self.setWindowTitle(self.i18n.translate('GUI.MAIN.WINDOW.TITLE'))
        self._init_menu()
        self._init_widgets()

    def _reset_phases(self):
        """Resets phases"""
        logging.info('Resetting phases')

        self.setCentralWidget(None)

        self._init_widgets()

    def _init_widgets(self):
        """Initializes widgets"""
        logging.info('Initializing widgets')

        widget = Widget(i18n=self.i18n,
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
