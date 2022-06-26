#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Denis Meyer
#
# This file is part of Rezepte.
#

from classes.Exceptions import ArgumentsException

from classes.Ingredients import Ingredients
from classes.Source import Source

"""Recipe"""

class Recipe():
    """Recipe"""

    def __init__(self, **args):
        """Initializes the recipe"""
        if not args or not 'name' in args:
            raise ArgumentsException('Could not extract arguments from {}'.format(args))
        self.name = args['name']
        self.ingredients = Ingredients(args['ingredients']) if 'ingredients' in args else None
        self.description = args['description'] if 'description' in args else ''
        self.source = Source(args['source']) if 'source' in args else {}

    def __str__(self):
        """to string"""
        return 'Recipe[name="{}",\ningredients={},\ndescription="{}",\nsource={}]'.format(self.name, self.ingredients, self.description, self.source)
