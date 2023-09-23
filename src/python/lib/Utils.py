#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Denis Meyer
#
# This file is part of Rezepte.
#

"""Utils"""

import os
import logging
import json
import platform
from pathlib import Path

from classes.Recipe import Recipe
from classes.Exceptions import JsonProcessingError

from lib.AppConfig import app_conf_get, get_loglevel

from PyQt5.QtGui import QPixmap, QIcon

def is_macos():
    """Check whether OS is macOS

    :return: True if OS is macOS, False else
    """
    if platform.uname().system.startswith('Darw'):
        logging.debug('Platform is Mac OS')
        return True
    else:
        logging.debug('Platform is not Mac OS')
        return False

def verify_recipes_dir():
    """Verifies the recipe dir is present"""
    _dir = app_conf_get('recipes.folder')
    try:
        if not os.path.exists(_dir):
            os.makedirs(_dir)
    except Exception as ex:
        logging.error('Failed creating recipe directory in home directory "%s": %s', _dir, ex)
        raise FileNotFoundError(f'Failed creating recipe directory in home directory "{_dir}"') from ex

def update_logging(loglevel, logtofile=False):
    """Updates the logging

    :param loglevel: DEBUG, INFO, ERROR
    :param logtofile: Flag whether to log to file
    """
    logging.info('Setting log level to "%s"', loglevel)
    _lvl = get_loglevel()
    logging.getLogger().setLevel(_lvl)

    if logtofile:
        logging.info('Logging to file')
        basedir = os.path.dirname(app_conf_get('logging.logfile'))
        try:
            if not os.path.exists(basedir):
                os.makedirs(basedir)
        except Exception as ex:
            logging.error('Failed creating a new directory "%s": %s', basedir, ex)
        handler_file = logging.FileHandler(app_conf_get('logging.logfile'), mode='w', encoding='utf-8', delay=False)
        handler_file.setLevel(_lvl)
        handler_file.setFormatter(logging.Formatter(fmt=app_conf_get('logging.format'), datefmt=app_conf_get('logging.datefmt')))
        logging.getLogger().addHandler(handler_file)
    else:
        logging.info('Not logging to file')

def _load_conf(file_path):
    """Loads the configuration

    :param file_path: The file path
    """
    config = {}
    loaded = False
    if os.path.isfile(file_path):
        logging.info('Config exists. Loading from "%s"', file_path)
        try:
            with open(file_path, 'r', encoding='utf-8') as jsonfile:
                config = json.load(jsonfile)
                loaded = True
        except Exception as ex:
            logging.error('Failed loading from "%s": %s', file_path, ex)

    return loaded, config

def _load_conf_from_home_folder():
    """Loads the configuration from home folder"""
    homedir = str(Path.home())
    homefolder = app_conf_get('conf.folder')
    file = app_conf_get('conf.name')

    file_path = os.path.join(homedir, homefolder, file)
    logging.info('Trying to load configuration from home directory "%s"', file_path)

    return _load_conf(file_path)

def save_conf(config):
    """Saves the configuration to the home directory

    :param config: The config
    """
    homedir = str(Path.home())
    homefolder = app_conf_get('conf.folder')
    file = app_conf_get('conf.name')

    home_dir_path = os.path.join(homedir, homefolder)
    file_path = os.path.join(homedir, homefolder, file)

    logging.info('Writing config to home directory "%s"', file_path)
    try:
        if not os.path.exists(home_dir_path):
            os.makedirs(home_dir_path)
    except Exception as ex:
        logging.error('Failed creating a new directory in home directory "%s": %s', home_dir_path, ex)

    try:
        with open(file_path, 'w', encoding='utf-8') as jsonfile:
            json.dump(config, jsonfile)
    except Exception as ex:
        logging.error('Failed writing to "%s": %s', file_path, ex)

def load_languages(basedir):
    """Loads the available languages

    :param basedir: The base path
    """
    logging.info('Loading available languages')
    path = os.path.join(basedir, 'resources', 'i18n')
    lang_files = [f[:-len('.json')] for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith('.json')]
    logging.info('Available languages: %s', lang_files)
    return lang_files

def load_i18n(basedir, lang):
    """Loads the i18n

    :param basedir: The base path
    :param lang: The language
    """
    file_path = os.path.join(basedir, 'resources', 'i18n', f'{lang}.json')
    logging.info('Trying to load translations from "%s"', file_path)

    translations = {}
    
    if os.path.isfile(file_path):
        logging.info('Translations exist. Loading.')
        try:
            with open(file_path, 'r', encoding='utf-8') as jsonfile:
                translations = json.load(jsonfile)
        except Exception as ex:
            logging.error('Failed loading from "%s": %s', file_path, ex)
    else:
        logging.info('Translations "%s" do not exist.', file_path)

    return translations

def load_pixmap(basedir, file, base_path=None):
    """
    Loads an image, prepares it for play

    :param basedir: The base path
    :param file: The file to load from
    :param base_path: The base path
    """
    if not base_path:
        file_path = os.path.join(basedir, 'resources', file)
    else:
        file_path = os.path.join(basedir, 'resources', base_path, file)
    logging.debug('Loading image "%s" from directory "%s"', file, file_path)
    try:
        return QPixmap(file_path) if os.path.exists(file_path) else None
    except Exception as ex:
        raise FileNotFoundError(f'Could not load image "{file_path}"') from ex

def load_icon(basedir, file, base_path=None):
    """
    Loads an image, prepares it for play

    :param basedir: The base path
    :param file: The file to load from
    :param base_path: The base path
    """
    if not base_path:
        file_path = os.path.join(basedir, 'resources', file)
    else:
        file_path = os.path.join(basedir, 'resources', base_path, file)
    logging.debug('Loading image "%s" from directory "%s"', file, file_path)
    try:
        return QIcon(file_path) if os.path.exists(file_path) else None
    except Exception as ex:
        raise FileNotFoundError(f'Could not load image "{file_path}"') from ex

def load_json(basedir, file, base_path=None):
    """
    Loads a JSON file

    :param basedir: The base path
    :param file: The file to load from
    :param base_path: The base path
    """
    if not base_path:
        file_path = os.path.join(basedir, file)
    else:
        file_path = os.path.join(basedir, base_path, file)
    logging.debug('Loading JSON file "%s" from directory "%s"', file, file_path)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f'Could not load JSON file "{file_path}"')
    try:
        with open(file_path, 'r', encoding='utf-8') as file_json:
            return json.load(file_json)
    except Exception as ex:
        raise JsonProcessingError(f'Could not process JSON file "{file_path}": {e}') from ex

def load_json_recipe(filename):
    """
    Loads a JSON file

    :param filename: The file name
    """
    logging.debug('Loading JSON file "{%s}"', filename)
    if not os.path.exists(filename):
        raise FileNotFoundError(f'Could not load JSON file "{filename}"')
    try:
        with open(filename, 'r', encoding='utf-8') as file_json:
            dict_json = json.load(file_json)
        return Recipe(**dict_json)
    except Exception as ex:
        raise JsonProcessingError(f'Could not process JSON file "{filename}": {e}') from ex

def save_recipe(recipe, path):
    """
    Tries to save the recipe to an existing file
    :param recipe: The recipe
    :param path: The path
    """
    logging.debug('Saving recipe to "%s"', path)

    logging.info('Checking recipe file "%s"', path)
    if os.path.exists(path):
        try:
            logging.info('Removing old recipe file "%s"', path)
            os.remove(path)
        except OSError:
            logging.error('Failed to remove recipe file "%s"', path)
            return False

    logging.info('Creating and writing recipe file "%s"', path)

    data = {
        'name': recipe.name,
        'ingredients': recipe.get_ingredients_obj(),
        'steps': recipe.get_steps_obj(),
        'information': recipe.get_information_obj()
    }

    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f)
        return True
    except Exception as ex:
        logging.error('Failed to create new recipe file "%s": %s', path, ex)
        return False
