#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Denis Meyer
#
# This file is part of Rezepte.
#

"""Tree widget"""

import logging

from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTreeWidget


class TreeWidget(QTreeWidget):
    """TreeWidget"""

    def __init__(self, cb_dropped):
        """Initializes the widget
        :param cb_dropped: Callback dropped
        """
        super().__init__()

        self.cb_dropped = cb_dropped

    # @override
    def dropEvent(self, event):
        source_item = None
        destination_item = None

        source = event.source()
        if source:
            curr_item = source.currentItem()
            source_item = curr_item.data(0, Qt.UserRole)
        
        destination = self.itemAt(event.pos())
        if destination:
            destination_item = destination.data(0, Qt.UserRole)

        if source_item:
            logging.info('Dropped an item')
            if self.cb_dropped:
                self.cb_dropped(source_item, destination_item)
