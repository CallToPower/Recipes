#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Denis Meyer
#
# This file is part of Rezepte.
#

"""Phase Ready widget"""

import logging
import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QSizePolicy, QWidget, QGridLayout, QLabel, QTreeWidget, QTreeWidgetItem, QProgressBar

from lib.Utils import load_json_recipe
from lib.AppConfig import app_conf_get

from gui.enums.Language import Language
from gui.components.RecipeWindow import RecipeWindow


class TreeViewUI(QWidget):
    """Tree View GUI"""

    def __init__(self, i18n, settings, log, image_cache):
        """Initializes the widget

        :param i18n: The I18n
        :param settings: The settings
        :param log: The (end user) message log
        :param image_cache: The image cache
        """
        super().__init__()

        logging.debug('Initializing TreeViewUI')

        self.i18n = i18n
        self.settings = settings
        self.log = log
        self.image_cache = image_cache
        
        self.recipe_suffix = app_conf_get('suffix.recipe', '.json')

        self.components = []
        self.recipe_windows = {}
        self.current_folder = self.settings.recipe_folder

    def init_ui(self):
        """Initiates application UI"""
        logging.debug('Initializing MainWidget GUI')

        self.font_label_header = QFont()
        self.font_label_header.setBold(True)
        self.font_label_header.setPointSize(app_conf_get('label.header.font.size', 20))

        self.font_label_info = QFont()
        self.font_label_info.setBold(False)
        self.font_label_info.setPointSize(app_conf_get('label.info.font.size', 16))

        self.line_css = 'background-color: #c0c0c0;'

        # Components

        self.label_header = QLabel(self.i18n.translate('GUI.TREEVIEW.HEADER'))
        self.label_header.setFont(self.font_label_header)
        self.label_header.setAlignment(Qt.AlignCenter)

        self.line_1 = QWidget()
        self.line_1.setFixedHeight(1)
        self.line_1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.line_1.setStyleSheet(self.line_css)

        self.line_2 = QWidget()
        self.line_2.setFixedHeight(1)
        self.line_2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.line_2.setStyleSheet(self.line_css)

        self.treewidget_dir = QTreeWidget()
        self.treewidget_dir.setHeaderHidden(True)
        #curr_folder = self._get_formatted_current_folder(show_slash=False)
        #self.treewidget_dir.setHeaderLabel(curr_folder)
        self.treewidget_dir.itemDoubleClicked.connect(self._on_item_double_clicked)
        self.components.append(self.treewidget_dir)
        
        self.progressbar = QProgressBar()
        self.progressbar.setTextVisible(False)

        self.label_current_folder = QLabel(self.i18n.translate('GUI.TREEVIEW.CURRENT_FOLDER').format(self.settings.recipe_folder))
        self.label_current_folder.setFont(self.font_label_info)
        self.label_current_folder.setAlignment(Qt.AlignLeft)

        # Layout

        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        # self.grid.addWidget(widget, row, column, rowspan, columnspan)

        curr_gridid = 0
        self.grid.addWidget(self.line_1, curr_gridid, 0, 1, 4)
        self.grid.addWidget(self.label_header, curr_gridid, 4, 1, 2)
        self.grid.addWidget(self.line_2, curr_gridid, 6, 1, 4)

        curr_gridid += 1
        self.grid.addWidget(self.treewidget_dir, curr_gridid, 0, 12, 10)
        
        curr_gridid += 12
        self.grid.addWidget(self.label_current_folder, curr_gridid, 0, 1, 10)

        curr_gridid += 1
        self.grid.addWidget(self.progressbar, curr_gridid, 0, 1, 10)

        self.setLayout(self.grid)
        self._refresh_view()
        self._reset_enabled()

    def _on_item_double_clicked(self, item, col):
        """When an item in the tree widget has been double-clicked
        :param item: The item
        :param col: The column
        """
        data = item.data(0, Qt.UserRole)
        path_info = data['path_info']
        folder = data['folder']
        startpath = data['startpath']
        filename = data['filename']
        if os.path.isfile(path_info) and path_info.endswith(self.recipe_suffix):
            logging.info('Double-clicked "{}", loading recipe'.format(path_info))
            json_recipe = load_json_recipe(path_info)
            if json_recipe:
                str_id = path_info
                if str_id in self.recipe_windows:
                    logging.debug('Recipe window already exists, activating')
                    self.recipe_windows[str_id].activateWindow()
                else:
                    logging.debug('Recipe window does not exist, creating new')
                    recipe_window = RecipeWindow(self.settings, self.i18n, str_id, json_recipe, self._recipe_window_closed)
                    self.recipe_windows[str_id] = recipe_window
                    recipe_window.init_ui()
                    recipe_window.show()
            else:
                logging.error('Could not load recipe "{}"'.format(path_info))
        else:
            logging.error('Does not appear to be a recipe: "{}"'.format(path_info))

    def _recipe_window_closed(self, id):
        """On recipe window close
        :param id: The ID of the window
        """
        logging.debug('Recipe window "{}" closed'.format(id))
        del self.recipe_windows[id]

    def _refresh_view(self):
        """Refreshes the view"""
        self.log(self.i18n.translate('GUI.TREEVIEW.LOG.LOAD_COOKBOOK.START'))
        logging.info('Loading cookbook')
        self._disable()
        self.progressbar.setValue(0)
        self.progressbar.setMinimum(0)
        self.progressbar.setMaximum(0)
        self.treewidget_dir.clear()
        self._load_project_structure(self.current_folder, self.treewidget_dir)
        self.progressbar.setMinimum(0)
        self.progressbar.setMaximum(100)
        self.progressbar.setValue(100)
        self.progressbar.reset()
        self._enable()
        self.log(self.i18n.translate('GUI.TREEVIEW.LOG.LOAD_COOKBOOK.DONE'))
        logging.info('Loaded cookbook')

    def _load_project_structure(self, startpath, tree):
        """
        Loads the project structure tree
        :param startpath: Start path 
        :param tree: Tree
        """
        for filename in os.listdir(startpath):
            path_info = os.path.join(startpath, filename)
            data = {
                'path_info': path_info,
                'startpath': startpath,
                'folder': os.path.basename(startpath),
                'filename': filename
            }
            if os.path.isdir(path_info):
                tw_item = QTreeWidgetItem(tree, [os.path.basename(filename)])
                icon = self.image_cache.get_or_load_icon('img.icon.folder-regular', 'folder-regular.svg', 'icons')
                self._load_project_structure(path_info, tw_item)
            else:
                if path_info.endswith(self.recipe_suffix):
                    tw_item = QTreeWidgetItem(tree, [os.path.basename(filename)[:-len(self.recipe_suffix)]])
                    icon = self.image_cache.get_or_load_icon('img.icon.file-solid', 'file-solid.svg', 'icons')
            tw_item.setData(0, Qt.UserRole, data)
            tw_item.setIcon(0, icon)

    def _get_formatted_current_folder(self, show_slash=False):
        """Returns the formatted current folder
        :param show_slash: Whether to show slash for recipe folder"""
        if show_slash and self.current_folder == self.settings.recipe_folder:
            return '/'
        return self.current_folder[len(self.settings.recipe_folder):]

    def reset(self):
        """Resets the widget"""
        logging.debug('Resetting widget')

        self.progressbar.reset()
        self._reset_enabled()

    def _reset_enabled(self):
        """Resets all component to initial state"""
        logging.debug('Resetting components to enabled state')

        self._enable()

    def _disable(self):
        """Resets all component to disabled state"""
        logging.debug('Disabling components')

        self.is_enabled = False
        for comp in self.components:
            comp.setEnabled(False)

    def _enable(self):
        """Resets all component to enabled state"""
        logging.debug('Enabling components')

        for comp in self.components:
            comp.setEnabled(True)
        self.is_enabled = True
