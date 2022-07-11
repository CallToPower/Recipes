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

        self._update_headers_v()

    def _update_headers_v(self):
        """Updates the vertical headers"""
        self._headers_v = [(i + 1) for i in range(0, len(self._data))]

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
        if not index.isValid():
            return False

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
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Vertical:
                return self._headers_v[section]

    # @override
    def rowCount(self, index=QModelIndex()):
        if not self._data:
            return 0
        return len(self._data)

    # @override
    def columnCount(self, index=QModelIndex()):
        return 1

    # @override
    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsDropEnabled
        if index.row() < len(self._data):
            return Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled
        return Qt.ItemIsEnabled | Qt.ItemIsEditable

    def supportedDropActions(self):
        return Qt.MoveAction

    def relocate_row(self, from_index, to_index):
        logging.debug('Relocate row from {} to {}'.format(from_index, to_index))
        len_data = len(self._data)
        if from_index >= 0 and from_index < len_data and to_index >= 0 and to_index < len_data:
            self._data.insert(to_index, self._data.pop(from_index))
            self.layoutChanged.emit()
            if self._cb_change:
                self._cb_change(self._data)
        else:
            logging.error('Index does not fit for data length {}'.format(len_data))

    def remove_row(self, row):
        """Removes the selected row
        :param row: Row
        """
        logging.debug('Remove row #{}'.format(row))
        self._data.pop(row)
        self._update_headers_v()
        self.layoutChanged.emit()
        if self._cb_change:
            self._cb_change(self._data)

    def add_row(self):
        """Adds a row"""
        logging.debug('Add row')
        self._data.append('')
        self._update_headers_v()
        self.layoutChanged.emit()

    def _copy_steps(self, steps):
        """Copies the steps
        :param steps: The steps list
        """
        return [s for s in steps]
