#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Denis Meyer
#
# This file is part of Rezepte.
#

import logging

from PyQt5.QtCore import Qt, QVariant, QModelIndex, QAbstractTableModel
from PyQt5.QtGui import QColor

from classes.Ingredient import Ingredient
from lib.Colors import COLOR_GRAY_LIGHT

class IngredientsTableModel(QAbstractTableModel):

    def __init__(self, i18n, ingredients=[], headers_h=['Quantity', 'Name', 'Further Information'], cb_change=None):
        """Initializes the model

        :param i18n: The i18n
        :param ingredients: The ingredients list
        :param headers_h: The horizontal headers list
        :param cb_change: The callback on data changed
        """
        super(IngredientsTableModel, self).__init__()

        self.i18n = i18n
        self._data = self._ingredients_to_datalist(ingredients)
        self._headers_h = [self.i18n.translate('GUI.RECIPE.HEADERS.INGREDIENTS.QUANTITY'), self.i18n.translate('GUI.RECIPE.HEADERS.INGREDIENTS.NAME'), self.i18n.translate('GUI.RECIPE.HEADERS.INGREDIENTS.ADDITION')]
        self.headers_v = []
        self._cb_change = cb_change

    # @override
    def data(self, index, role=Qt.DisplayRole):
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
    def setData(self, index, value, role):
        if not Qt.EditRole:
            logging.debug('Not edit role')
            return False
        try:
            value_old = self._data[index.row()][index.column()]
            if value_old and value and value_old.strip() == value.strip():
                logging.debug('Data did not change: [row={}, column={}, value={}]'.format(index.row(), index.column(), value))
                return False

            logging.debug('Data changed. [row={}, column={}, old="{}", new="{}"]'.format(index.row(), index.column(), value_old, value))
            self._data[index.row()][index.column()] = value.strip()
            if self._cb_change:
                self._cb_change(self._datalist_to_ingredients())
        except Exception as e:
            logging.error('Could not change data[row={}, column={}, value={}]: {}'.format(index.row(), index.column(), value, e))
            return False

        return True

    # @override
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._headers_h[section]

    # @override
    def rowCount(self, index=QModelIndex()):
        if not self._data:
            return 0
        return len(self._data)

    # @override
    def columnCount(self, index=QModelIndex()):
        if not self._data:
            return 0
        return len(self._data[0])

    # @override
    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

    def remove_row(self, row):
        """Removes the selected row
        :param row: Row
        """
        logging.debug('Remove row #{}'.format(row))
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
        for d in self._data:
            ing = Ingredient()
            ing.init_from_attr(d[0], d[1], d[2])
            lst.append(ing)
        return lst
