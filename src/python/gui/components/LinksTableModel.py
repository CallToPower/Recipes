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

class LinksTableModel(QAbstractTableModel):

    def __init__(self, links=[], headers_h=['Name', 'URL'], headers_v=None, cb_change=None):
        """Initializes the model
        :param links: The links list
        :param headers_h: The horizontal headers list
        :param headers_v: The vertical headers list
        :param cb_change: The callback on data changed
        """
        super(LinksTableModel, self).__init__()

        self._data = self._links_to_datalist(links)
        self._headers_h = headers_h
        self._headers_v = headers_v if headers_v else [i for i in range(0, len(self._data))]
        self._cb_change = cb_change

    # @override
    def data(self, index, role=Qt.DisplayRole):
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
                self._cb_change(self._datalist_to_links())
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
            if orientation == Qt.Vertical:
                return self._headers_v[section]

    # @override
    def rowCount(self, index=QModelIndex()):
        return len(self._data)

    # @override
    def columnCount(self, index=QModelIndex()):
        return len(self._data[0])

    # @override
    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

    def _links_to_datalist(self, links):
        """Converts a list of Link objects to a "plain" data list
        :param links: The list of Link objects
        """
        return [[link.name, link.url] for link in links]

    def _datalist_to_links(self):
        """Converts a "plain" data list to a list of Link objects"""
        return [{'name': d[0], 'url': d[1]} for d in self._data]
