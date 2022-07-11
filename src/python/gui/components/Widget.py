#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Denis Meyer
#
# This file is part of Rezepte.
#

"""Widget"""

import logging
import os
import shutil

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QAbstractItemView, QMenu, QAction, QSizePolicy, QWidget, QGridLayout, QLabel, QTreeWidgetItem, QProgressBar, QPushButton, QMessageBox, QInputDialog, QLineEdit, QFileDialog, QDialog

from gui.components.TreeWidget import TreeWidget
from lib.Utils import load_json_recipe
from lib.AppConfig import app_conf_get

from classes.Recipe import Recipe
from gui.enums.Language import Language
from gui.components.RecipeWindow import RecipeWindow
from lib.Utils import save_recipe


class Widget(QWidget):
    """Widget"""

    def __init__(self, i18n, settings, log, image_cache):
        """Initializes the widget

        :param i18n: The I18n
        :param settings: The settings
        :param log: The (end user) message log
        :param image_cache: The image cache
        """
        super().__init__()

        logging.debug('Initializing Widget')

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

        _font_label_header = QFont()
        _font_label_header.setBold(True)
        _font_label_header.setPointSize(app_conf_get('label.header.font.size', 16))

        _font_label_info = QFont()
        _font_label_info.setBold(False)
        _font_label_info.setPointSize(app_conf_get('label.info.font.size', 12))

        _font_label_text = QFont()
        _font_label_text.setBold(False)
        _font_label_text.setPointSize(app_conf_get('label.text.font.size', 10))

        _line_css = 'background-color: #c0c0c0;'

        # Components

        _line_1 = QWidget()
        _line_1.setFixedHeight(1)
        _line_1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        _line_1.setStyleSheet(_line_css)

        _label_header = QLabel(self.i18n.translate('GUI.TREEVIEW.HEADER'))
        _label_header.setFont(_font_label_header)
        _label_header.setAlignment(Qt.AlignCenter)

        _line_2 = QWidget()
        _line_2.setFixedHeight(1)
        _line_2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        _line_2.setStyleSheet(_line_css)

        _button_delete = QPushButton()
        icon = self.image_cache.get_or_load_icon('img.icon.delete', 'minus-solid.svg', 'icons')
        _button_delete.setIcon(icon)
        _button_delete.clicked[bool].connect(self._delete)

        _button_edit = QPushButton()
        icon = self.image_cache.get_or_load_icon('img.icon.edit', 'pen-to-square-solid.svg', 'icons')
        _button_edit.setIcon(icon)
        _button_edit.clicked[bool].connect(self._edit)

        _button_move = QPushButton()
        icon = self.image_cache.get_or_load_icon('img.icon.move', 'arrow-right-arrow-left-solid.svg', 'icons')
        _button_move.setIcon(icon)
        _button_move.clicked[bool].connect(self._move)

        _button_create_folder = QPushButton()
        icon = self.image_cache.get_or_load_icon('img.icon.create_folder', 'folder-plus-solid.svg', 'icons')
        _button_create_folder.setIcon(icon)
        _button_create_folder.clicked[bool].connect(self._create_folder)

        _button_create_recipe = QPushButton()
        icon = self.image_cache.get_or_load_icon('img.icon.create_recipe', 'plus-solid.svg', 'icons')
        _button_create_recipe.setIcon(icon)
        _button_create_recipe.clicked[bool].connect(self._create_recipe)

        self._treewidget = TreeWidget(self._dropped)
        self._treewidget.setHeaderHidden(True)
        self._treewidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self._treewidget.customContextMenuRequested.connect(self._open_menu)
        self._treewidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self._treewidget.setDragEnabled(True)
        self._treewidget.setAcceptDrops(True)
        self._treewidget.setDropIndicatorShown(True)

        #curr_folder = self._get_formatted_current_folder(show_slash=False)
        #self._treewidget.setHeaderLabel(curr_folder)
        self._treewidget.itemDoubleClicked.connect(self._on_item_double_clicked)
        self.components.append(self._treewidget)
        
        self.progressbar = QProgressBar()
        self.progressbar.setTextVisible(False)

        _label_current_folder = QLabel(self.i18n.translate('GUI.TREEVIEW.CURRENT_FOLDER').format(self.settings.recipe_folder))
        _label_current_folder.setFont(_font_label_text)
        _label_current_folder.setAlignment(Qt.AlignLeft)

        # Layout

        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        # self.grid.addWidget(widget, row, column, rowspan, columnspan)

        curr_gridid = 0
        self.grid.addWidget(_line_1, curr_gridid, 0, 1, 3)
        self.grid.addWidget(_label_header, curr_gridid, 3, 1, 1)
        self.grid.addWidget(_line_2, curr_gridid, 4, 1, 1)
        self.grid.addWidget(_button_delete, curr_gridid, 5, 1, 1)
        self.grid.addWidget(_button_edit, curr_gridid, 6, 1, 1)
        self.grid.addWidget(_button_move, curr_gridid, 7, 1, 1)
        self.grid.addWidget(_button_create_folder, curr_gridid, 8, 1, 1)
        self.grid.addWidget(_button_create_recipe, curr_gridid, 9, 1, 1)

        curr_gridid += 1
        self.grid.addWidget(self._treewidget, curr_gridid, 0, 12, 10)
        
        curr_gridid += 12
        self.grid.addWidget(_label_current_folder, curr_gridid, 0, 1, 10)

        curr_gridid += 1
        self.grid.addWidget(self.progressbar, curr_gridid, 0, 1, 10)

        self.setLayout(self.grid)
        self._refresh_view()
        self._enable()

    def _open_menu(self, position):
        indexes = self._treewidget.selectedIndexes()

        menu = QMenu()

        action_delete = QAction(self.i18n.translate('GUI.TREEVIEW.MENU.RIGHTCLICK.DELETE', 'Delete'), self)
        action_delete.triggered.connect(self._delete)
        icon = self.image_cache.get_or_load_icon('img.icon.delete', 'minus-solid.svg', 'icons')
        action_delete.setIcon(icon)
        action_edit = QAction(self.i18n.translate('GUI.TREEVIEW.MENU.RIGHTCLICK.EDIT', 'Edit'), self)
        action_edit.triggered.connect(self._edit)
        icon = self.image_cache.get_or_load_icon('img.icon.edit', 'pen-to-square-solid.svg', 'icons')
        action_edit.setIcon(icon)
        action_move = QAction(self.i18n.translate('GUI.TREEVIEW.MENU.RIGHTCLICK.MOVE', 'Move'), self)
        action_move.triggered.connect(self._move)
        icon = self.image_cache.get_or_load_icon('img.icon.move', 'arrow-right-arrow-left-solid.svg', 'icons')
        action_move.setIcon(icon)
        action_create_folder = QAction(self.i18n.translate('GUI.TREEVIEW.MENU.RIGHTCLICK.CREATE_FOLDER', 'Create Folder'), self)
        action_create_folder.triggered.connect(self._create_folder)
        icon = self.image_cache.get_or_load_icon('img.icon.create_folder', 'folder-plus-solid.svg', 'icons')
        action_create_folder.setIcon(icon)
        action_create_file = QAction(self.i18n.translate('GUI.TREEVIEW.MENU.RIGHTCLICK.CREATE_FILE', 'Create Recipe'), self)
        action_create_file.triggered.connect(self._create_recipe)
        icon = self.image_cache.get_or_load_icon('img.icon.create_recipe', 'plus-solid.svg', 'icons')
        action_create_file.setIcon(icon)

        menu.addAction(action_delete)
        menu.addAction(action_edit)
        menu.addAction(action_move)
        menu.addAction(action_create_folder)
        menu.addAction(action_create_file)

        menu.exec_(self._treewidget.viewport().mapToGlobal(position))

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

    def _get_file_name(self, filename, is_file=False):
        """Asks for a new name
        :param is_file: Flag whether is a file or a folder
        """
        name, ok = QInputDialog().getText(self, self.i18n.translate('GUI.TREEVIEW.ACTIONS.{}'.format('EDIT_FILE' if is_file else 'EDIT_FOLDER')), self.i18n.translate('GUI.TREEVIEW.ACTIONS.{}.TEXT'.format('EDIT_FILE' if is_file else 'EDIT_FOLDER')), QLineEdit.Normal, filename)
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

    def _dropped(self, source, destination):
        """On event dropped
        :param source: Source item
        :param destination: Destination item (may be None)
        """
        if destination:
            destination_path_info = destination['path_info']
        else:
            destination_path_info = self.settings.recipe_folder
        if os.path.isdir(destination_path_info):
            destination_folder = destination_path_info
        else:
            destination_folder = os.path.dirname(destination_path_info)

        is_dir = False
        source_path_info = source['path_info']
        if os.path.isfile(source_path_info) and source_path_info.endswith(self.recipe_suffix):
            source_folder = os.path.dirname(source_path_info)
        elif os.path.isdir(source_path_info):
            is_dir = True
            source_folder = source_path_info

        moved = False

        if source_folder and destination_folder:
            is_subfolder_of = False
            if is_dir:
                is_subfolder_of = destination_folder.startswith(source_folder)
            if source_folder != destination_folder and not is_subfolder_of:
                logging.debug('Move "{}" to "{}"'.format(source_path_info, destination_folder))
                try:
                    shutil.move(source_path_info, destination_folder)
                    self.log(self.i18n.translate('GUI.TREEVIEW.LOG.MOVE_{}'.format('DIRECTORY' if is_dir else 'FILE')).format(os.path.basename(source_path_info), os.path.basename(destination_folder)))
                    moved = True
                except Exception as e:
                    self.log(self.i18n.translate('GUI.TREEVIEW.LOG.MOVE_{}.FAIL'.format('DIRECTORY' if is_dir else 'FILE')).format(os.path.basename(dirname), os.path.basename(destination_folder)))
                    logging.error('Failed to move "{}" to "{}": {}'.format(source_path_info, destination_folder, e))
            else:
                logging.info('Same folder, not moving')

        if moved:
            logging.debug('Refreshing view')
            self._refresh_view(do_log=False)
            self._enable()

    def _delete(self):
        """Deletes the selected folder/file"""
        curr_item = self._treewidget.currentItem()
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
                        self.log(self.i18n.translate('GUI.TREEVIEW.LOG.DELETE_DIRECTORY').format(filename))
                        deleted = True
                    except Exception as e:
                        self.log(self.i18n.translate('GUI.TREEVIEW.LOG.DELETE_DIRECTORY.FAIL').format(filename))
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

    def _edit(self):
        """Edits the selected folder/file"""
        curr_item = self._treewidget.currentItem()
        if curr_item:
            data = curr_item.data(0, Qt.UserRole)
            path_info = data['path_info']
            folder = data['folder']
            filename = data['filename']
            edited = False
            logging.info('Move "{}"'.format(path_info))
            if os.path.isdir(path_info):
                name, ok = self._get_file_name(filename, is_file=False)
                if ok:
                    dirname = os.path.dirname(path_info)
                    new_path = os.path.join(dirname, name)
                    logging.info('Moving "{}" to "{}"'.format(path_info, new_path))
                    try:
                        shutil.move(path_info, new_path)
                        self.log(self.i18n.translate('GUI.TREEVIEW.LOG.EDIT_FOLDER.SUCCESS').format(filename, name))
                        edited = True
                    except Exception as e:
                        self.log(self.i18n.translate('GUI.TREEVIEW.LOG.EDIT_FOLDER.FAIL').format(filename, new_path))
                        logging.error('Failed to edit directory "{}" to "{}": {}'.format(filename, new_path, e))
            elif os.path.isfile(path_info) and path_info.endswith(self.recipe_suffix):
                _filename = filename[:-len(self.recipe_suffix)]
                name, ok = self._get_file_name(_filename, is_file=False)
                if ok:
                    dirname = os.path.dirname(path_info)
                    _name = '{}{}'.format(name, self.recipe_suffix)
                    new_path = os.path.join(dirname, _name)
                    logging.info('Moving "{}" to "{}"'.format(path_info, new_path))
                    try:
                        shutil.move(path_info, new_path)
                        self.log(self.i18n.translate('GUI.TREEVIEW.LOG.EDIT_FILE.SUCCESS').format(_filename, name))
                        edited = True
                    except Exception as e:
                        self.log(self.i18n.translate('GUI.TREEVIEW.LOG.EDIT_FILE.FAIL').format(_filename, name))
                        logging.error('Failed to edit file "{}" to "{}": {}'.format(_filename, name, e))
            if edited:
                logging.debug('Refreshing view')
                self._refresh_view(do_log=False)
                self._enable()
        else:
            logging.debug('No item selected')

    def _move(self):
        """Moves the selected file"""
        curr_item = self._treewidget.currentItem()
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
                        self.log(self.i18n.translate('GUI.TREEVIEW.LOG.MOVE_DIRECTORY').format(os.path.basename(dirname), os.path.basename(selected_folder)))
                        moved = True
                    except Exception as e:
                        self.log(self.i18n.translate('GUI.TREEVIEW.LOG.MOVE_DIRECTORY.FAIL').format(os.path.basename(dirname), os.path.basename(selected_folder)))
                        logging.error('Failed to move directory "{}" to "{}": {}'.format(dirname, selected_folder, e))
            elif os.path.isfile(path_info):
                dirname = os.path.dirname(path_info)
                logging.info('Move file "{}"'.format(path_info))
                selected_folder, is_selected = self._select_folder(dirname)
                if is_selected and dirname != selected_folder:
                    logging.info('Moving file "{}"'.format(selected_folder))
                    try:
                        shutil.move(path_info, selected_folder)
                        self.log(self.i18n.translate('GUI.TREEVIEW.LOG.MOVE_FILE').format(os.path.basename(dirname), os.path.basename(selected_folder)))
                        moved = True
                    except Exception as e:
                        self.log(self.i18n.translate('GUI.TREEVIEW.LOG.MOVE_FILE.FAIL').format(os.path.basename(dirname), os.path.basename(selected_folder)))
                        logging.error('Failed to move file "{}" to "{}": {}'.format(dirname, selected_folder, e))
            if moved:
                logging.debug('Refreshing view')
                self._refresh_view(do_log=False)
                self._enable()

    def _create_folder(self):
        """Creates a new folder"""
        curr_item = self._treewidget.currentItem()
        if curr_item:
            data = curr_item.data(0, Qt.UserRole)
            path_info = data['path_info']
        else:
            path_info = self.current_folder
        dirname = path_info
        if os.path.isfile(path_info):
            dirname = os.path.dirname(path_info)
        foldername, ok = self._get_new_file_name(is_file=False)
        if ok and foldername:
            folder = os.path.join(dirname, foldername)
            if not os.path.exists(folder):
                logging.info('Creating folder "{}"'.format(folder))
                os.makedirs(folder)
                self.log(self.i18n.translate('GUI.TREEVIEW.LOG.CREATE_FOLDER.SUCCESS').format(foldername))
                logging.debug('Refreshing view')
                self._refresh_view(do_log=False)
                self._enable()
            else:
                self.log(self.i18n.translate('GUI.TREEVIEW.LOG.CREATE_FOLDER.FAIL.EXISTS').format(foldername))
                logging.error('Folder "{}" already exists'.format(folder))

    def _create_recipe(self):
        """Creates a new recipe"""
        curr_item = self._treewidget.currentItem()
        if curr_item:
            data = curr_item.data(0, Qt.UserRole)
            path_info = data['path_info']
        else:
            path_info = self.current_folder
        dirname = path_info
        if os.path.isfile(path_info):
            dirname = os.path.dirname(path_info)
        filename, ok = self._get_new_file_name(is_file=True)
        if ok and filename:
            file = os.path.join(dirname, filename)
            if not file.endswith(self.recipe_suffix):
                file = file + self.recipe_suffix
            if not os.path.exists(file):
                logging.info('Creating file "{}"'.format(file))
                recipe = Recipe()
                if save_recipe(recipe, file):
                    self.log(self.i18n.translate('GUI.TREEVIEW.LOG.CREATE_FILE.SUCCESS').format(filename))
                    logging.debug('Refreshing view')
                    self._refresh_view(do_log=False)
                    self._enable()
                else:
                    logging.error('Could not create file "{}"'.format(file))
            else:
                self.log(self.i18n.translate('GUI.TREEVIEW.LOG.CREATE_FOLDER.FAIL.EXISTS').format(filename))
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
        if id in self.recipe_windows:
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
        self._treewidget.clear()
        self._load_project_structure(self.current_folder, self._treewidget)
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

        model = self._treewidget.model()
        for row in range(model.rowCount()):
            index = model.index(row, 0)
            self._treewidget.expand(index)

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
