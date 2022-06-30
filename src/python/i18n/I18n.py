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
    'GUI.MAIN.LOG.TREEVIEW': 'Welcome!',
    'GUI.TREEVIEW.HEADER': 'Recipes',
    'GUI.TREEVIEW.CURRENT_FOLDER': 'Cookbook: {}',
    'GUI.TREEVIEW.LOG.LOAD_COOKBOOK.START': 'Loading cookbook',
    'GUI.TREEVIEW.LOG.LOAD_COOKBOOK.DONE': 'Cookbook loaded',
    'GUI.RECIPE.MENU.RECIPE.NAME': 'Recipe',
    'GUI.RECIPE.MENU.ITEM.CLOSE': 'Close',
    'GUI.RECIPE.VIEW.HEADERS.INGREDIENTS': 'Ingredients',
    'GUI.RECIPE.VIEW.HEADERS.STEPS': 'Steps',
    'GUI.RECIPE.VIEW.HEADERS.LINKS': 'Links',
    'GUI.RECIPE.VIEW.ACTIONS.INGREDIENTS.REMOVE': '-',
    'GUI.RECIPE.VIEW.ACTIONS.INGREDIENTS.ADD': '+',
    'GUI.RECIPE.VIEW.ACTIONS.STEPS.REMOVE': '-',
    'GUI.RECIPE.VIEW.ACTIONS.STEPS.ADD': '+',
    'GUI.RECIPE.VIEW.ACTIONS.LINKS.REMOVE': '-',
    'GUI.RECIPE.VIEW.ACTIONS.LINKS.ADD': '+',
    'GUI.RECIPE.VIEW.ACTIONS.CANCEL': 'Cancel',
    'GUI.RECIPE.VIEW.ACTIONS.SAVE': 'Save',
    'GUI.RECIPE.HEADERS.INGREDIENTS.QUANTITY': 'Quantity',
    'GUI.RECIPE.HEADERS.INGREDIENTS.NAME': 'Name',
    'GUI.RECIPE.HEADERS.INGREDIENTS.ADDITION': 'Further Information',
    'GUI.RECIPE.HEADERS.LINKS.NAME': 'Name',
    'GUI.RECIPE.HEADERS.LINKS.URL': 'URL',
    'GUI.MAIN.LOG.RECIPE': 'Opened recipe: "{}"',
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
    'GUI.MAIN.LOG.TREEVIEW': 'Willkommen!',
    'GUI.TREEVIEW.HEADER': 'Rezepte',
    'GUI.TREEVIEW.CURRENT_FOLDER': 'Kochbuch: {}',
    'GUI.TREEVIEW.LOG.LOAD_COOKBOOK.START': 'Kochbuch lädt',
    'GUI.TREEVIEW.LOG.LOAD_COOKBOOK.DONE': 'Kochbuch geladen',
    'GUI.RECIPE.MENU.RECIPE.NAME': 'Rezept',
    'GUI.RECIPE.MENU.ITEM.CLOSE': 'Schließen',
    'GUI.RECIPE.VIEW.HEADERS.INGREDIENTS': 'Zutaten',
    'GUI.RECIPE.VIEW.HEADERS.STEPS': 'Schritte',
    'GUI.RECIPE.VIEW.HEADERS.LINKS': 'Links',
    'GUI.RECIPE.VIEW.ACTIONS.INGREDIENTS.REMOVE': '-',
    'GUI.RECIPE.VIEW.ACTIONS.INGREDIENTS.ADD': '+',
    'GUI.RECIPE.VIEW.ACTIONS.STEPS.REMOVE': '-',
    'GUI.RECIPE.VIEW.ACTIONS.STEPS.ADD': '+',
    'GUI.RECIPE.VIEW.ACTIONS.LINKS.REMOVE': '-',
    'GUI.RECIPE.VIEW.ACTIONS.LINKS.ADD': '+',
    'GUI.RECIPE.VIEW.ACTIONS.CANCEL': 'Abbrechen',
    'GUI.RECIPE.VIEW.ACTIONS.SAVE': 'Speichern',
    'GUI.RECIPE.HEADERS.INGREDIENTS.QUANTITY': 'Anzahl',
    'GUI.RECIPE.HEADERS.INGREDIENTS.NAME': 'Name',
    'GUI.RECIPE.HEADERS.INGREDIENTS.ADDITION': 'Weitere Angaben',
    'GUI.RECIPE.HEADERS.LINKS.NAME': 'Name',
    'GUI.RECIPE.HEADERS.LINKS.URL': 'URL',
    'GUI.MAIN.LOG.RECIPE': 'Geöffnetes Rezept: "{}"',
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
