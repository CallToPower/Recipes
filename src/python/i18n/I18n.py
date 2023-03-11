#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2019-2022 Denis Meyer
#
# This file is part of ImageScaler.
#

"""The I18n"""

import os
import logging
import json

from lib.Utils import load_languages, load_i18n

class I18n():
    """I18n"""

    def __init__(self, basedir, lang='en'):
        """Initializing Translations

        :param basedir: The base directory
        :param lang: Default language
        """
        self.basedir = basedir

        self.languages = load_languages(self.basedir)
        self.language_main = lang
        self._translations = {}

        self._init()

    def _init(self):
        """Initializes the translations"""
        if not self.language_main in self.languages:
            logging.warn('Language "{}" not found, falling back to "{}"'.format(self.language_main, self.languages[0]))
            self.language_main = self.languages[0]
        lang = self.languages[self.languages.index(self.language_main)]
        self._load_language(lang)

    def _load_language(self, lang):
        """Loads a language"""
        translations = load_i18n(self.basedir, lang)
        for key, val in translations.items():
            self._translations[key] = val

    def change_language(self, lang):
        """Changes the language
        
        :param lang: The language
        """
        logging.info('Changing language to {}'.format(lang))
        self.language_main = lang
        self._init()

    def translate(self, key, default=''):
        """Returns the value for the given key or - if not found - a default value

        :param key: The key to be translated
        :param default: The default if no value could be found for the key
        """
        try:
            return self._translations[key]
        except KeyError as exception:
            logging.error('Returning default for key "{}": "{}"'.format(key, exception))
            return default
