#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Denis Meyer
#
# This file is part of Rezepte.
#

"""Information"""

class Information():
    """Information"""

    def __init__(self):
        """Initializes the information"""
        logging.debug('Init Information')

        self.name = None
        self.url = None

    def init_from_obj(self, obj):
        """Initializes the Information
        
        :param obj: Object containing information
        """
        self.name = obj['name'] if 'name' in obj else ''
        self.url = obj['url'] if 'url' in obj else ''

    def init_from_attr(self, name, url):
        """Initializes the Information

        :param name: Name
        :param url: URL
        """
        self.name = name
        self.url = url

    def as_obj(self):
        """Returns the ingredient as object"""
        return {'name': self.name, 'url': self.url}

    def __str__(self):
        """to string"""
        return 'Information[name={}, url={}]'.format(self.name, self.url)
