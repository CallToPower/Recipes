#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Denis Meyer
#
# This file is part of Rezepte.
#

"""Recipe"""

import logging

from classes.Ingredient import Ingredient

class Recipe():
    """Recipe"""

    def __init__(self, **args):
        """Initializes the recipe"""
        logging.debug('Init recipe')

        self.name = args['name'] if 'name' in args else ''

        self.ingredients = []
        if 'ingredients' in args:
            for d in args['ingredients']:
                ing = Ingredient()
                ing.init_from_obj(d)
                self.ingredients.append(ing)

        self.steps = args['steps'] if 'steps' in args else []

        self.information = args['information'] if 'information' in args else ''

    def get_ingredients_obj(self):
        """Returns the ingredients as object"""
        return [d.as_obj() for d in self.ingredients]

    def get_steps_obj(self):
        """Returns the steps as object"""
        return self.steps

    def get_information_obj(self):
        """Returns the information as object"""
        return self.information

    def __str__(self):
        """to string"""
        ingredients = ', '.join(str(x) for x in self.ingredients)
        return f'Recipe[name="{self.name}",\ningredients=[{ingredients}],\nsteps="{self.steps}",\ninformation={self.information}]'
