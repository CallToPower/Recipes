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

        self.ingredients = []
        if 'ingredients' in args:
            for d in args['ingredients']:
                ing = Ingredient()
                ing.init_from_obj(d)
                self.ingredients.append(ing)

        self.steps = args['steps'] if 'steps' in args else []

        self.links = []
        if 'links' in args:
            for d in args['links']:
                lnk = Link()
                lnk.init_from_obj(d)
                self.links.append(lnk)

    def get_ingredients_obj(self):
        """Returns the ingredients as object"""
        return [d.as_obj() for d in self.ingredients]

    def get_steps_obj(self):
        """Returns the steps as object"""
        return self.steps

    def get_links_obj(self):
        """Returns the links as object"""
        return [d.as_obj() for d in self.links]

    def __str__(self):
        """to string"""
        return 'Recipe[name="{}",\ningredients=[{}],\nsteps="{}",\nlinks={}]'.format(self.name, ', '.join(str(x) for x in self.ingredients), self.steps, self.links)
