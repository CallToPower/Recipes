#!/usr/bin/env python3
# -*- coding: 'utf-8 -*-
#
# Copyright 2022 Denis Meyer
#
# This file is part of Rezepte.
#

"""AppConfig"""

import logging
import time
from pathlib import Path

_app_config = {
    'author': 'Denis Meyer',
    'version': '1.2.0',
    'build': '2023-03-11-1',
    'copyright': '© 2022-2023 Denis Meyer',
    'conf.folder': 'Recipes',
    'conf.name': 'conf.json',
    'language.main': 'en',
    'suffix.recipe': '.json',
    'recipes.folder': str(Path.home()) + '/Recipes/Recipes-Cookbook',
    'about.logo.scaled.width': 280,
    'about.logo.scaled.height': 80,
    'label.header.font.size': 16,
    'label.info.font.size': 12,
    'label.text.font.size': 10,
    'info.length.max': 80,
    'window.recipe.width': 600,
    'window.recipe.height': 800,
    'logging.log_to_file': False,
    'logging.loglevel': 'INFO',
    'logging.format': '[%(asctime)s] [%(levelname)-5s] [%(module)-20s:%(lineno)-4s] %(message)s',
    'logging.datefmt': '%d-%m-%Y %H:%M:%S',
    'logging.logfile': str(Path.home()) + '/Recipes/logs/application-' + time.strftime('%d-%m-%Y-%H-%M-%S') + '.log'
}

def get_loglevel():
    """Returns the log level

    :return: The log level
    """
    _loglvl = app_conf_get('logging.loglevel')
    _lvl = logging.INFO
    if _loglvl == 'DEBUG':
        _lvl = logging.DEBUG
    elif _loglvl == 'ERROR':
        _lvl = logging.DEBUG

    return _lvl

def get_public_values():
    """Returns a dict with public values to write to a config file"""
    vals = ['window.recipe.width',
            'window.recipe.height',
            'label.header.font.size',
            'label.info.font.size',
            'label.text.font.size',
            'language.main',
            'recipes.folder',
            'logging.log_to_file',
            'logging.loglevel'
            ]
    _dict = {}
    for v in vals:
        _dict[v] = app_conf_get(v)

    return _dict

def app_conf_set(key, value):
    """Sets the value for the given key

    :param key: The key
    :param value: The value
    """
    _app_config[key] = value

def app_conf_get(key, default=''):
    """Returns the value for the given key or - if not found - a default value

    :param key: The key
    :param default: The default if no value could be found for the key
    """
    try:
        return _app_config[key]
    except KeyError as exception:
        logging.warn('Returning default for key "{}": "{}"'.format(key, exception))
        return default
