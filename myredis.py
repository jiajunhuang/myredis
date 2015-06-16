#!/usr/bin/env python3
# -*- utf-8 -*-

__author__ = 'Jiajun Huang'

import exceptions
from utils import to_bytes

class RedisDB(object):
    def __init__(self):
        self._db = {}

    def lpush(self, listname, *value):
        if to_bytes(listname) not in self._db:
            self._db[listname] = list()
        self._db[listname][0:0] = list(reversed([x for x in value]))
        return len(self._db[listname])

    def lrange(self, listname, start, stop):
        if stop == -1:
            stop = None
        else:
            stop += 1
        return self._db.get(listname, [])[start:stop]
