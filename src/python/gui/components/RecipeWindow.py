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
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QMenuBar, QAction, QInputDialog, QLineEdit, QLabel, QWidget, QSizePolicy, QGridLayout, QTableView, QHeaderView, QPushButton, QAbstractItemView, QMessageBox

from lib.Utils import is_macos
from i18n.I18n import I18n
from gui.components.IngredientsTableModel import IngredientsTableModel
from gui.components.StepsTableModel import StepsTableModel

from lib.AppConfig import app_conf_get
from lib.Utils import save_recipe

class RecipeWindow(QMainWindow):
    """Recipe window GUI"""

    def __init__(self, settings, i18n, image_cache, path_info, recipe, close_cb):
        """Initializes the recipe window

        :param settings: The settings
        :param i18n: The i18n
        :param image_cache: The image cache
        :param path_info: The path info
        :param recipe: The Recipe
        :param close_cb: Callback when the window closes
        """
        super().__init__()

        logging.debug('Initializing RecipeWindow')

        self.settings = settings
        self.i18n = i18n
        self.image_cache = image_cache
        self.path_info = path_info
        self.recipe = recipe
        self.close_cb = close_cb
        
        self._changed = False

    def init_ui(self):
        """Initiates UI"""
        logging.debug('Initializing RecipeWindow GUI')

        self._init_menu()

        if self.recipe.name:
            self.setWindowTitle(self.recipe.name)
        else:
            self.setWindowTitle(self.i18n.translate('GUI.RECIPE.VIEW.EMPTY_WINDOW_TITLE', 'Unknown Recipe'))
        self.statusbar = self.statusBar()
        if self.recipe.name:
            self.show_message(self.i18n.translate('GUI.RECIPE.LOG.RECIPE').format(self.recipe.name))

        self._init_widgets()

        self.resize(app_conf_get('window.recipe.width'), app_conf_get('window.recipe.height'))

        self._center()

    def _init_menu(self):
        """Initializes the menu bar"""
        logging.debug('Initializing the menu bar')

        self.menu_bar = QMenuBar() if is_macos() else self.menuBar()

        self.menu_bar.clear()

        menu_application = self.menu_bar.addMenu(self.i18n.translate('GUI.RECIPE.MENU.RECIPE.NAME', 'Recipe'))

        action_close = QAction(self.i18n.translate('GUI.RECIPE.MENU.ITEM.CLOSE', 'Close'), self)
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
        font_label_header.setPointSize(app_conf_get('label.header.font.size', 16))

        font_label_info = QFont()
        font_label_info.setBold(False)
        font_label_info.setPointSize(app_conf_get('label.info.font.size', 12))

        font_label_text = QFont()
        font_label_text.setBold(False)
        font_label_text.setPointSize(app_conf_get('label.text.font.size', 10))

        line_css = 'background-color: #c0c0c0;'
        bgcolor_header_css = 'background-color: rgb(230, 230, 230);'

        # Components

        self.label_header = QLabel(self.recipe.name)
        self.label_header.setFont(font_label_header)
        self.label_header.setAlignment(Qt.AlignCenter)

        button_edit_recipe_name = QPushButton()
        icon = self.image_cache.get_or_load_icon('img.icon.edit', 'pen-to-square-solid.svg', 'icons')
        button_edit_recipe_name.setIcon(icon)
        button_edit_recipe_name.clicked[bool].connect(self._edit_recipe_name)

        label_ingredients_line = QWidget()
        label_ingredients_line.setFixedHeight(1)
        label_ingredients_line.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        label_ingredients_line.setStyleSheet(line_css)

        label_ingredients = QLabel(self.i18n.translate('GUI.RECIPE.VIEW.HEADERS.INGREDIENTS', 'Ingredients'))
        label_ingredients.setFont(font_label_info)
        label_ingredients.setAlignment(Qt.AlignLeft)

        button_remove_ingredient = QPushButton(self.i18n.translate('GUI.RECIPE.VIEW.ACTIONS.INGREDIENTS.REMOVE', '-'))
        button_remove_ingredient.clicked[bool].connect(self._remove_ingredient)
        button_add_ingredient = QPushButton(self.i18n.translate('GUI.RECIPE.VIEW.ACTIONS.INGREDIENTS.ADD', '+'))
        button_add_ingredient.clicked[bool].connect(self._add_ingredient)

        self.table_ingredients = QTableView()
        self.table_ingredients.setStyleSheet('QHeaderView::section { ' + bgcolor_header_css + ' }')
        self.table_ingredients.setSelectionMode(QAbstractItemView.SingleSelection)
        self.model_ingredients = IngredientsTableModel(self.i18n, self.recipe.ingredients, cb_change=self._on_ingredients_changed)
        self.table_ingredients.setModel(self.model_ingredients)
        self.table_ingredients.resizeRowsToContents()
        self.table_ingredients.resizeColumnsToContents()
        self.table_ingredients.setWordWrap(True)
        self._update_headers(self.table_ingredients, self.model_ingredients, len(self.recipe.ingredients))
        self.table_ingredients.verticalHeader().setVisible(False)

        label_steps_line = QWidget()
        label_steps_line.setFixedHeight(1)
        label_steps_line.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        label_steps_line.setStyleSheet(line_css)

        label_steps = QLabel(self.i18n.translate('GUI.RECIPE.VIEW.HEADERS.STEPS', 'Steps'))
        label_steps.setFont(font_label_info)
        label_steps.setAlignment(Qt.AlignLeft)

        button_remove_step = QPushButton(self.i18n.translate('GUI.RECIPE.VIEW.ACTIONS.STEPS.REMOVE', '-'))
        button_remove_step.clicked[bool].connect(self._remove_step)
        button_add_step = QPushButton(self.i18n.translate('GUI.RECIPE.VIEW.ACTIONS.STEPS.ADD', '+'))
        button_add_step.clicked[bool].connect(self._add_step)

        self.table_steps = QTableView()
        self.table_steps.setStyleSheet('QHeaderView::section { ' + bgcolor_header_css + ' }')
        self.table_steps.setSelectionMode(QAbstractItemView.SingleSelection)
        self.model_steps = StepsTableModel(self.i18n, self.recipe.steps, cb_change=self._on_steps_changed)
        self.table_steps.setModel(self.model_steps)
        self.table_steps.resizeRowsToContents()
        self.table_steps.resizeColumnsToContents()
        self.table_steps.setWordWrap(True)
        self._update_headers(self.table_steps, self.model_steps, len(self.recipe.steps))
        self.table_steps.horizontalHeader().setVisible(False)

        label_info_line = QWidget()
        label_info_line.setFixedHeight(1)
        label_info_line.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        label_info_line.setStyleSheet(line_css)

        label_info = QLabel(self.i18n.translate('GUI.RECIPE.VIEW.HEADERS.INFO', 'Information'))
        label_info.setFont(font_label_info)
        label_info.setAlignment(Qt.AlignLeft)

        button_edit_info = QPushButton()
        icon = self.image_cache.get_or_load_icon('img.icon.edit', 'pen-to-square-solid.svg', 'icons')
        button_edit_info.setIcon(icon)
        button_edit_info.clicked[bool].connect(self._edit_info)

        self.label_info_text = QLabel(self._get_short(self.recipe.information))
        self.label_info_text.setFont(font_label_text)
        self.label_info_text.setAlignment(Qt.AlignLeft)

        button_cancel = QPushButton(self.i18n.translate('GUI.RECIPE.VIEW.ACTIONS.CANCEL', 'Cancel'))
        button_cancel.clicked[bool].connect(self._close)
        button_save = QPushButton(self.i18n.translate('GUI.RECIPE.VIEW.ACTIONS.SAVE', 'Save'))
        button_save.clicked[bool].connect(self._save)

        # Layout

        layout_grid = QGridLayout()
        layout_grid.setSpacing(10)

        # layout_grid.addWidget(widget, row, column, rowspan, columnspan)

        curr_gridid = 0
        layout_grid.setRowStretch(curr_gridid, 0)
        layout_grid.addWidget(self.label_header, curr_gridid, 0, 1, 9)
        layout_grid.addWidget(button_edit_recipe_name, curr_gridid, 9, 1, 1)

        curr_gridid += 1
        layout_grid.setRowStretch(curr_gridid, 0)
        layout_grid.addWidget(label_ingredients, curr_gridid, 0, 1, 1)
        layout_grid.addWidget(label_ingredients_line, curr_gridid, 1, 1, 7)
        layout_grid.addWidget(button_remove_ingredient, curr_gridid, 8, 1, 1)
        layout_grid.addWidget(button_add_ingredient, curr_gridid, 9, 1, 1)

        curr_gridid += 1
        layout_grid.setRowStretch(curr_gridid, 10)
        layout_grid.addWidget(self.table_ingredients, curr_gridid, 0, 10, 10)

        curr_gridid += 10
        layout_grid.setRowStretch(curr_gridid, 0)
        layout_grid.addWidget(label_steps, curr_gridid, 0, 1, 1)
        layout_grid.addWidget(label_steps_line, curr_gridid, 1, 1, 7)
        layout_grid.addWidget(button_remove_step, curr_gridid, 8, 1, 1)
        layout_grid.addWidget(button_add_step, curr_gridid, 9, 1, 1)

        curr_gridid += 1
        layout_grid.setRowStretch(curr_gridid, 10)
        layout_grid.addWidget(self.table_steps, curr_gridid, 0, 10, 10)

        curr_gridid += 10
        layout_grid.setRowStretch(curr_gridid, 0)
        layout_grid.addWidget(label_info, curr_gridid, 0, 1, 1)
        layout_grid.addWidget(label_info_line, curr_gridid, 1, 1, 8)
        layout_grid.addWidget(button_edit_info, curr_gridid, 9, 1, 1)

        curr_gridid += 1
        layout_grid.setRowStretch(curr_gridid, 0)
        layout_grid.addWidget(self.label_info_text, curr_gridid, 0, 1, 10)
        
        curr_gridid += 1
        layout_grid.addWidget(QLabel(''), curr_gridid, 0, 1, 10)

        curr_gridid += 1
        layout_grid.setRowStretch(curr_gridid, 0)
        layout_grid.addWidget(button_cancel, curr_gridid, 0, 1, 5)
        layout_grid.addWidget(button_save, curr_gridid, 5, 1, 5)

        widget.setLayout(layout_grid)

    def _edit_recipe_name(self):
        """Edits the recipe name"""
        name, ok = QInputDialog().getText(self, self.i18n.translate('GUI.RECIPE.VIEW.ACTIONS.EDIT_RECIPE_NAME'), self.i18n.translate('GUI.RECIPE.VIEW.ACTIONS.EDIT_RECIPE_NAME.TEXT'), QLineEdit.Normal, self.recipe.name)
        if ok and name:
            if name != self.recipe.name:
                self.recipe.name = name
                self.label_header.setText(self.recipe.name)
                self.setWindowTitle(self.recipe.name)
                self._changed = True
            else:
                logging.debug('Name did not change')

    def _update_headers(self, table, model, len_v):
        """Updates the headers
        :param table: The table
        :param model: The model
        :param len_v: Vertical header length
        """
        header_v = table.verticalHeader()
        if header_v:
            for i in range(0, len_v):
                header_v.setSectionResizeMode(i, QHeaderView.ResizeToContents)

        header_h = table.horizontalHeader()
        if header_h:
            for i in range(0, max(0, len(model._headers_h))):
                header_h.setSectionResizeMode(i, QHeaderView.ResizeToContents)
            header_h.setSectionResizeMode(max(0, len(model._headers_h) - 1), QHeaderView.Stretch)

    def _close_yesno(self):
        """Displays a message box with yes/no
        :return: True if yes, False else
        """
        msg = self.i18n.translate('GUI.RECIPE.MESSAGE_BOX.CLOSE.TEXT')
        title = self.i18n.translate('GUI.RECIPE.MESSAGE_BOX.CLOSE')
        message_box = QMessageBox(QMessageBox.Information, title, msg, buttons=QMessageBox.Yes | QMessageBox.No)
        message_box.exec_()

        return message_box.standardButton(message_box.clickedButton()) == QMessageBox.Yes

    def _cancel(self, event=None):
        """Cancels the change"""
        logging.debug('Cancel')
        if not self._changed:
            logging.info('Nothing changed, closing')
            if event:
                event.accept()
            self._close()
        else:
            logging.info('Something changed, asking whether to close')
            if self._close_yesno():
                logging.info('Closing without saving')
                if event:
                    event.accept()
                self._close()
            else:
                logging.info('Not closing without saving')
                if event:
                    event.ignore()

    def _save(self):
        """Saves the change"""
        logging.debug('Save')
        if not self._changed:
            logging.info('Nothing changed')
            self._close()
            return
        logging.info('Saving recipe to "{}"'.format(self.path_info))
        if save_recipe(self.recipe, self.path_info):
            self._changed = False
            self._close()

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
        self._update_headers(self.table_ingredients, self.model_ingredients, len(self.recipe.ingredients))
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
        self._update_headers(self.table_steps, self.model_steps, len(self.recipe.steps))
        self._changed = True

    def _edit_info(self):
        """Edits information"""
        logging.debug('Edit information')
        info, ok = QInputDialog().getText(self, self.i18n.translate('GUI.RECIPE.VIEW.ACTIONS.EDIT_INFORMATION'), self.i18n.translate('GUI.RECIPE.VIEW.ACTIONS.EDIT_INFORMATION.TEXT'), QLineEdit.Normal, self.recipe.information)
        if ok and info:
            if info != self.recipe.information:
                self.recipe.information = info
                self.label_info_text.setText(self._get_short(self.recipe.information))
                self.setWindowTitle(self.recipe.information)
                self._changed = True
            else:
                logging.debug('Information did not change')

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

    def _on_information_changed(self, info):
        """On information changed
        :param info: Information string
        """
        logging.debug('Information changed')
        self._changed = True
        self.recipe.information = info

    def _center(self):
        """Centers the window on the screen"""
        screen = QDesktopWidget().screenGeometry()
        self.move(int((screen.width() - self.geometry().width()) / 2),
                  int((screen.height() - self.geometry().height()) / 2))

    def _get_short(self, str, max_length=app_conf_get('info.length.max', 80)):
        """Returns a shortened string
        :param str: String to shorten
        :param max_length: Max string length
        """
        info = self.recipe.information
        if len(info) > max_length:
            return info[:(max_length - 3)] + '...'
        return info

    def _close(self):
        """Close window"""
        logging.debug('Closing window')
        if self.close_cb:
            self.close_cb(self.path_info)
        self.close()

    # @override
    def closeEvent(self, event):
        """Window close event
        
        :param event: The event
        """
        logging.debug('Window close triggered')
        self._cancel(event)

    def show_message(self, msg=''):
        """Shows a message in the status bar

        :param msg: The message to be displayed
        """
        self.statusBar().showMessage(msg)
