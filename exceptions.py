#!/usr/bin/env python3

__author__ = 'Jiajun Huang'

class CmdNotExistError(Exception):
    def __init__(self, value):
        self._value = value

    def __str__(self):
        return str(self._value)
