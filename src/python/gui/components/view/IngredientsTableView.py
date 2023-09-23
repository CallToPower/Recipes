#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Denis Meyer
#
# This file is part of Rezepte.
#

"""IngredientsTableView"""

import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableView

class IngredientsTableView(QTableView):
    """IngredientsTableView"""

    bgcolor_header_css = 'background-color: rgb(230, 230, 230);'

    def __init__(self, cb_dropped=None):
        """Initializes the table view
        :param cb_dropped: Dropped event callback
        """
        super(IngredientsTableView, self).__init__()

        self.cb_dropped = cb_dropped

        self.setStyleSheet('QHeaderView::section { ' + self.bgcolor_header_css + ' }')
        self.resizeRowsToContents()
        self.resizeColumnsToContents()
        self.setWordWrap(True)
        self.verticalHeader().setVisible(False)

        self.setSelectionBehavior(self.SelectRows)
        self.setSelectionMode(self.SingleSelection)
        self.setDragDropMode(self.InternalMove)
        self.setDragDropOverwriteMode(False)

    # @override
    def dropEvent(self, event):
        """dropEvent

        :param event: event
        """
        logging.debug('Drop Event')

        source = event.source()

        if source is not self or (event.dropAction() != Qt.MoveAction and self.dragDropMode() != QtWidgets.QAbstractItemView.InternalMove):
            super().dropEvent(event)

        selection = self.selectedIndexes()
        from_index = selection[0].row() if selection else -1
        to_index = self.indexAt(event.pos()).row()
        if (0 <= from_index < self.model().rowCount() and 0 <= to_index < self.model().rowCount() and from_index != to_index):
            if self.cb_dropped:
                self.cb_dropped(from_index, to_index)
