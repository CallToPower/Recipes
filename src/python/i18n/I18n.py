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
    'GUI.TREEVIEW.LOG.DELETE_DIRECTORY': 'Deleted directory "{}"',
    'GUI.TREEVIEW.LOG.DELETE_DIRECTORY.FAIL': 'Could not delete directory "{}"',
    'GUI.TREEVIEW.LOG.DELETE_FILE': 'Deleted recipe "{}"',
    'GUI.TREEVIEW.LOG.DELETE_FILE.FAIL': 'Could not delete recipe "{}"',
    'GUI.TREEVIEW.MESSAGE_BOX.DELETE': 'Delete',
    'GUI.TREEVIEW.MESSAGE_BOX.DELETE.DIRECTORY': 'Do you really want to delete the directory "{}"?',
    'GUI.TREEVIEW.MESSAGE_BOX.DELETE.FILE': 'Do you really want to delete the recipe "{}"?',
    'GUI.TREEVIEW.ACTIONS.NEW_FOLDER': 'New Folder',
    'GUI.TREEVIEW.ACTIONS.NEW_FOLDER.TEXT': 'Name of the new folder:',
    'GUI.TREEVIEW.LOG.CREATE_FOLDER.SUCCESS': 'Successfully created new folder "{}"',
    'GUI.TREEVIEW.LOG.CREATE_FOLDER.FAIL.EXISTS': 'The folder "{}" already exists',
    'GUI.TREEVIEW.ACTIONS.NEW_FILE': 'New Recipe',
    'GUI.TREEVIEW.ACTIONS.NEW_FILE.TEXT': 'Name of the new recipe:',
    'GUI.TREEVIEW.LOG.CREATE_FILE.SUCCESS': 'Successfully created new recipe "{}"',
    'GUI.TREEVIEW.LOG.CREATE_FILE.FAIL.EXISTS': 'The recipe "{}" already exists',
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
    'GUI.RECIPE.VIEW.ACTIONS.CANCEL': 'Close',
    'GUI.RECIPE.VIEW.ACTIONS.SAVE': 'Save',
    'GUI.RECIPE.HEADERS.INGREDIENTS.QUANTITY': 'Quantity',
    'GUI.RECIPE.HEADERS.INGREDIENTS.NAME': 'Name',
    'GUI.RECIPE.HEADERS.INGREDIENTS.ADDITION': 'Further Information',
    'GUI.RECIPE.HEADERS.LINKS.NAME': 'Name',
    'GUI.RECIPE.HEADERS.LINKS.URL': 'URL',
    'GUI.RECIPE.VIEW.ACTIONS.EDIT_RECIPE_NAME': 'Recipe Name',
    'GUI.RECIPE.VIEW.ACTIONS.EDIT_RECIPE_NAME.TEXT': 'New recipe name:',
    'GUI.RECIPE.MESSAGE_BOX.CLOSE': 'CLose recipe',
    'GUI.RECIPE.MESSAGE_BOX.CLOSE.TEXT': 'Do you really wand to close the recipe without saving?',
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
    'GUI.TREEVIEW.LOG.DELETE_DIRECTORY': 'Ordner "{}" gelöscht',
    'GUI.TREEVIEW.LOG.DELETE_DIRECTORY.FAIL': 'Ordner "{}" konnte nicht gelöscht werden',
    'GUI.TREEVIEW.LOG.DELETE_FILE': 'Rezept "{}" gelöscht',
    'GUI.TREEVIEW.LOG.DELETE_FILE.FAIL': 'Rezept "{}" konnte nicht gelöscht werden',
    'GUI.TREEVIEW.MESSAGE_BOX.DELETE': 'Löschen',
    'GUI.TREEVIEW.MESSAGE_BOX.DELETE.DIRECTORY': 'Soll der Ordner "{}" wirklich gelöscht werden?',
    'GUI.TREEVIEW.MESSAGE_BOX.DELETE.FILE': 'Soll das Rezept "{}" wirklich gelöscht werden?',
    'GUI.TREEVIEW.ACTIONS.NEW_FOLDER': 'Neuer Ordner',
    'GUI.TREEVIEW.ACTIONS.NEW_FOLDER.TEXT': 'Name des neuen Ordners:',
    'GUI.TREEVIEW.LOG.CREATE_FOLDER.SUCCESS': 'Neuer Ordner "{}" wurde erfolgreich angelegt',
    'GUI.TREEVIEW.LOG.CREATE_FOLDER.FAIL.EXISTS': 'Der Ordner "{}" existiert bereits',
    'GUI.TREEVIEW.ACTIONS.NEW_FILE': 'Neues Rezept',
    'GUI.TREEVIEW.ACTIONS.NEW_FILE.TEXT': 'Name des neuen Rezeptes:',
    'GUI.TREEVIEW.LOG.CREATE_FILE.SUCCESS': 'Neues Rezept "{}" wurde erfolgreich angelegt',
    'GUI.TREEVIEW.LOG.CREATE_FILE.FAIL.EXISTS': 'Das Rezept "{}" existiert bereits',
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
    'GUI.RECIPE.VIEW.ACTIONS.CANCEL': 'Schließen',
    'GUI.RECIPE.VIEW.ACTIONS.SAVE': 'Speichern',
    'GUI.RECIPE.HEADERS.INGREDIENTS.QUANTITY': 'Anzahl',
    'GUI.RECIPE.HEADERS.INGREDIENTS.NAME': 'Name',
    'GUI.RECIPE.HEADERS.INGREDIENTS.ADDITION': 'Weitere Angaben',
    'GUI.RECIPE.HEADERS.LINKS.NAME': 'Name',
    'GUI.RECIPE.HEADERS.LINKS.URL': 'URL',
    'GUI.RECIPE.VIEW.ACTIONS.EDIT_RECIPE_NAME': 'Rezeptname',
    'GUI.RECIPE.VIEW.ACTIONS.EDIT_RECIPE_NAME.TEXT': 'Neuer Rezeptname:',
    'GUI.RECIPE.MESSAGE_BOX.CLOSE': 'Rezept schließen',
    'GUI.RECIPE.MESSAGE_BOX.CLOSE.TEXT': 'Rezept wirklich ohne zu Speichern schließen?',
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
            logging.warn('Returning default for key "{}": "{}"'.format(key, exception))
            return default
