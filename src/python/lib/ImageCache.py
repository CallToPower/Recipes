#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Denis Meyer
#
# This file is part of Rezepte.
#

"""ImageCache"""

import logging

from lib.Utils import load_pixmap, load_icon

class ImageCache():
    """ImageCache"""

    _cache_pixmap = {
        'img.logo_app': None,
        'img.logo_app-de': None,
        'img.logo_app-en': None
    }

    _cache_icon = {
        'img.flag.en': None,
        'img.flag.de': None,
        'img.icon.folder-regular': None,
        'img.icon.file-solid': None,
        'img.icon.select-recipe': None,
        'img.icon.delete': None,
        'img.icon.move': None,
        'img.icon.create_folder': None,
        'img.icon.create_recipe': None,
        'img.icon.open': None,
        'img.icon.edit': None,
        'img.icon.about': None,
        'img.icon.quit': None
    }

    def __init__(self, basedir):
        """Initializes the image cache
        
        :param basedir: The base path
        """
        logging.debug('Initializing ImageCache')

        self.basedir = basedir

    def get_or_load_pixmap(self, key, name, path=None):
        """Gets or, if not present, loads the image

        :param key: The key
        :param name: The name
        :param path: The path
        """
        val = self.get_pixmap(key)
        if not val:
            self.set_pixmap(key, load_pixmap(self.basedir, name, path))
            val = self.get_pixmap(key)

        return val

    def _get_or_load_icon(self, key, name, path=None):
        """Gets or, if not present, loads the image

        :param key: The key
        :param name: The name
        :param path: The path
        """
        val = self.get_icon(key)
        if not val:
            self.set_icon(key, load_icon(self.basedir, name, path))
            val = self.get_icon(key)

        return val

    def get_or_load_icon(self, icdef):
        """Gets or, if not present, loads the image via IconDefinition class

        :param icdef: The IconDefinition class
        """
        return self._get_or_load_icon(icdef.key, icdef.name, icdef.path)

    def set_pixmap(self, key, value, override=False):
        """Sets the value for the given key

        :param key: The key
        :param value: The value
        :param override: Whether to force override
        """
        if override or not key in self._cache_pixmap or not self.get_pixmap(key):
            self._cache_pixmap[key] = value

    def set_icon(self, key, value, override=False):
        """Sets the value for the given key

        :param key: The key
        :param value: The value
        :param override: Whether to force override
        """
        if override or not key in self._cache_icon or not self.get_icon(key):
            self._cache_icon[key] = value

    def get_pixmap(self, key, default=None):
        """Returns the value for the given key or - if not found - a default value

        :param key: The key
        :param default: The default if no value could be found for the key
        """
        try:
            return self._cache_pixmap[key]
        except KeyError as exception:
            logging.warning('Returning default for key "%s": "%s"', key, exception)
            return default

    def get_icon(self, key, default=None):
        """Returns the value for the given key or - if not found - a default value

        :param key: The key
        :param default: The default if no value could be found for the key
        """
        try:
            return self._cache_icon[key]
        except KeyError as exception:
            logging.warning('Returning default for key "%s": "%s"', key, exception)
            return default
