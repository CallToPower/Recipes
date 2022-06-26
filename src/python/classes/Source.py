#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Denis Meyer
#
# This file is part of Rezepte.
#

from classes.Exceptions import ArgumentsException

"""Source"""

class Source():
    """Source"""

    def __init__(self, obj):
        """Initializes the source
        
        :param obj: Object containing information
        """
        if not 'name' in obj:
            raise ArgumentsException('Could not extract arguments from {}'.format(args))
        self.name = obj['name']
        self.url = obj['url'] if 'url' in obj else ''

    def __str__(self):
        """to string"""
        return 'Source[name={}, url={}]'.format(self.name, self.url)
