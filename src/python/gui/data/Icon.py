#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Denis Meyer
#
# This file is part of Rezepte.
#

"""Icons"""

class Icon():
    """Icon"""

    def __init__(self, key, name, path):
        """Initializes the icon

        :param key: The key
        :param name: The name
        :param folder: The folder
        """
        self.key = key
        self.name = name
        self.path = path
