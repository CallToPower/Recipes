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
import shutil

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QMenu, QAction, QSizePolicy, QWidget, QGridLayout, QLabel, QTreeWidget, QTreeWidgetItem, QProgressBar, QPushButton, QMessageBox, QInputDialog, QLineEdit, QFileDialog, QDialog

from lib.Utils import load_json_recipe
from lib.AppConfig import app_conf_get

from classes.Recipe import Recipe
from gui.enums.Language import Language
from gui.components.RecipeWindow import RecipeWindow
from lib.Utils import save_recipe


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

        self.line_1 = QWidget()
        self.line_1.setFixedHeight(1)
        self.line_1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.line_1.setStyleSheet(self.line_css)

        self.label_header = QLabel(self.i18n.translate('GUI.TREEVIEW.HEADER'))
        self.label_header.setFont(self.font_label_header)
        self.label_header.setAlignment(Qt.AlignCenter)

        self.line_2 = QWidget()
        self.line_2.setFixedHeight(1)
        self.line_2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.line_2.setStyleSheet(self.line_css)

        self.button_delete = QPushButton()
        icon = self.image_cache.get_or_load_icon('img.icon.delete', 'minus-solid.svg', 'icons')
        self.button_delete.setIcon(icon)
        self.button_delete.clicked[bool].connect(self._delete)

        self.button_move = QPushButton()
        icon = self.image_cache.get_or_load_icon('img.icon.move', 'arrow-right-arrow-left-solid.svg', 'icons')
        self.button_move.setIcon(icon)
        self.button_move.clicked[bool].connect(self._move)

        self.button_create_folder = QPushButton()
        icon = self.image_cache.get_or_load_icon('img.icon.create_folder', 'folder-plus-solid.svg', 'icons')
        self.button_create_folder.setIcon(icon)
        self.button_create_folder.clicked[bool].connect(self._create_folder)

        self.button_create_recipe = QPushButton()
        icon = self.image_cache.get_or_load_icon('img.icon.create_recipe', 'plus-solid.svg', 'icons')
        self.button_create_recipe.setIcon(icon)
        self.button_create_recipe.clicked[bool].connect(self._create_recipe)

        self.treewidget_dir = QTreeWidget()
        self.treewidget_dir.setHeaderHidden(True)
        self.treewidget_dir.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treewidget_dir.customContextMenuRequested.connect(self._open_menu)
        # self.treewidget_dir.setSelectionMode(QAbstractItemView.SingleSelection)
        #self.treewidget_dir.setDragEnabled(True)
        #self.treewidget_dir.setAcceptDrops(True)
        #self.treewidget_dir.setDropIndicatorShown(True)

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
        self.grid.addWidget(self.line_1, curr_gridid, 0, 1, 3)
        self.grid.addWidget(self.label_header, curr_gridid, 3, 1, 2)
        self.grid.addWidget(self.line_2, curr_gridid, 5, 1, 1)
        self.grid.addWidget(self.button_delete, curr_gridid, 6, 1, 1)
        self.grid.addWidget(self.button_move, curr_gridid, 7, 1, 1)
        self.grid.addWidget(self.button_create_folder, curr_gridid, 8, 1, 1)
        self.grid.addWidget(self.button_create_recipe, curr_gridid, 9, 1, 1)

        curr_gridid += 1
        self.grid.addWidget(self.treewidget_dir, curr_gridid, 0, 12, 10)
        
        curr_gridid += 12
        self.grid.addWidget(self.label_current_folder, curr_gridid, 0, 1, 10)

        curr_gridid += 1
        self.grid.addWidget(self.progressbar, curr_gridid, 0, 1, 10)

        self.setLayout(self.grid)
        self._refresh_view()
        self._enable()

    def _open_menu(self, position):
        indexes = self.treewidget_dir.selectedIndexes()

        menu = QMenu()

        action_delete = QAction('Delete', self)
        action_delete.triggered.connect(self._delete)
        icon = self.image_cache.get_or_load_icon('img.icon.delete', 'minus-solid.svg', 'icons')
        action_delete.setIcon(icon)
        action_move = QAction('Move', self)
        action_move.triggered.connect(self._move)
        icon = self.image_cache.get_or_load_icon('img.icon.move', 'arrow-right-arrow-left-solid.svg', 'icons')
        action_move.setIcon(icon)
        action_create_folder = QAction('Create Folder', self)
        action_create_folder.triggered.connect(self._create_folder)
        icon = self.image_cache.get_or_load_icon('img.icon.create_folder', 'folder-plus-solid.svg', 'icons')
        action_create_folder.setIcon(icon)
        action_create_file = QAction('Create Recipe', self)
        action_create_file.triggered.connect(self._create_recipe)
        icon = self.image_cache.get_or_load_icon('img.icon.create_recipe', 'plus-solid.svg', 'icons')
        action_create_file.setIcon(icon)

        menu.addAction(action_delete)
        menu.addAction(action_move)
        menu.addAction(action_create_folder)
        menu.addAction(action_create_file)

        menu.exec_(self.treewidget_dir.viewport().mapToGlobal(position))

    def _messagebox_delete_yesno(self, is_file, name):
        """Displays a message box with yes/no
        :param is_file: Flag whether is a file or a folder
        :param name: The file/folder name
        :return: True if yes, False else
        """
        msg = self.i18n.translate('GUI.TREEVIEW.MESSAGE_BOX.DELETE.{}'.format('FILE' if is_file else 'DIRECTORY')).format(name)
        title = self.i18n.translate('GUI.TREEVIEW.MESSAGE_BOX.DELETE')
        message_box = QMessageBox(QMessageBox.Information, title, msg, buttons=QMessageBox.Yes | QMessageBox.No)
        message_box.exec_()

        return message_box.standardButton(message_box.clickedButton()) == QMessageBox.Yes

    def _get_new_file_name(self, is_file=False):
        """Asks for a new folder name
        :param is_file: Flag whether is a file or a folder
        """
        name, ok = QInputDialog().getText(self, self.i18n.translate('GUI.TREEVIEW.ACTIONS.{}'.format('NEW_FILE' if is_file else 'NEW_FOLDER')), self.i18n.translate('GUI.TREEVIEW.ACTIONS.{}.TEXT'.format('NEW_FILE' if is_file else 'NEW_FOLDER')), QLineEdit.Normal, '')
        return name, ok

    def _select_folder(self, directory):
        """Select folder dialog
        :param directory: The directory
        """
        filter = None
        dialog = QFileDialog(self, self.i18n.translate('GUI.TREEVIEW.MESSAGE_BOX.SELECT_FOLDER'), directory, filter)
        dialog.setFileMode(QFileDialog.DirectoryOnly)
        if dialog.exec_() == QDialog.Accepted:
            return dialog.selectedFiles()[0], True
        else:
            return '', False

    def _delete(self):
        """Deletes the selected folder/file"""
        curr_item = self.treewidget_dir.currentItem()
        if curr_item:
            data = curr_item.data(0, Qt.UserRole)
            path_info = data['path_info']
            folder = data['folder']
            filename = data['filename']
            deleted = False
            if os.path.isdir(path_info):
                logging.info('Delete folder "{}"'.format(path_info))
                if self._messagebox_delete_yesno(False, filename):
                    try:
                        shutil.rmtree(path_info)
                        self.log(self.i18n.translate('GUI.TREEVIEW.LOG.DELETE_DIRECTORY').format(folder))
                        deleted = True
                    except Exception as e:
                        self.log(self.i18n.translate('GUI.TREEVIEW.LOG.DELETE_DIRECTORY.FAIL').format(folder))
                        logging.error('Failed to remove directory "{}": {}'.format(path_info, e))
            elif os.path.isfile(path_info) and path_info.endswith(self.recipe_suffix):
                logging.info('Delete file "{}"'.format(path_info))
                _filename = filename[:-len(self.recipe_suffix)]
                if self._messagebox_delete_yesno(True, _filename):
                    try:
                        os.remove(path_info)
                        self.log(self.i18n.translate('GUI.TREEVIEW.LOG.DELETE_FILE').format(_filename))
                        deleted = True
                    except Exception as e:
                        self.log(self.i18n.translate('GUI.TREEVIEW.LOG.DELETE_FILE.FAIL').format(_filename))
                        logging.error('Failed to remove directory "{}": {}'.format(path_info, e))
            if deleted:
                logging.debug('Refreshing view')
                self._refresh_view(do_log=False)
                self._enable()
        else:
            logging.debug('No item selected')

    def _move(self):
        """Moves the selected file"""
        curr_item = self.treewidget_dir.currentItem()
        if curr_item:
            data = curr_item.data(0, Qt.UserRole)
            path_info = data['path_info']
            folder = data['folder']
            moved = False
            if os.path.isdir(path_info):
                dirname = path_info
                logging.info('Move folder "{}"'.format(dirname))
                selected_folder, is_selected = self._select_folder(dirname)
                if is_selected and dirname != selected_folder:
                    logging.info('Moving folder "{}"'.format(selected_folder))
                    try:
                        shutil.move(dirname, selected_folder)
                        self.log(self.i18n.translate('GUI.TREEVIEW.LOG.MOVE_DIRECTORY').format(dirname, selected_folder))
                        moved = True
                    except Exception as e:
                        self.log(self.i18n.translate('GUI.TREEVIEW.LOG.MOVE_DIRECTORY.FAIL').format(dirname, selected_folder))
                        logging.error('Failed to move directory "{}" to "{}": {}'.format(dirname, selected_folder, e))
            elif os.path.isfile(path_info):
                dirname = os.path.dirname(path_info)
                logging.info('Move file "{}"'.format(path_info))
                selected_folder, is_selected = self._select_folder(dirname)
                if is_selected and dirname != selected_folder:
                    logging.info('Moving file "{}"'.format(selected_folder))
                    try:
                        shutil.move(path_info, selected_folder)
                        self.log(self.i18n.translate('GUI.TREEVIEW.LOG.MOVE_FILE').format(dirname, selected_folder))
                        moved = True
                    except Exception as e:
                        self.log(self.i18n.translate('GUI.TREEVIEW.LOG.MOVE_FILE.FAIL').format(dirname, selected_folder))
                        logging.error('Failed to move file "{}" to "{}": {}'.format(dirname, selected_folder, e))
            if moved:
                logging.debug('Refreshing view')
                self._refresh_view(do_log=False)
                self._enable()

    def _create_folder(self):
        """Creates a new folder"""
        curr_item = self.treewidget_dir.currentItem()
        if curr_item:
            data = curr_item.data(0, Qt.UserRole)
            path_info = data['path_info']
        else:
            path_info = self.current_folder
        dirname = path_info
        if os.path.isfile(path_info):
            dirname = os.path.dirname(path_info)
        foldername, ok = self._get_new_file_name(is_file=False)
        if ok:
            folder = os.path.join(dirname, foldername)
            if not os.path.exists(folder):
                logging.info('Creating folder "{}"'.format(folder))
                os.makedirs(folder)
                self.log(self.i18n.translate('GUI.TREEVIEW.LOG.CREATE_FOLDER.SUCCESS').format(folder))
                logging.debug('Refreshing view')
                self._refresh_view(do_log=False)
                self._enable()
            else:
                self.log(self.i18n.translate('GUI.TREEVIEW.LOG.CREATE_FOLDER.FAIL.EXISTS').format(folder))
                logging.error('Folder "{}" already exists'.format(folder))

    def _create_recipe(self):
        """Creates a new recipe"""
        curr_item = self.treewidget_dir.currentItem()
        if curr_item:
            data = curr_item.data(0, Qt.UserRole)
            path_info = data['path_info']
        else:
            path_info = self.current_folder
        dirname = path_info
        if os.path.isfile(path_info):
            dirname = os.path.dirname(path_info)
        filename, ok = self._get_new_file_name(is_file=True)
        if ok:
            file = os.path.join(dirname, filename)
            if not file.endswith(self.recipe_suffix):
                file = file + self.recipe_suffix
            if not os.path.exists(file):
                logging.info('Creating file "{}"'.format(file))
                recipe = Recipe()
                if save_recipe(recipe, file):
                    self.log(self.i18n.translate('GUI.TREEVIEW.LOG.CREATE_FILE.SUCCESS').format(file))
                    logging.debug('Refreshing view')
                    self._refresh_view(do_log=False)
                    self._enable()
                else:
                    logging.error('Could not create file "{}"'.format(file))
            else:
                self.log(self.i18n.translate('GUI.TREEVIEW.LOG.CREATE_FOLDER.FAIL.EXISTS').format(folder))
                logging.error('Folder "{}" already exists'.format(folder))

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
                if path_info in self.recipe_windows:
                    logging.debug('Recipe window already exists, activating')
                    self.recipe_windows[path_info].activateWindow()
                else:
                    logging.debug('Recipe window does not exist, creating new')
                    recipe_window = RecipeWindow(self.settings, self.i18n, self.image_cache, path_info, json_recipe, self._recipe_window_closed)
                    self.recipe_windows[path_info] = recipe_window
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

    def _refresh_view(self, do_log=True):
        """Refreshes the view"""
        if do_log:
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
        if do_log:
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
