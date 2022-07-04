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

class StepsTableModel(QAbstractTableModel):

    def __init__(self, i18n, steps=[], cb_change=None):
        """Initializes the model

        :param i18n: The i18n
        :param steps: The steps list
        :param cb_change: The callback on data changed
        """
        super(StepsTableModel, self).__init__()

        self.i18n = i18n
        self._data = self._copy_steps(steps)
        self._headers_h = []
        self._cb_change = cb_change

    # @override
    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.BackgroundColorRole:
            if index.row() % 2 != 0:
                return QVariant(COLOR_GRAY_LIGHT)
        if role == Qt.EditRole:
            return self._data[index.row()]
        if role == Qt.DisplayRole:
            return self._data[index.row()]
        else:
            return QVariant()

    # @override
    def setData(self, index, value, role):
        if not Qt.EditRole:
            logging.debug('Not edit role')
            return False
        try:
            value_old = self._data[index.row()]
            if value_old and value and value_old.strip() == value.strip():
                logging.debug('Data did not change: [row={}, column={}, value={}]'.format(index.row(), index.column(), value))
                return False

            logging.debug('Data changed. [row={}, column={}, old="{}", new="{}"]'.format(index.row(), index.column(), value_old, value))
            self._data[index.row()] = value.strip()
            if self._cb_change:
                self._cb_change(self._data)
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
            if orientation == Qt.Vertical:
                return section + 1

    # @override
    def rowCount(self, index=QModelIndex()):
        if not self._data:
            return 0
        return len(self._data)

    # @override
    def columnCount(self, index=QModelIndex()):
        return 1

    def remove_row(self, row):
        """Removes the selected row
        :param row: Row
        """
        logging.debug('Remove row #{}'.format(row))
        self._data.pop(row)
        self.layoutChanged.emit()
        if self._cb_change:
            self._cb_change(self._data)

    def add_row(self):
        """Adds a row"""
        logging.debug('Add row')
        self._data.append('')
        self.layoutChanged.emit()

    # @override
    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

    def _copy_steps(self, steps):
        """Copies the steps
        :param steps: The steps list
        """
        return [s for s in steps]
