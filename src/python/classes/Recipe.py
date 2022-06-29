#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Denis Meyer
#
# This file is part of Rezepte.
#

from classes.Exceptions import ArgumentsException

from classes.Ingredient import Ingredient
from classes.Link import Link

"""Recipe"""

class Recipe():
    """Recipe"""

    def __init__(self, **args):
        """Initializes the recipe"""
        if not args or not 'name' in args or not 'ingredients' in args or args['ingredients'] == None:
            raise ArgumentsException('Could not extract arguments from {}'.format(args))
        self.name = args['name']
        self.ingredients = [Ingredient(x) for x in args['ingredients']] if 'ingredients' in args else []
        self.steps = args['steps'] if 'steps' in args else []
        self.links = [Link(x) for x in args['links']] if 'links' in args else []

    def __str__(self):
        """to string"""
        return 'Recipe[name="{}",\ningredients=[{}],\nsteps="{}",\nlinks={}]'.format(self.name, ', '.join(str(x) for x in self.ingredients), self.steps, self.links)
