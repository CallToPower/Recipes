#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Denis Meyer
#
# This file is part of Rezepte.
#

from classes.Exceptions import ArgumentsException

from classes.Ingredient import Ingredient
from classes.Source import Source

"""Recipe"""

class Recipe():
    """Recipe"""

    def __init__(self, **args):
        """Initializes the recipe"""
        if not args or not 'name' in args or not 'ingredients' in args or args['ingredients'] == None:
            raise ArgumentsException('Could not extract arguments from {}'.format(args))
        self.name = args['name']
        self.ingredients = [Ingredient(x) for x in args['ingredients']] if 'ingredients' in args else []
        self.description = args['description'] if 'description' in args else ''
        self.source = Source(args['source']) if 'source' in args else {}

    def __str__(self):
        """to string"""
        return 'Recipe[name="{}",\ningredients=[{}],\ndescription="{}",\nsource={}]'.format(self.name, ', '.join(str(x) for x in self.ingredients), self.description, self.source)
