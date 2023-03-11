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
from PyQt5.QtCore import QCoreApplication, QUrl
from PyQt5.QtGui import QFont, QDesktopServices, QIcon
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QMenuBar, QAction, QFileDialog, QInputDialog, QLineEdit, QLabel, QWidget, QSizePolicy, QGridLayout, QHeaderView, QPushButton, QAbstractItemView, QMessageBox

from fpdf import FPDF

from lib.Utils import is_macos
from i18n.I18n import I18n
from gui.data.IconDefinitions import EDIT, QUIT
from gui.components.view.IngredientsTableView import IngredientsTableView
from gui.components.view.StepsTableView import StepsTableView
from gui.components.model.IngredientsTableModel import IngredientsTableModel
from gui.components.model.StepsTableModel import StepsTableModel

from lib.AppConfig import app_conf_get
from lib.Utils import save_recipe
from lib.RecipePDF import RecipePDF

class RecipeWindow(QMainWindow):
    """Recipe window GUI"""

    def __init__(self, i18n, image_cache, path_info, recipe, close_cb):
        """Initializes the recipe window

        :param i18n: The i18n
        :param image_cache: The image cache
        :param path_info: The path info
        :param recipe: The Recipe
        :param close_cb: Callback when the window closes
        """
        super().__init__()

        logging.debug('Initializing RecipeWindow')

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
            self.show_message(self.i18n.translate('GUI.RECIPE.LOG.RECIPE.OPENED').format(self.recipe.name))

        logo = self.image_cache.get_or_load_pixmap('img.logo_app', 'logo-app.png')
        if logo is not None:
            self.setWindowIcon(QIcon(logo))

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
        icon = self.image_cache.get_or_load_icon(QUIT)
        action_close.setIcon(icon)

        menu_application.addAction(action_close)

    def _init_widgets(self):
        """Initializes widgets"""
        logging.debug('Initializing widgets')

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
        icon = self.image_cache.get_or_load_icon(EDIT)
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

        self.table_ingredients = IngredientsTableView(cb_dropped=self._ingredients_dropped)
        self.model_ingredients = IngredientsTableModel(self.i18n, self.recipe.ingredients, cb_change=self._on_ingredients_changed)
        self.table_ingredients.setModel(self.model_ingredients)
        self._update_headers(self.table_ingredients, self.model_ingredients)

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

        self.table_steps = StepsTableView(cb_dropped=self._steps_dropped)
        self.model_steps = StepsTableModel(self.i18n, self.recipe.steps, cb_change=self._on_steps_changed)
        self.table_steps.setModel(self.model_steps)
        self._update_headers(self.table_steps, self.model_steps)

        label_info_line = QWidget()
        label_info_line.setFixedHeight(1)
        label_info_line.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        label_info_line.setStyleSheet(line_css)

        label_info = QLabel(self.i18n.translate('GUI.RECIPE.VIEW.HEADERS.INFO', 'Information'))
        label_info.setFont(font_label_info)
        label_info.setAlignment(Qt.AlignLeft)

        button_edit_info = QPushButton()
        icon = self.image_cache.get_or_load_icon(EDIT)
        button_edit_info.setIcon(icon)
        button_edit_info.clicked[bool].connect(self._edit_info)

        self.label_info_text = QLabel(self._get_short(self.recipe.information))
        self.label_info_text.setFont(font_label_text)
        self.label_info_text.setAlignment(Qt.AlignLeft)

        button_cancel = QPushButton(self.i18n.translate('GUI.RECIPE.VIEW.ACTIONS.CANCEL', 'Cancel'))
        button_cancel.clicked[bool].connect(self._close)
        button_export = QPushButton(self.i18n.translate('GUI.RECIPE.VIEW.ACTIONS.EXPORT', 'Export'))
        button_export.clicked[bool].connect(self._export)
        button_save = QPushButton(self.i18n.translate('GUI.RECIPE.VIEW.ACTIONS.SAVE', 'Save'))
        button_save.clicked[bool].connect(self._save)
        button_save_close = QPushButton(self.i18n.translate('GUI.RECIPE.VIEW.ACTIONS.SAVE_CLOSE', 'Save & Close'))
        button_save_close.clicked[bool].connect(self._save_close)

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
        layout_grid.addWidget(button_cancel, curr_gridid, 0, 1, 2)
        layout_grid.addWidget(button_export, curr_gridid, 2, 1, 2)
        layout_grid.addWidget(button_save, curr_gridid, 4, 1, 3)
        layout_grid.addWidget(button_save_close, curr_gridid, 7, 1, 3)

        widget.setLayout(layout_grid)

    def _ingredients_dropped(self, from_index, to_index):
        """On ingredients dropped
        :param from_index: From index
        :param to_index: To index
        """
        logging.debug('Ingredients dropped from {} to {}'.format(from_index, to_index))
        self.model_ingredients.relocate_row(from_index, to_index)

    def _steps_dropped(self, from_index, to_index):
        """On steps dropped
        :param from_index: From index
        :param to_index: To index
        """
        logging.debug('Steps dropped from {} to {}'.format(from_index, to_index))
        self.model_steps.relocate_row(from_index, to_index)

    def _edit_recipe_name(self):
        """Edits the recipe name"""
        logging.debug('Edit recipe name')
        name, ok = QInputDialog().getText(self, self.i18n.translate('GUI.RECIPE.VIEW.ACTIONS.EDIT_RECIPE_NAME'), self.i18n.translate('GUI.RECIPE.VIEW.ACTIONS.EDIT_RECIPE_NAME.TEXT'), QLineEdit.Normal, self.recipe.name)
        if ok and name:
            if name != self.recipe.name:
                self.recipe.name = name
                self.label_header.setText(self.recipe.name)
                self.setWindowTitle(self.recipe.name)
                self._changed = True
            else:
                logging.debug('Name did not change')
        else:
            logging.debug('Cancelled')

    def _update_headers(self, table, model):
        """Updates the headers
        :param table: The table
        :param model: The model
        """
        logging.debug('Update table headers')

        header_v = table.verticalHeader()
        if header_v:
            for i in range(0, max(0, len(model._headers_v))):
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
        logo = self.image_cache.get_or_load_pixmap('img.logo_app', 'logo-app.png')
        if logo is not None:
            message_box.setWindowIcon(QIcon(logo))
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

    def _save(self, close=False):
        """Saves the change"""
        logging.debug('Save')
        if not self._changed:
            logging.info('Nothing changed')
            self.show_message(self.i18n.translate('GUI.RECIPE.LOG.RECIPE.SAVED').format(self.recipe.name))
            if close:
                self._close()
            return
        logging.info('Saving recipe to "{}"'.format(self.path_info))
        if save_recipe(self.recipe, self.path_info):
            self._changed = False
            self.show_message(self.i18n.translate('GUI.RECIPE.LOG.RECIPE.SAVED').format(self.recipe.name))
            if close:
                self._close()
        else:
            logging.info('Could not save recipe to "{}"'.format(self.path_info))
            self.show_message(self.i18n.translate('GUI.RECIPE.LOG.RECIPE.SAVED.FAIL').format(self.recipe.name))

    def _save_close(self):
        """Saves the change"""
        logging.debug('Save & Close')
        self._save(close=True)

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
        self._update_headers(self.table_ingredients, self.model_ingredients)
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
        self._update_headers(self.table_steps, self.model_steps)
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

    def _export(self):
        """Export recipe"""
        logging.debug('Exporting')
        selected, dirname = self._select_export_dir()
        if selected:
            try:
                pdf = RecipePDF(orientation='P', unit='mm', format='A4')
                pdf.set_recipe(self.recipe)
                line_height_base = pdf.font_size * 2.5
                pdf.add_page()
                self._add_ingredients(pdf)
                pdf.add_page()
                self._restore(pdf)
                pdf.ln(line_height_base)
                self._add_steps(pdf)
                self._restore(pdf)
                pdf.ln(line_height_base)
                self._add_information(pdf)
                self._restore(pdf)
                pdf.ln(line_height_base)
                outputname = '{}/{}.pdf'.format(dirname, self.recipe.name)
                logging.info('Saving pdf to "{}"'.format(outputname))
                pdf.output(outputname)
                self.show_message(self.i18n.translate('GUI.RECIPE.LOG.RECIPE.EXPORTED').format(self.recipe.name))
                self._open_export_folder(dirname)
            except Exception as e:
                logging.error('Failed to export recipe "{}" to "{}"'.format(self.recipe.name, dirname))
                self.show_message(self.i18n.translate('GUI.RECIPE.LOG.RECIPE.EXPORTED.FAIL').format(self.recipe.name))
                logging.error(e)

    def _restore(self, pdf):
        """Restores color and font

        :param pdf: The PDF
        """
        pdf.set_fill_color(224, 235, 255)
        pdf.set_text_color(0)
        pdf.set_font()

    def _add_ingredients(self, pdf, col_widths=(30, 100, 60)):
        """Adds the ingredients

        :param pdf: The PDF
        :param col_widths: The column widths
        """
        logging.info('Adding ingredients')
        pdf.set_font('helvetica', size=14)
        pdf.cell(txt=self.i18n.translate('GUI.RECIPE.VIEW.HEADERS.INGREDIENTS', 'Zutaten'))
        self._restore(pdf)
        line_height_base = pdf.font_size * 2.5
        pdf.ln(line_height_base)
        pdf.set_font('helvetica', size=12)
        pdf.set_fill_color(211,211,211)
        pdf.set_line_width(0.3)
        headings = [self.i18n.translate('GUI.RECIPE.HEADERS.INGREDIENTS.QUANTITY', 'Quantity'), self.i18n.translate('GUI.RECIPE.HEADERS.INGREDIENTS.NAME', 'Name'), self.i18n.translate('GUI.RECIPE.HEADERS.INGREDIENTS.ADDITION', 'Addition')]
        for col_width, heading in zip(col_widths, headings):
            pdf.cell(col_width, 7, heading, border=1, align="C")
        pdf.ln()
        fill = False
        for i, ingredient in enumerate(self.recipe.ingredients):
            t1 = self._get_none_safe(ingredient.quantity)
            t2 = self._get_none_safe(ingredient.name)
            t3 = self._get_none_safe(ingredient.addition)
            test_split_1 = pdf.multi_cell(col_widths[0], line_height_base, t1, border='LR', new_x='RIGHT', new_y='TOP', max_line_height=pdf.font_size, split_only=True)
            test_split_2 = pdf.multi_cell(col_widths[1], line_height_base, t2, border='LR', new_x='RIGHT', new_y='TOP', max_line_height=pdf.font_size, split_only=True)
            test_split_3 = pdf.multi_cell(col_widths[2], line_height_base, t3, border='LR', new_x='RIGHT', new_y='TOP', max_line_height=pdf.font_size, split_only=True)
            test_split_max = max(max(len(test_split_1), len(test_split_2)), len(test_split_3))
            line_height = pdf.font_size + pdf.font_size * test_split_max
            pdf.multi_cell(col_widths[0], line_height, t1, border='LR', new_x='RIGHT', new_y='TOP', max_line_height=pdf.font_size, fill=fill)
            pdf.multi_cell(col_widths[1], line_height, t2, border='LR', new_x='RIGHT', new_y='TOP', max_line_height=pdf.font_size, fill=fill)
            pdf.multi_cell(col_widths[2], line_height, t3, border='LR', new_x='RIGHT', new_y='TOP', max_line_height=pdf.font_size, fill=fill)
            pdf.ln(line_height)
            fill = not fill
        pdf.cell(sum(col_widths), 0, '', border='T')

    def _add_steps(self, pdf, col_widths=(10, 180)):
        """Adds the steps

        :param pdf: The PDF
        :param col_widths: The column widths
        """
        logging.info('Adding steps')
        pdf.set_font('helvetica', size=14)
        pdf.cell(txt=self.i18n.translate('GUI.RECIPE.VIEW.HEADERS.STEPS', 'Schritte'))
        line_height_base = pdf.font_size * 2
        self._restore(pdf)
        pdf.ln(line_height_base)
        pdf.set_font('helvetica', size=12)
        pdf.set_fill_color(211,211,211)
        pdf.set_line_width(0.3)
        headings = ['#', '']
        for col_width, heading in zip(col_widths, headings):
            pdf.cell(col_width, 7, heading, border=1, align="C")
        pdf.ln()
        fill = False
        for i, step in enumerate(self.recipe.steps):
            step_text = self._get_none_safe(step)
            test_split = pdf.multi_cell(col_widths[1], line_height_base, step_text, border='LR', new_x='RIGHT', new_y='TOP', max_line_height=pdf.font_size, split_only=True)
            line_height = pdf.font_size + pdf.font_size * len(test_split)
            pdf.multi_cell(col_widths[0], line_height, '{}'.format(i + 1), border='LR', new_x='RIGHT', new_y='TOP', max_line_height=pdf.font_size, fill=fill)
            pdf.multi_cell(col_widths[1], line_height, step_text, border='LR', new_x='RIGHT', new_y='TOP', max_line_height=pdf.font_size, fill=fill)
            pdf.ln(line_height)
            fill = not fill
        pdf.cell(sum(col_widths), 0, '', border='T')

    def _add_information(self, pdf):
        """Adds the steps

        :param pdf: The PDF
        """
        logging.info('Adding information')
        pdf.set_font('helvetica', size=14)
        pdf.cell(txt=self.i18n.translate('GUI.RECIPE.VIEW.HEADERS.INFO', 'Information'))
        line_height_base = pdf.font_size * 2
        self._restore(pdf)
        pdf.ln(line_height_base)
        pdf.set_font('helvetica', size=12)
        text = self._get_none_safe(self.recipe.information)
        test_split = pdf.multi_cell(190, line_height_base, text, border='LR', new_x='RIGHT', new_y='TOP', max_line_height=pdf.font_size, split_only=True)
        line_height = pdf.font_size + pdf.font_size * len(test_split)
        pdf.multi_cell(190, line_height, text, border=0, new_x='RIGHT', new_y='TOP', max_line_height=pdf.font_size)
        pdf.ln(line_height)

    def _get_none_safe(self, obj):
        """Returns an empty string if none

        :param obj: The object
        """
        return obj if obj else ''

    def _select_export_dir(self):
        """Selects the export directory"""
        logging.info('Select export dir')

        dirname = QFileDialog.getExistingDirectory(self, self.i18n.translate('GUI.SELECT_EXPORT_DIR.DIALOG.SELECT'), app_conf_get('recipes.folder'), QFileDialog.ShowDirsOnly)
        if dirname:
            logging.info('Selected export directory: "{}"'.format(dirname))
            return True, dirname
        else:
            logging.debug('Cancelled selecting output directory')
            return False, ''

    def _open_export_folder(self, folder):
        """Opens the export folder in the native file explorer"""
        logging.debug('Open export folder "{}"'.format(folder))
        if folder:
            if not QDesktopServices.openUrl(QUrl.fromLocalFile(folder)):
                logging.error('Could not open export folder "{}" in native file explorer'.format(folder))
        else:
            logging.warn('Export folder not set')


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
