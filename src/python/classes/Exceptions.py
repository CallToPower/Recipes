#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Denis Meyer
#
# This file is part of Rezepte.
#

"""Exceptions"""

class Error(Exception):
    """Base class for other exceptions"""
    pass

class FileNotFoundError(Error):
    """Raised when a file has not been found"""
    pass

class JsonProcessingError(Error):
    """Raised when a JSON file could not be processed"""
    pass
