#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Denis Meyer
#
# This file is part of Rezepte.
#

"""The I18n"""

import logging

from gui.enums.Language import Language

_translations_en = {
    'GUI.ABOUT.LABEL.AUTHOR': 'Author',
    'GUI.ABOUT.LABEL.COPYRIGHT': 'Copyright',
    'GUI.ABOUT.LABEL.VERSION': 'Version',
    'GUI.ABOUT.LABEL.BUILD': 'Build',
    'GUI.ABOUT.TITLE': 'About Recipes',
    'GUI.MAIN.LOG.PHASE.READY': 'Ready!',
    'GUI.PHASE.READY.HEADER': 'Recipes',
    'GUI.PHASE.READY.CURRENT_FOLDER': 'Cookbook: {} / <b>{}</b>',
    'GUI.PHASE.READY.LOG.LOAD_COOKBOOK.START': 'Loading cookbook',
    'GUI.PHASE.READY.LOG.LOAD_COOKBOOK.DONE': 'Cookbook loaded',
    'GUI.MAIN.MENU.APPNAME': 'Recipes',
    'GUI.MAIN.MENU.ITEM.ABOUT': 'About',
    'GUI.MAIN.MENU.ITEM.QUIT': 'Quit',
    'GUI.MAIN.MENU.LANGUAGE': 'Language',
    'GUI.MAIN.MENU.ITEM.LANGUAGE.DE': 'German',
    'GUI.MAIN.MENU.ITEM.LANGUAGE.EN': 'English',
    'GUI.MAIN.MENU.SETTINGS': 'Settings',
    'GUI.MAIN.MENU.ITEM.SETTINGS.SELECT_RECIPE_DIR': 'Select cookbook',
    'GUI.SELECT_RECIPE_DIR.DIALOG.SELECT': 'Select cookbook',
    'GUI.MAIN.WINDOW.TITLE': 'Recipes'
}

_translations_de = {
    'GUI.ABOUT.LABEL.AUTHOR': 'Autor',
    'GUI.ABOUT.LABEL.COPYRIGHT': 'Copyright',
    'GUI.ABOUT.LABEL.VERSION': 'Version',
    'GUI.ABOUT.LABEL.BUILD': 'Build',
    'GUI.ABOUT.TITLE': 'Über Rezepte',
    'GUI.MAIN.LOG.PHASE.READY': 'Willkommen!',
    'GUI.PHASE.READY.HEADER': 'Rezepte',
    'GUI.PHASE.READY.CURRENT_FOLDER': 'Kochbuch: {} / <b>{}</b>',
    'GUI.PHASE.READY.LOG.LOAD_COOKBOOK.START': 'Kochbuch lädt',
    'GUI.PHASE.READY.LOG.LOAD_COOKBOOK.DONE': 'Kochbuch geladen',
    'GUI.MAIN.MENU.APPNAME': 'Rezepte',
    'GUI.MAIN.MENU.ITEM.ABOUT': 'Über',
    'GUI.MAIN.MENU.ITEM.QUIT': 'Beenden',
    'GUI.MAIN.MENU.LANGUAGE': 'Sprache',
    'GUI.MAIN.MENU.ITEM.LANGUAGE.DE': 'Deutsch',
    'GUI.MAIN.MENU.ITEM.LANGUAGE.EN': 'Englisch',
    'GUI.MAIN.MENU.SETTINGS': 'Einstellungen',
    'GUI.MAIN.MENU.ITEM.SETTINGS.SELECT_RECIPE_DIR': 'Kochbuch auswählen',
    'GUI.SELECT_RECIPE_DIR.DIALOG.SELECT': 'Kochbuch auswählen',
    'GUI.MAIN.WINDOW.TITLE': 'Rezepte'
}

class I18n():
    """I18n"""

    def __init__(self, lang=Language.EN):
        """Initializing Translations

        :param lang: Default language
        """
        self.current_language = lang
        self._translations = None

        self.set_lang()

    def set_lang(self):
        """Sets the language"""
        logging.debug('Setting language to {}'.format(self.current_language))
        if self.current_language == Language.EN:
            self._translations = _translations_en
        else:
            self._translations = _translations_de

    def change_language(self, lang):
        """Changes the language
        
        :param lang: The language
        """
        logging.info('Changing language to {}'.format(lang))
        if lang == Language.EN:
            self.current_language = Language.EN
        else:
            self.current_language = Language.DE

        self.set_lang()

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
