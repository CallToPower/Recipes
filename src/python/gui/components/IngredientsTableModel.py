#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Denis Meyer
#
# This file is part of Rezepte.
#

import logging

from PyQt5.QtCore import Qt, QVariant, QModelIndex
from PyQt5.QtCore import QAbstractTableModel

from classes.Ingredient import Ingredient

class IngredientsTableModel(QAbstractTableModel):

    def __init__(self, ingredients=[], headers=['Quantity', 'Name', 'Further Information'], cb_change=None):
        """Initializes the model
        :param ingredients: The ingredients list
        :param headers: The header list
        :param cb_change: The callback on data changed
        """
        super(IngredientsTableModel, self).__init__()

        self._headers = headers
        self.cb_change = cb_change

        self._data = self._ingredients_to_datalist(ingredients)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.EditRole:
            return self._data[index.row()][index.column()]
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]
        else:
            return QVariant()

    def setData(self, index, value, role):
        if not Qt.EditRole:
            logging.debug('Not edit role')
            return False
        try:
            value_old = self._data[index.row()][index.column()]
            if value_old.strip() == value.strip():
                logging.debug('Data did not change: [row={}, column={}, value={}]'.format(index.row(), index.column(), value))
                return False

            logging.debug('Data changed: [row={}, column={}, value={}]'.format(index.row(), index.column(), value))
            self._data[index.row()][index.column()] = value.strip()
            if self.cb_change:
                self.cb_change(self._datalist_to_ingredients())
        except Exception as e:
            logging.error('Could not change data[row={}, column={}, value={}]: {}'.format(index.row(), index.column(), value, e))
            return False
        return True

    #def insertRows():
    #def removeRows():

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._headers[section] 

    def rowCount(self, index=QModelIndex()):
        return len(self._data)

    def columnCount(self, index=QModelIndex()):
        return len(self._data[0])

    def flags(self, index):
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def _ingredients_to_datalist(self, ingredients):
        """Converts a list of Ingredient objects to a "plain" data list
        :param ingredients: The list of Ingredient objects
        """
        return [[ingredient.quantity, ingredient.name, ingredient.addition] for ingredient in ingredients]

    def _datalist_to_ingredients(self):
        """Converts a "plain" data list to a list of Ingredient objects"""
        return [{'quantity': d[0], 'name': d[1], 'addition': d[2]} for d in self._data]
