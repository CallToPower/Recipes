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
import tempfile
import os


_app_config = {
    'author': 'Denis Meyer',
    'version': '1.0.0',
    'build': '2022-07-10-1',
    'copyright': '© 2022 Denis Meyer',
    'settings.filename': 'recipes-settings.json',
    'suffix.recipe': '.json',
    'about.logo.scaled.width': 280,
    'about.logo.scaled.height': 80,
    'label.header.font.size': 16,
    'label.info.font.size': 12,
    'label.text.font.size': 10,
    'info.length.max': 80,
    'window.recipe.width': 600,
    'window.recipe.height': 800,
    'logging.log_to_file': False,
    'logging.loglevel': logging.DEBUG,
    'logging.format': '[%(asctime)s] [%(levelname)-5s] [%(module)-20s:%(lineno)-4s] %(message)s',
    'logging.datefmt': '%d-%m-%Y %H:%M:%S',
    'logging.logfile': os.path.join(os.getcwd(), 'logs', 'py-imgscaler.application-{}.log'.format(time.strftime('%d-%m-%Y-%H-%M-%S')))
}


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
