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

# Flags
FLAG_DE = Icon('img.flag.de', 'de.png', _FOLDER_FLAGS)
FLAG_EN = Icon('img.flag.en', 'en.png', _FOLDER_FLAGS)

# Icons
FOLDER = Icon('img.icon.folder-regular', 'folder-regular.svg', _FOLDER_ICONS)
FILE = Icon('img.icon.file-solid', 'file-solid.svg', _FOLDER_ICONS)
SELECT_RECIPE_DIR = Icon('img.icon.select-recipe', 'book-solid.svg', _FOLDER_ICONS)
DELETE = Icon('img.icon.delete', 'minus-solid.svg', _FOLDER_ICONS)
MOVE = Icon('img.icon.move', 'arrow-right-arrow-left-solid.svg', _FOLDER_ICONS)
CREATE_FOLDER = Icon('img.icon.create_folder', 'folder-plus-solid.svg', _FOLDER_ICONS)
CREATE_FILE = Icon('img.icon.create_recipe', 'plus-solid.svg', _FOLDER_ICONS)
OPEN_EXTERNAL = Icon('img.icon.open', 'arrow-up-right-from-square-solid.svg', _FOLDER_ICONS)
EDIT = Icon('img.icon.edit', 'pen-to-square-solid.svg', _FOLDER_ICONS)
ABOUT = Icon('img.icon.about', 'address-card-solid.svg', _FOLDER_ICONS)
QUIT = Icon('img.icon.quit', 'circle-xmark-solid.svg', _FOLDER_ICONS)
