#!/usr/bin/env python3
# -*- utf-8 -*-

__author__ = 'Jiajun Huang'

from collections import deque
import itertools

class RedisDB(object):
    def __init__(self):
        self._db = {}

    # operations on list
    # must make sure listname is bytes.
    def lpush(self, listname, *value):
        if listname not in self._db:
            self._db[listname] = deque()
        self._db[listname].extendleft(list(reversed([x for x in value])))
        return len(self._db[listname])

    def rpush(self, listname, *value):
        if listname not in self._db:
            self._db[listname] = deque()
        self._db[listname].extend([x for x in value])
        return len(self._db[listname])

    def lrange(self, listname, start, stop):
        if stop == -1:
            stop = None
        else:
            stop += 1
        mydeque = self._db.get(listname, [])
        return list(itertools.islice(mydeque, start, stop))

    def lindex(self, listname, index):
        try:
            return self._db[listname][index]
        except IndexError:
            return None

    def linsert(self, listname, direction, pivot, value):
        pass

    def llen(self, listname):
        try:
            return len(self._db[listname])
        except KeyError:
            return 0

    def lpop(self, listname):
        try:
            return self._db[listname].popleft()
        except IndexError:
            return None

    def rpop(self, listname):
        try:
            return self._db[listname].pop()
        except IndexError:
            return None

    def lset(self, listname, index, value):
        self._db[listname][index] = value

    def rpoplpush(self, listname, source, destination):
        try:
            self._db[lsitname].rotate()
        except NameError:
            return None
    
    def lrem(self, listname, count:int, value):
        '''to keep the api same, i;m not going implement lrem with 
        deque.remove'''
        result = []
        removed = 0
        if count == 0:
            result = [x for x in self._db[listname] if x != value]
            removed = len(self._db[listname]) - len(result)
            return (result, removed)
        elif count > 0:
            for x in self._db[listname]:
                if x == value and count > 0:
                    count -= 1
                    removed += 1
                    continue
                result.append(x)
            return (result, removed)
        else:
            for x in list(reversed(self._db[listname])):
                if x == value and count < 0:
                    count += 1
                    removed += 1
                    continue
                result.append(x)
            return (result, removed)

    ## unimplement methods with block
    def blpop(self, *listname, timeout):
        pass
    def brpop(self, *listname, timeout):
        pass
    def brpoplpush(self, source, destination, timeout):
        pass

    # operations on keys.
    def exists(self, key):
        realkey = key.decode().lower()
        if key in self._db:
            return 1
        else:
            return 0
    
    def get(self, key):
        try:
            return self._db[key]
        except KeyError:
            return None

    def set(self, key, value):
        self._db[key] = value

    def del(self, *keys):
        count = 0
        for key in keys:
            try:
                del(self._db[key])
                count += 1
            except KeyError:
                pass
        return count
