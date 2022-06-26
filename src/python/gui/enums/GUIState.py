#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Denis Meyer
#
# This file is part of Rezepte.
#

"""GUI State"""

from enum import Enum, unique


@unique
class GUIState(Enum):
    """The GUI state"""
    INIT_UI = 10
    PHASE_READY = 20
