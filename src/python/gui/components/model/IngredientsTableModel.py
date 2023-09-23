#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Denis Meyer
#
# This file is part of Rezepte.
#

"""IngredientsTableModel"""

import logging

from PyQt5.QtCore import Qt, QVariant, QModelIndex, QAbstractTableModel
from PyQt5.QtGui import QColor

from classes.Ingredient import Ingredient
from lib.Colors import COLOR_GRAY_LIGHT

class IngredientsTableModel(QAbstractTableModel):
    """IngredientsTableModel"""

    def __init__(self, i18n, ingredients=[], cb_change=None):
        """Initializes the model

        :param i18n: The i18n
        :param ingredients: The ingredients list
        :param cb_change: The callback on data changed
        """
        super(IngredientsTableModel, self).__init__()

        self.i18n = i18n
        self._data = self._ingredients_to_datalist(ingredients)
        # 'Quantity', 'Name', 'Further Information'
        self.headers_h = [self.i18n.translate('GUI.RECIPE.HEADERS.INGREDIENTS.QUANTITY', 'Quantity'), self.i18n.translate('GUI.RECIPE.HEADERS.INGREDIENTS.NAME', 'Name'), self.i18n.translate('GUI.RECIPE.HEADERS.INGREDIENTS.ADDITION', 'Addition')]
        self.headers_v = []
        self._cb_change = cb_change

    # @override
    def data(self, index, role=Qt.DisplayRole):
        """data

        :param index: index
        :param role: role
        """
        if role == Qt.BackgroundColorRole:
            if index.row() % 2 != 0:
                return QVariant(COLOR_GRAY_LIGHT)
        if role == Qt.EditRole:
            return self._data[index.row()][index.column()]
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]
        else:
            return QVariant()

    # @override
    def setData(self, index, value, _role):
        """setData

        :param index: index
        :param value: value
        :param _role: role
        """
        if not index.isValid():
            return False

        if not Qt.EditRole:
            logging.debug('Not edit role')
            return False
        try:
            value_old = self._data[index.row()][index.column()]
            if value_old and value and value_old.strip() == value.strip():
                logging.debug('Data did not change: [row=%d, column=%d, value=%s]', index.row(), index.column(), value)
                return False

            logging.debug('Data changed. [row=%d, column=%d, old="%s", new="%s"]', index.row(), index.column(), value_old, value)
            self._data[index.row()][index.column()] = value.strip()
            if self._cb_change:
                self._cb_change(self._datalist_to_ingredients())
        except Exception as ex:
            logging.error('Could not change data[row=%d, column=%d, value=%s]: %s', index.row(), index.column(), value, ex)
            return False

        return True

    # @override
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """headerData

        :param section: section
        :param orientation: orientation
        :param role: role
        """
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.headers_h[section]

    # @override
    def rowCount(self, _index=QModelIndex()):
        """rowCount

        :param _index: index
        """
        if not self._data:
            return 0
        return len(self._data)

    # @override
    def columnCount(self, _index=QModelIndex()):
        """columnCount

        :param _index: index
        """
        if not self._data:
            return 0
        return len(self._data[0])

    # @override
    def flags(self, index):
        """flags

        :param index: index
        """
        if not index.isValid():
            return Qt.ItemIsDropEnabled
        if index.row() < len(self._data):
            return Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled
        return Qt.ItemIsEnabled | Qt.ItemIsEditable

    def supportedDropActions(self):
        """supportedDropActions"""
        return Qt.MoveAction

    def relocate_row(self, from_index, to_index):
        """relocate_row

        :param from_index: from_index
        :param to_index: to_index
        """
        logging.debug('Relocate row from %d to %d', from_index, to_index)
        len_data = len(self._data)
        if from_index >= 0 and from_index < len_data and to_index >= 0 and to_index < len_data:
            self._data.insert(to_index, self._data.pop(from_index))
            self.layoutChanged.emit()
            if self._cb_change:
                self._cb_change(self._datalist_to_ingredients())
        else:
            logging.error('Index does not fit for data length %d', len_data)

    def remove_row(self, row):
        """Removes the selected row

        :param row: Row
        """
        logging.debug('Remove row #%d', row)
        self._data.pop(row)
        self.layoutChanged.emit()
        if self._cb_change:
            self._cb_change(self._datalist_to_ingredients())

    def add_row(self):
        """Adds a row"""
        logging.debug('Add row')
        self._data.append([None, '', None])
        self.layoutChanged.emit()

    def _ingredients_to_datalist(self, ingredients):
        """Converts a list of Ingredient objects to a "plain" data list
        :param ingredients: The list of Ingredient objects
        """
        return [[ingredient.quantity, ingredient.name, ingredient.addition] for ingredient in ingredients]

    def _datalist_to_ingredients(self):
        """Converts a "plain" data list to a list of Ingredient objects"""
        lst = []
        for dat in self._data:
            ing = Ingredient()
            ing.init_from_attr(dat[0], dat[1], dat[2])
            lst.append(ing)
        return lst
