#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Denis Meyer
#
# This file is part of Rezepte.
#

"""Recipe window"""

import logging

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QMenuBar, QAction, QFileDialog, QLabel, QWidget, QSizePolicy, QGridLayout, QTableView, QHeaderView, QPushButton, QAbstractItemView

from lib.Utils import is_macos
from i18n.I18n import I18n
from gui.components.IngredientsTableModel import IngredientsTableModel
from gui.components.StepsTableModel import StepsTableModel
from gui.components.LinksTableModel import LinksTableModel

from lib.AppConfig import app_conf_get
from lib.Utils import save_recipe

class RecipeWindow(QMainWindow):
    """Recipe window GUI"""

    def __init__(self, settings, i18n, path_info, recipe, close_cb):
        """Initializes the recipe window

        :param settings: The settings
        :param i18n: The i18n
        :param path_info: The path info
        :param recipe: The Recipe
        :param close_cb: Callback when the window closes
        """
        super().__init__()

        logging.debug('Initializing RecipeWindow')

        self.settings = settings
        self.i18n = i18n
        self.path_info = path_info
        self.recipe = recipe
        self.close_cb = close_cb
        
        self._changed = False

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

        self.menu_bar = QMenuBar() if is_macos() else self.menuBar()

        self.menu_bar.clear()

        menu_application = self.menu_bar.addMenu(self.i18n.translate('GUI.RECIPE.MENU.RECIPE.NAME'))

        action_close = QAction(self.i18n.translate('GUI.RECIPE.MENU.ITEM.CLOSE'), self)
        action_close.setShortcut('Ctrl+C')
        action_close.triggered.connect(self._close)

        menu_application.addAction(action_close)


    def _init_widgets(self):
        """Initializes widgets"""
        logging.info('Initializing widgets')

        widget = QWidget(self)
        self.setCentralWidget(widget)

        font_label_header = QFont()
        font_label_header.setBold(True)
        font_label_header.setPointSize(app_conf_get('label.header.font.size', 20))

        font_label_info = QFont()
        font_label_info.setBold(False)
        font_label_info.setPointSize(app_conf_get('label.info.font.size', 16))

        line_css = 'background-color: #c0c0c0;'
        bgcolor_header_css = 'background-color: rgb(230, 230, 230);'

        # Components

        label_header = QLabel(self.recipe.name)
        label_header.setFont(font_label_header)
        label_header.setAlignment(Qt.AlignCenter)

        label_ingredients_line = QWidget()
        label_ingredients_line.setFixedHeight(1)
        label_ingredients_line.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        label_ingredients_line.setStyleSheet(line_css)

        label_ingredients = QLabel(self.i18n.translate('GUI.RECIPE.VIEW.HEADERS.INGREDIENTS'))
        label_ingredients.setFont(font_label_info)
        label_ingredients.setAlignment(Qt.AlignLeft)

        button_remove_ingredient = QPushButton(self.i18n.translate('GUI.RECIPE.VIEW.ACTIONS.INGREDIENTS.REMOVE'))
        button_remove_ingredient.clicked[bool].connect(self._remove_ingredient)
        button_add_ingredient = QPushButton(self.i18n.translate('GUI.RECIPE.VIEW.ACTIONS.INGREDIENTS.ADD'))
        button_add_ingredient.clicked[bool].connect(self._add_ingredient)

        self.table_ingredients = QTableView()
        self.table_ingredients.setStyleSheet('QHeaderView::section { ' + bgcolor_header_css + ' }')
        self.table_ingredients.setSelectionMode(QAbstractItemView.SingleSelection)
        self.model_ingredients = IngredientsTableModel(self.i18n, self.recipe.ingredients, cb_change=self._on_ingredients_changed)
        self.table_ingredients.setModel(self.model_ingredients)
        self.table_ingredients.resizeRowsToContents()
        self.table_ingredients.resizeColumnsToContents()
        self.table_ingredients.setWordWrap(True)
        header_h_ingredients = self.table_ingredients.horizontalHeader()
        for i in range(0, max(0, len(self.model_ingredients._headers_h) - 2)):
            header_h_ingredients.setSectionResizeMode(i, QHeaderView.ResizeToContents)
        header_h_ingredients.setSectionResizeMode(max(0, len(self.model_ingredients._headers_h) - 1), QHeaderView.Stretch)
        self._update_headers(self.table_ingredients, len(self.recipe.ingredients))
        self.table_ingredients.verticalHeader().setVisible(False)

        label_steps_line = QWidget()
        label_steps_line.setFixedHeight(1)
        label_steps_line.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        label_steps_line.setStyleSheet(line_css)

        label_steps = QLabel(self.i18n.translate('GUI.RECIPE.VIEW.HEADERS.STEPS'))
        label_steps.setFont(font_label_info)
        label_steps.setAlignment(Qt.AlignLeft)

        button_remove_step = QPushButton(self.i18n.translate('GUI.RECIPE.VIEW.ACTIONS.STEPS.REMOVE'))
        button_remove_step.clicked[bool].connect(self._remove_step)
        button_add_step = QPushButton(self.i18n.translate('GUI.RECIPE.VIEW.ACTIONS.STEPS.ADD'))
        button_add_step.clicked[bool].connect(self._add_step)

        self.table_steps = QTableView()
        self.table_steps.setStyleSheet('QHeaderView::section { ' + bgcolor_header_css + ' }')
        self.table_steps.setSelectionMode(QAbstractItemView.SingleSelection)
        self.model_steps = StepsTableModel(self.i18n, self.recipe.steps, cb_change=self._on_steps_changed)
        self.table_steps.setModel(self.model_steps)
        self.table_steps.resizeRowsToContents()
        self.table_steps.resizeColumnsToContents()
        self.table_steps.setWordWrap(True)
        header_h_steps = self.table_steps.horizontalHeader()
        for i in range(0, max(0, len(self.model_steps._headers_h) - 2)):
            header_h_steps.setSectionResizeMode(i, QHeaderView.ResizeToContents)
        header_h_steps.setSectionResizeMode(max(0, len(self.model_steps._headers_h) - 1), QHeaderView.Stretch)
        header_h_steps.setVisible(False)
        self._update_headers(self.table_steps, len(self.recipe.steps))

        label_links_line = QWidget()
        label_links_line.setFixedHeight(1)
        label_links_line.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        label_links_line.setStyleSheet(line_css)

        label_links = QLabel(self.i18n.translate('GUI.RECIPE.VIEW.HEADERS.LINKS'))
        label_links.setFont(font_label_info)
        label_links.setAlignment(Qt.AlignLeft)

        button_remove_link = QPushButton(self.i18n.translate('GUI.RECIPE.VIEW.ACTIONS.LINKS.REMOVE'))
        button_remove_link.clicked[bool].connect(self._remove_link)
        button_add_link = QPushButton(self.i18n.translate('GUI.RECIPE.VIEW.ACTIONS.LINKS.ADD'))
        button_add_link.clicked[bool].connect(self._add_link)
        
        self.table_links = QTableView()
        self.table_links.setStyleSheet('QHeaderView::section { ' + bgcolor_header_css + ' }')
        self.table_links.setSelectionMode(QAbstractItemView.SingleSelection)
        self.model_links = LinksTableModel(self.i18n, self.recipe.links, cb_change=self._on_links_changed)
        self.table_links.setModel(self.model_links)
        self.table_links.resizeRowsToContents()
        self.table_links.resizeColumnsToContents()
        self.table_links.setWordWrap(True)
        header_h_links = self.table_links.horizontalHeader()
        for i in range(0, max(0, len(self.model_links._headers_h) - 2)):
            header_h_links.setSectionResizeMode(i, QHeaderView.ResizeToContents)
        header_h_links.setSectionResizeMode(max(0, len(self.model_links._headers_h) - 1), QHeaderView.Stretch)
        self._update_headers(self.table_links, len(self.recipe.links))

        button_cancel = QPushButton(self.i18n.translate('GUI.RECIPE.VIEW.ACTIONS.CANCEL'))
        button_cancel.clicked[bool].connect(self._cancel)
        button_save = QPushButton(self.i18n.translate('GUI.RECIPE.VIEW.ACTIONS.SAVE'))
        button_save.clicked[bool].connect(self._save)

        # Layout

        layout_grid = QGridLayout()
        layout_grid.setSpacing(10)

        # layout_grid.addWidget(widget, row, column, rowspan, columnspan)

        curr_gridid = 0
        layout_grid.setRowStretch(curr_gridid, 0)
        layout_grid.addWidget(label_header, curr_gridid, 0, 1, 10)

        curr_gridid += 1
        layout_grid.setRowStretch(curr_gridid, 0)
        layout_grid.addWidget(label_ingredients, curr_gridid, 0, 1, 1)
        layout_grid.addWidget(label_ingredients_line, curr_gridid, 1, 1, 7)
        layout_grid.addWidget(button_remove_ingredient, curr_gridid, 8, 1, 1)
        layout_grid.addWidget(button_add_ingredient, curr_gridid, 9, 1, 1)

        curr_gridid += 1
        layout_grid.setRowStretch(curr_gridid, 1)
        layout_grid.addWidget(self.table_ingredients, curr_gridid, 0, 5, 10)

        curr_gridid += 5
        layout_grid.setRowStretch(curr_gridid, 0)
        layout_grid.addWidget(label_steps, curr_gridid, 0, 1, 1)
        layout_grid.addWidget(label_steps_line, curr_gridid, 1, 1, 7)
        layout_grid.addWidget(button_remove_step, curr_gridid, 8, 1, 1)
        layout_grid.addWidget(button_add_step, curr_gridid, 9, 1, 1)

        curr_gridid += 1
        layout_grid.setRowStretch(curr_gridid, 1)
        layout_grid.addWidget(self.table_steps, curr_gridid, 0, 5, 10)

        curr_gridid += 5
        layout_grid.setRowStretch(curr_gridid, 0)
        layout_grid.addWidget(label_links, curr_gridid, 0, 1, 1)
        layout_grid.addWidget(label_links_line, curr_gridid, 1, 1, 7)
        layout_grid.addWidget(button_remove_link, curr_gridid, 8, 1, 1)
        layout_grid.addWidget(button_add_link, curr_gridid, 9, 1, 1)

        curr_gridid += 1
        layout_grid.setRowStretch(curr_gridid, 0)
        layout_grid.addWidget(self.table_links, curr_gridid, 0, 1, 10)

        curr_gridid += 1
        layout_grid.setRowStretch(curr_gridid, 0)
        layout_grid.addWidget(button_cancel, curr_gridid, 0, 1, 5)
        layout_grid.addWidget(button_save, curr_gridid, 5, 1, 5)

        widget.setLayout(layout_grid)

    def _update_headers(self, table, len_v):
        header_v = table.verticalHeader()
        for i in range(0, len_v):
            header_v.setSectionResizeMode(i, QHeaderView.ResizeToContents)

    def _cancel(self):
        """Cancels the change"""
        logging.debug('Cancel')
        if not self._changed:
            self._close()

    def _save(self):
        """Saves the change"""
        logging.debug('Save')
        if not self._changed:
            logging.info('Nothing changed')
            return
        logging.info('Saving recipe to "{}"'.format(self.path_info))
        if save_recipe(self.recipe, self.path_info):
            self._close()
        # TODO: Dialog whether to close with changes

    def _remove_ingredient(self):
        """Removes the currently selected ingredient"""
        logging.debug('Remove ingredient')
        rows = sorted(set(index.row() for index in self.table_ingredients.selectedIndexes()))
        if rows:
            for row in rows:
                logging.info('Remove row #{}'.format(row))
                self.model_ingredients.remove_row(row)
            self._changed = True

    def _add_ingredient(self):
        """Adds a new ingredient"""
        logging.debug('Add ingredient')
        self.model_ingredients.add_row()
        self._update_headers(self.table_ingredients, len(self.recipe.ingredients))
        self._changed = True

    def _remove_step(self):
        """Removes the currently selected step"""
        logging.debug('Remove step')
        rows = sorted(set(index.row() for index in self.table_steps.selectedIndexes()))
        if rows:
            for row in rows:
                logging.info('Remove row #{}'.format(row))
                self.model_steps.remove_row(row)
            self._changed = True

    def _add_step(self):
        """Adds a new step"""
        logging.debug('Add step')
        self.model_steps.add_row()
        self._update_headers(self.table_steps, len(self.recipe.steps))
        self._changed = True

    def _remove_link(self):
        """Removes the currently selected link"""
        logging.debug('Remove link')
        rows = sorted(set(index.row() for index in self.table_links.selectedIndexes()))
        if rows:
            for row in rows:
                logging.info('Remove row #{}'.format(row))
                self.model_links.remove_row(row)
            self._changed = True

    def _add_link(self):
        """Adds a new link"""
        logging.debug('Add link')
        self.model_links.add_row()
        self._update_headers(self.table_links, len(self.recipe.links))
        self._changed = True

    def _on_ingredients_changed(self, lst):
        """On ingredients changed
        :param lst: Ingredients list
        """
        logging.debug('Ingredients changed')
        self._changed = True
        self.recipe.ingredients = lst

    def _on_steps_changed(self, lst):
        """On steps changed
        :param lst: Steps list
        """
        logging.debug('Steps changed')
        self._changed = True
        self.recipe.steps = lst

    def _on_links_changed(self, lst):
        """On links changed
        :param lst: Links list
        """
        logging.debug('Links changed')
        self._changed = True
        self.recipe.links = lst

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
            self.close_cb(self.path_info)

    def show_message(self, msg=''):
        """Shows a message in the status bar

        :param msg: The message to be displayed
        """
        self.statusBar().showMessage(msg)
