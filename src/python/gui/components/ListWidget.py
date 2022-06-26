#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Denis Meyer
#
# This file is part of Rezepte.
#

"""ListWidget"""

import logging
import uuid

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout
from i18n.I18n import I18n


class ListWidget(QWidget):
    """Custom QWidget GUI for list elements"""

    def __init__(self, i18n, path_img, img, widget_list, parent=None):
        """Initializes the component

        :param i18n: The I18n
        :param path_img: The image path
        :param img: The image name
        :param widget_list: The list widget
        :param parent: The parent component
        """
        super(ListWidget, self).__init__(parent)
        self.widget_list = widget_list
        self.id = str(uuid.uuid4())
        self.path_img = path_img
        self.i18n = i18n

        label = QLabel("{}".format(img))

        button = QPushButton(self.i18n.translate('GUI.MAIN.WIDGET.REMOVE'))
        button.clicked[bool].connect(self._remove)

        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addStretch()
        layout.addWidget(button)

        self.setLayout(layout)

    def _remove(self):
        """Removes the item from the list"""
        logging.debug('Removing item')

        self.widget_list.current_images.remove(self.path_img)
        items = self.widget_list.findItems('', Qt.MatchRegExp)
        if len(items) > 0:
            for item in items:
                if self.id == item.id:
                    logging.debug("Removing element #{}".format(
                        self.widget_list.row(item)))
                    self.widget_list.takeItem(self.widget_list.row(item))
                    return
