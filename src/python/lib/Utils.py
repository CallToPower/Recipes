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
from classes.Exceptions import FileNotFoundError, JsonProcessingError

from PyQt5.QtGui import QPixmap, QIcon

def is_macos():
    if platform.uname().system.startswith('Darw'):
        logging.debug('Platform is Mac OS')
        return True
    else:
        logging.debug('Platform is not Mac OS')
        return False

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
    logging.debug('Loading image "{}" from directory "{}"'.format(file, file_path))
    try:
        return QPixmap(file_path) if os.path.exists(file_path) else None
    except:
        raise FileNotFoundError('Could not load image "{}"'.format(file_path))

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
    logging.debug('Loading image "{}" from directory "{}"'.format(file, file_path))
    try:
        return QIcon(file_path) if os.path.exists(file_path) else None
    except:
        raise FileNotFoundError('Could not load image "{}"'.format(file_path))

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
    logging.debug('Loading JSON file "{}" from directory "{}"'.format(file, file_path))
    if not os.path.exists(file_path):
        raise FileNotFoundError('Could not load JSON file "{}"'.format(file_path))
    try:
        with open(file_path, 'r', encoding='utf-8') as file_json:
            return json.load(file_json)
    except Exception as e:
        raise JsonProcessingError('Could not process JSON file "{}": {}'.format(file_path, e))

def load_json_recipe(filename):
    """
    Loads a JSON file

    :param filename: The file name
    """
    logging.debug('Loading JSON file "{}"'.format(filename))
    if not os.path.exists(filename):
        raise FileNotFoundError('Could not load JSON file "{}"'.format(filename))
    try:
        with open(filename, 'r', encoding='utf-8') as file_json:
            dict_json = json.load(file_json)
        return Recipe(**dict_json)
    except Exception as e:
        raise JsonProcessingError('Could not process JSON file "{}": {}'.format(filename, e))

def save_recipe(recipe, path):
    """
    Tries to save the recipe to an existing file
    :param recipe: The recipe
    :param path: The path
    """
    logging.debug('Saving recipe to "{}"'.format(path))

    logging.info('Checking recipe file "{}"'.format(path))
    if os.path.exists(path):
        try:
            logging.info('Removing old recipe file "{}"'.format(path))
            os.remove(path)
        except OSError:
            logging.error('Failed to remove recipe file "{}"'.format(path))
            return False

    logging.info('Creating and writing recipe file "{}"'.format(path))

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
    except Exception as e:
        logging.error('Failed to create new recipe file "{}": {}'.format(path, e))
        return False
