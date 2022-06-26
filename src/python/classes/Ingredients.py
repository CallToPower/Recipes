#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Denis Meyer
#
# This file is part of Rezepte.
#

from classes.Exceptions import ArgumentsException
from classes.Ingredient import Ingredient

"""Ingredients"""

class Ingredients():
    """Ingredients"""

    def __init__(self, lst):
        """Initializes the ingredients
        
        :param lst: List of ingredients
        """
        if lst == None:
            raise ArgumentsException('Could not extract arguments from {}'.format(args))

        self.lst = [Ingredient(x) for x in lst]

    def __str__(self):
        """to string"""
        return 'Ingredients[{}]'.format(', '.join(str(x) for x in self.lst))
