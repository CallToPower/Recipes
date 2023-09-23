#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Denis Meyer
#
# This file is part of Rezepte.
#

"""StepsTableModel"""

import logging

from PyQt5.QtCore import Qt, QVariant, QModelIndex, QAbstractTableModel
from PyQt5.QtGui import QColor

from lib.Colors import COLOR_GRAY_LIGHT

class StepsTableModel(QAbstractTableModel):
    """StepsTableModel"""

    def __init__(self, i18n, steps=[], cb_change=None):
        """Initializes the model

        :param i18n: The i18n
        :param steps: The steps list
        :param cb_change: The callback on data changed
        """
        super(StepsTableModel, self).__init__()

        self.i18n = i18n
        self._data = self._copy_steps(steps)
        self.headers_h = []
        self._cb_change = cb_change

        self._updateheaders_v()

    def _updateheaders_v(self):
        """Updates the vertical headers"""
        self.headers_v = [(i + 1) for i in range(0, len(self._data))]

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
            return self._data[index.row()]
        if role == Qt.DisplayRole:
            return self._data[index.row()]
        else:
            return QVariant()

    # @override
    def setData(self, index, value, _role):
        """setData

        :param index: index
        :param value: indevaluex
        :param _role: role
        """
        if not index.isValid():
            return False

        if not Qt.EditRole:
            logging.debug('Not edit role')
            return False
        try:
            value_old = self._data[index.row()]
            if value_old and value and value_old.strip() == value.strip():
                logging.debug('Data did not change: [row=%d, column=%d, value=%s]', index.row(), index.column(), value)
                return False

            logging.debug('Data changed. [row=%d, column=%d, old="%s", new="%s"]', index.row(), index.column(), value_old, value)
            self._data[index.row()] = value.strip()
            if self._cb_change:
                self._cb_change(self._data)
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
            if orientation == Qt.Vertical:
                return self.headers_v[section]

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
        return 1

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
                self._cb_change(self._data)
        else:
            logging.error('Index does not fit for data length %d', len_data)

    def remove_row(self, row):
        """Removes the selected row

        :param row: Row
        """
        logging.debug('Remove row #%d', row)
        self._data.pop(row)
        self._updateheaders_v()
        self.layoutChanged.emit()
        if self._cb_change:
            self._cb_change(self._data)

    def add_row(self):
        """Adds a row"""
        logging.debug('Add row')
        self._data.append('')
        self._updateheaders_v()
        self.layoutChanged.emit()

    def _copy_steps(self, steps):
        """Copies the steps

        :param steps: The steps list
        """
        return list(steps)
