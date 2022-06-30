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

    def __init__(self, ingredients=[], headers_h=['Quantity', 'Name', 'Further Information'], cb_change=None):
        """Initializes the model
        :param ingredients: The ingredients list
        :param headers_h: The horizontal headers list
        :param cb_change: The callback on data changed
        """
        super(IngredientsTableModel, self).__init__()

        self._data = self._ingredients_to_datalist(ingredients)
        self._headers_h = headers_h
        self._headers_v = []
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
            if value_old.strip() == value.strip():
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
    #def insertRows():

    # @override
    #def removeRows():

    # @override
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._headers_h[section]

    # @override
    def rowCount(self, index=QModelIndex()):
        return len(self._data)

    # @override
    def columnCount(self, index=QModelIndex()):
        return len(self._data[0])

    # @override
    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

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
