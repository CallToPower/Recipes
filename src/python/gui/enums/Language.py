#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Denis Meyer
#
# This file is part of Rezepte.
#

"""Language"""

from enum import Enum, unique


@unique
class Language(Enum):
    """The language"""
    EN = 10
    DE = 20
