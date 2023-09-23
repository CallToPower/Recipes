#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Denis Meyer
#
# This file is part of Rezepte.
#

"""Icon definitions"""

from gui.data.Icon import Icon

_FOLDER_FLAGS = 'flags'
_FOLDER_ICONS = 'icons'

def get_flag(lang):
    """Returns the flag

    :param lang: The language
    :return: The flag as icon
    """
    return Icon(f'img.flag.{lang}', f'{lang}.png', _FOLDER_FLAGS)

def get_icon(key, value):
    """Returns the icon

    :param value: The value
    :return: The icon
    """
    return Icon(key, value, _FOLDER_ICONS)

# Icons
FOLDER = get_icon('img.icon.folder-regular', 'folder-regular.svg')
FILE = get_icon('img.icon.file-solid', 'file-solid.svg')
SELECT_RECIPE_DIR = get_icon('img.icon.select-recipe', 'book-solid.svg')
DELETE = get_icon('img.icon.delete', 'minus-solid.svg')
MOVE = get_icon('img.icon.move', 'arrow-right-arrow-left-solid.svg')
CREATE_FOLDER = get_icon('img.icon.create_folder', 'folder-plus-solid.svg')
CREATE_FILE = get_icon('img.icon.create_recipe', 'plus-solid.svg')
OPEN_EXTERNAL = get_icon('img.icon.open', 'arrow-up-right-from-square-solid.svg')
EDIT = get_icon('img.icon.edit', 'pen-to-square-solid.svg')
ABOUT = get_icon('img.icon.about', 'address-card-solid.svg')
QUIT = get_icon('img.icon.quit', 'circle-xmark-solid.svg')
