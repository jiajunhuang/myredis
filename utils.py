#!/usr/bin/env python3

__author__ = 'Jiajun Huang'

import hiredis

def to_arglist(message):
    reader = hiredis.Reader()
    reader.feed(message)
    return reader.gets()

def to_resp(value):
    if isinstance(value, str):
        return ('+%s' % value).encode() + b'\r\n'
    elif isinstance(value, bool) and value:
        return b"+OK\r\n"
    elif isinstance(value, int):
        return (':%s' % value).encode() + b'\r\n'
    elif isinstance(value, bytes):
        return (b'$' + str(len(value)).encode() +
                b'\r\n' + value + b'\r\n')
    elif value is None:
        return b'$-1\r\n'
    elif isinstance(value, list):
        base = b'*' + str(len(value)).encode() + b'\r\n'
        for item in value:
            base += to_resp(item)
        return base

def to_bytes(x):
    if x is None:
        return None
    if isinstance(x, (bytes, bytearray)) or hasattr(x, '__str__'):
        return bytes(x)
    if isinstance(x, str):
        return x.encode()

if __name__ == '__main__':
    msg = b'+OK\r\n'
    msg2 = b'*3\r\n:3\r\n:2\r\n$5\r\nhello\r\n'
    print(to_str(msg))
    print(to_resp(msg2))
