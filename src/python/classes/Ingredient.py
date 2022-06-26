#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Denis Meyer
#
# This file is part of Rezepte.
#

from classes.Exceptions import ArgumentsException

"""Ingredient"""

class Ingredient():
    """Ingredient"""

    def __init__(self, obj):
        """Initializes the ingredient
        
        :param obj: Object containing information
        """
        if not 'name' in obj:
            raise ArgumentsException('Could not extract arguments from {}'.format(args))
        self.quantity = obj['quantity'] if 'quantity' in obj else None
        self.name = obj['name']
        self.addition = obj['addition'] if 'addition' in obj else ''

    def __str__(self):
        """to string"""
        return 'Ingredient[quantity={}, name={}, addition={}]'.format(self.quantity, self.name, self.addition)
