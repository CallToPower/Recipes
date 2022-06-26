#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Denis Meyer
#
# This file is part of Rezepte.
#

"""Settings"""

import os
import json
import logging

from gui.enums.Language import Language

class Settings():
    """Settings"""

    DEFAULT_SETTINGS_FOLDER_NAME = 'Recipes1'
    DEFAULT_WINDOW_WIDTH = 1200
    DEFAULT_WINDOW_HEIGHT = 800

    def __init__(self, basedir, settings_file_name, i18n):
        """Initializes the settings
        
        :param basedir: The base directory
        :param settings_file_name: The name of the settings file
        :param i18n: The i18n
        """
        self.basedir = basedir
        self.settings_file_name = settings_file_name
        self.i18n = i18n
        self.recipe_folder = os.path.join(self.basedir, self.DEFAULT_SETTINGS_FOLDER_NAME)
        self.window = {
            'width': self.DEFAULT_WINDOW_WIDTH,
            'height': self.DEFAULT_WINDOW_HEIGHT
        }
        self.language = self.i18n.current_language

        self.loaded_from_file = False

    def load(self):
        """Tries to load the settings"""
        logging.debug('Loading settings')

        self.loaded_from_file = False

        logging.info('Checking base dir "{}"'.format(self.basedir))
        try:
            if not os.path.exists(self.basedir):
                logging.info('Creating base dir "{}"'.format(self.basedir))
                os.makedirs(self.basedir)
        except:
            logging.error('Failed to create base dir "{}"'.format(self.basedir))
            return False

        settings_file_path = os.path.join(self.basedir, self.settings_file_name)
        logging.info('Checking settings file "{}"'.format(settings_file_path))
        if not os.path.exists(settings_file_path):
            logging.warn('Settings file does not exist: {}'.format(settings_file_path))
        else:
            logging.info('Loading settings file "{}"'.format(settings_file_path))
            try:
                with open(settings_file_path, 'r', encoding='utf-8') as settings_fp:
                    settings_obj = json.load(settings_fp)
            except:
                logging.error('Failed to read settings file "{}"'.format(settings_file_path))
                return False

            logging.info('Extracting settings')
            self.recipe_folder = settings_obj['recipe_folder'] if 'recipe_folder' in settings_obj else os.path.join(self.basedir, self.DEFAULT_SETTINGS_FOLDER_NAME)
            self.window['width'] = settings_obj['window']['width'] if ('window' in settings_obj) and 'width' in settings_obj['window'] else self.DEFAULT_WINDOW_WIDTH
            self.window['height'] = settings_obj['window']['height'] if ('window' in settings_obj) and 'height' in settings_obj['window'] else self.DEFAULT_WINDOW_HEIGHT
            self.language = self._get_language(settings_obj['language']) if 'language' in settings_obj else Language.DE

            self.loaded_from_file = True

        logging.info('Checking recipe folder "{}"'.format(self.recipe_folder))
        try:
            if not os.path.exists(self.recipe_folder):
                logging.info('Creating recipe folder "{}"'.format(self.recipe_folder))
                os.makedirs(self.recipe_folder)
        except:
            logging.error('Failed to create recipe folder "{}"'.format(self.recipe_folder))
            return False

        return True

    def _get_language(self, lang):
        """Returns the language
        :param lang: The Language string
        """
        if lang == 'EN':
            return Language.EN
        return Language.DE

    def save(self):
        """Tries to save the settings to a file"""
        logging.debug('Saving settings')

        settings_file_name = os.path.join(self.basedir, self.settings_file_name)
        logging.info('Checking settings file "{}"'.format(settings_file_name))
        if os.path.exists(settings_file_name):
            try:
                logging.info('Removing old settings file "{}"'.format(settings_file_name))
                os.remove(settings_file_name)
            except OSError:
                logging.error('Failed to remove settings file "{}"'-format(settings_file_name))
                return False

        logging.info('Creating and writing settings file "{}"'.format(settings_file_name))

        data = {
            'settings_file_name': self.settings_file_name,
            'recipe_folder': self.recipe_folder,
            'window': self.window,
            'language': Language.EN.name if self.i18n.current_language == Language.EN else Language.DE.name
        }

        try:
            with open(settings_file_name, 'w', encoding='utf-8') as f:
                json.dump(data, f)
        except Exception as e:
            logging.error('Failed to create new settings file "{}": {}'.format(settings_file_name, e))
            return False
