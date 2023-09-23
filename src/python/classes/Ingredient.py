#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Denis Meyer
#
# This file is part of Rezepte.
#

"""Ingredient"""

class Ingredient():
    """Ingredient"""

    def __init__(self):
        """Initializes the ingredient"""
        self.quantity = None
        self.name = None
        self.addition = None

    def init_from_obj(self, obj):
        """Initializes the ingredient
        
        :param obj: Object containing information
        """
        self.quantity = obj['quantity'] if 'quantity' in obj else None
        self.name = obj['name'] if 'name' in obj else ''
        self.addition = obj['addition'] if 'addition' in obj else ''

    def init_from_attr(self, quantity, name, addition):
        """Initializes the ingredient

        :param quantity: Quantity
        :param name: Name
        :param addition: Addition
        """
        self.quantity = quantity
        self.name = name
        self.addition = addition

    def as_obj(self):
        """Returns the ingredient as object"""
        return {'quantity': self.quantity, 'name': self.name, 'addition': self.addition}

    def __str__(self):
        """to string"""
        return f'Ingredient[quantity={self.quantity}, name={self.name}, addition={self.addition}]'
