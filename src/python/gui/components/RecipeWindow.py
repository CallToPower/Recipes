#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Denis Meyer
#
# This file is part of Rezepte.
#

"""Recipe window"""

import logging
import platform

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QMenuBar, QAction, QFileDialog, QLabel, QWidget, QSizePolicy, QGridLayout, QTableView, QHeaderView

from i18n.I18n import I18n
from gui.components.IngredientsTableModel import IngredientsTableModel
from gui.components.StepsTableModel import StepsTableModel
from gui.components.LinksTableModel import LinksTableModel

from lib.AppConfig import app_conf_get

class RecipeWindow(QMainWindow):
    """Recipe window GUI"""

    def __init__(self, settings, i18n, id, recipe, close_cb):
        """Initializes the recipe window

        :param settings: The settings
        :param i18n: The i18n
        :param id: The window ID
        :param recipe: The Recipe
        :param close_cb: Callback when the window closes
        """
        super().__init__()

        logging.debug('Initializing RecipeWindow')

        self.settings = settings
        self.i18n = i18n
        self.id = id
        self.recipe = recipe
        self.close_cb = close_cb

    def init_ui(self):
        """Initiates UI"""
        logging.debug('Initializing RecipeWindow GUI')

        self._init_menu()

        self.setWindowTitle(self.recipe.name)
        self.statusbar = self.statusBar()
        self.show_message(self.i18n.translate('GUI.MAIN.LOG.RECIPE').format(self.recipe.name))

        self._init_widgets()

        self.resize(app_conf_get('window.recipe.width'), app_conf_get('window.recipe.height'))

        self._center()

    def _init_menu(self):
        """Initializes the menu bar"""
        logging.debug('Initializing the menu bar')
        
        if platform.uname().system.startswith('Darw'):
            logging.debug('Platform is Mac OS')
            self.menu_bar = QMenuBar()
        else:
            logging.debug('Platform is not Mac OS')
            self.menu_bar = self.menuBar()

        self.menu_bar.clear()

        menu_application = self.menu_bar.addMenu(self.i18n.translate('GUI.RECIPE.MENU.RECIPE.NAME'))

        action_close = QAction(self.i18n.translate('GUI.RECIPE.MENU.ITEM.CLOSE'), self)
        action_close.setShortcut('Ctrl+C')
        action_close.triggered.connect(self._close)

        menu_application.addAction(action_close)


    def _init_widgets(self):
        """Initializes widgets"""
        logging.info('Initializing widgets')

        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)

        self.font_label_header = QFont()
        self.font_label_header.setBold(True)
        self.font_label_header.setPointSize(app_conf_get('label.header.font.size', 20))

        self.font_label_info = QFont()
        self.font_label_info.setBold(False)
        self.font_label_info.setPointSize(app_conf_get('label.info.font.size', 16))

        self.line_css = 'background-color: #c0c0c0;'

        # Components

        self.label_header = QLabel(self.recipe.name)
        self.label_header.setFont(self.font_label_header)
        self.label_header.setAlignment(Qt.AlignCenter)

        self.label_ingredients_line_1 = QWidget()
        self.label_ingredients_line_1.setFixedHeight(1)
        self.label_ingredients_line_1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.label_ingredients_line_1.setStyleSheet(self.line_css)

        self.label_ingredients = QLabel(self.i18n.translate('GUI.RECIPE.VIEW.HEADERS.INGREDIENTS'))
        self.label_ingredients.setFont(self.font_label_info)
        self.label_ingredients.setAlignment(Qt.AlignCenter)

        self.label_ingredients_line_2 = QWidget()
        self.label_ingredients_line_2.setFixedHeight(1)
        self.label_ingredients_line_2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.label_ingredients_line_2.setStyleSheet(self.line_css)

        self.table_ingredients = QTableView()
        headers_h_ingredients = [self.i18n.translate('GUI.RECIPE.HEADERS.QUANTITY'), self.i18n.translate('GUI.RECIPE.HEADERS.NAME'), self.i18n.translate('GUI.RECIPE.HEADERS.ADDITION')]
        self.model_ingredients = IngredientsTableModel(self.recipe.ingredients, headers_h=headers_h_ingredients, cb_change=self._on_ingredients_changed)
        self.table_ingredients.setModel(self.model_ingredients)
        self.table_ingredients.resizeRowsToContents()
        self.table_ingredients.resizeColumnsToContents()
        self.table_ingredients.setWordWrap(True)
        header_h_ingredients = self.table_ingredients.horizontalHeader()
        for i in range(0, max(0, len(self.model_ingredients._headers_h) - 2)):
            header_h_ingredients.setSectionResizeMode(i, QHeaderView.ResizeToContents)
        header_h_ingredients.setSectionResizeMode(max(0, len(self.model_ingredients._headers_h) - 1), QHeaderView.Stretch)
        header_v_ingredients = self.table_ingredients.verticalHeader()
        for i in range(0, len(self.model_ingredients._headers_v)):
            header_v_ingredients.setSectionResizeMode(i, QHeaderView.ResizeToContents)
        header_v_ingredients.setVisible(False)

        self.label_steps_line_1 = QWidget()
        self.label_steps_line_1.setFixedHeight(1)
        self.label_steps_line_1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.label_steps_line_1.setStyleSheet(self.line_css)

        self.label_steps = QLabel(self.i18n.translate('GUI.RECIPE.VIEW.HEADERS.STEPS'))
        self.label_steps.setFont(self.font_label_info)
        self.label_steps.setAlignment(Qt.AlignCenter)

        self.label_steps_line_2 = QWidget()
        self.label_steps_line_2.setFixedHeight(1)
        self.label_steps_line_2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.label_steps_line_2.setStyleSheet(self.line_css)

        self.table_steps = QTableView()
        self.model_steps = StepsTableModel(self.recipe.steps, cb_change=self._on_steps_changed)
        self.table_steps.setModel(self.model_steps)
        self.table_steps.resizeRowsToContents()
        self.table_steps.resizeColumnsToContents()
        self.table_steps.setWordWrap(True)
        header_h_steps = self.table_steps.horizontalHeader()
        for i in range(0, max(0, len(self.model_steps._headers_h) - 2)):
            header_h_steps.setSectionResizeMode(i, QHeaderView.ResizeToContents)
        header_h_steps.setSectionResizeMode(max(0, len(self.model_steps._headers_h) - 1), QHeaderView.Stretch)
        header_h_steps.setVisible(False)
        header_v_steps = self.table_steps.verticalHeader()
        for i in range(0, len(self.model_steps._headers_v)):
            header_v_steps.setSectionResizeMode(i, QHeaderView.ResizeToContents)

        self.label_links_line_1 = QWidget()
        self.label_links_line_1.setFixedHeight(1)
        self.label_links_line_1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.label_links_line_1.setStyleSheet(self.line_css)

        self.label_links = QLabel(self.i18n.translate('GUI.RECIPE.VIEW.HEADERS.LINKS'))
        self.label_links.setFont(self.font_label_info)
        self.label_links.setAlignment(Qt.AlignCenter)

        self.label_links_line_2 = QWidget()
        self.label_links_line_2.setFixedHeight(1)
        self.label_links_line_2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.label_links_line_2.setStyleSheet(self.line_css)
        
        self.table_links = QTableView()
        self.model_links = LinksTableModel(self.recipe.links, cb_change=self._on_links_changed)
        self.table_links.setModel(self.model_links)
        self.table_links.resizeRowsToContents()
        self.table_links.resizeColumnsToContents()
        self.table_links.setWordWrap(True)
        header_h_links = self.table_links.horizontalHeader()
        for i in range(0, max(0, len(self.model_links._headers_h) - 2)):
            header_h_links.setSectionResizeMode(i, QHeaderView.ResizeToContents)
        header_h_links.setSectionResizeMode(max(0, len(self.model_links._headers_h) - 1), QHeaderView.Stretch)
        header_v_links = self.table_links.verticalHeader()
        for i in range(0, len(self.model_links._headers_v)):
            header_v_links.setSectionResizeMode(i, QHeaderView.ResizeToContents)

        # Layout

        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        # self.grid.addWidget(widget, row, column, rowspan, columnspan)

        curr_gridid = 0
        self.grid.setRowStretch(curr_gridid, 0)
        self.grid.addWidget(self.label_header, curr_gridid, 0, 1, 10)

        curr_gridid += 1
        self.grid.setRowStretch(curr_gridid, 0)
        self.grid.addWidget(self.label_ingredients_line_1, curr_gridid, 0, 1, 4)
        self.grid.addWidget(self.label_ingredients, curr_gridid, 4, 1, 2)
        self.grid.addWidget(self.label_ingredients_line_2, curr_gridid, 6, 1, 4)

        curr_gridid += 1
        self.grid.setRowStretch(curr_gridid, 1)
        self.grid.addWidget(self.table_ingredients, curr_gridid, 0, 5, 10)

        curr_gridid += 5
        self.grid.setRowStretch(curr_gridid, 0)
        self.grid.addWidget(self.label_steps_line_1, curr_gridid, 0, 1, 4)
        self.grid.addWidget(self.label_steps, curr_gridid, 4, 1, 2)
        self.grid.addWidget(self.label_steps_line_2, curr_gridid, 6, 1, 4)

        curr_gridid += 1
        self.grid.setRowStretch(curr_gridid, 1)
        self.grid.addWidget(self.table_steps, curr_gridid, 0, 5, 10)

        curr_gridid += 5
        self.grid.setRowStretch(curr_gridid, 0)
        self.grid.addWidget(self.label_links_line_1, curr_gridid, 0, 1, 4)
        self.grid.addWidget(self.label_links, curr_gridid, 4, 1, 2)
        self.grid.addWidget(self.label_links_line_2, curr_gridid, 6, 1, 4)

        curr_gridid += 1
        self.grid.setRowStretch(curr_gridid, 0)
        self.grid.addWidget(self.table_links, curr_gridid, 0, 1, 10)

        self.widget.setLayout(self.grid)

    def _on_ingredients_changed(self, lst):
        """On ingredients changed
        :param lst: Ingredients list
        """
        print(lst)

    def _on_steps_changed(self, lst):
        """On steps changed
        :param lst: Steps list
        """
        print(lst)

    def _on_links_changed(self, lst):
        """On links changed
        :param lst: Links list
        """
        print(lst)

    def _center(self):
        """Centers the window on the screen"""
        screen = QDesktopWidget().screenGeometry()
        self.move(int((screen.width() - self.geometry().width()) / 2),
                  int((screen.height() - self.geometry().height()) / 2))

    def _close(self):
        """Close window"""
        logging.debug('Closing window')
        self.close()

    def closeEvent(self, _e):
        """Window close event
        
        :param _e: _e [unused]
        """
        logging.debug('Window close triggered')
        if self.close_cb:
            self.close_cb(self.id)

    def show_message(self, msg=''):
        """Shows a message in the status bar

        :param msg: The message to be displayed
        """
        self.statusBar().showMessage(msg)
