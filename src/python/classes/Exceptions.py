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

class JsonProcessingError(Error):
    """Raised when a JSON file could not be processed"""
