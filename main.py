#!/usr/bin/env python3

import functools
import asyncio
from utils import tostr, toresp
import myredis
import exceptions

class RedisServerProtocol(asyncio.Protocol):
    def __init__(self, redis):
        self._redis = redis
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        parsed = tostr(data)
        print('============', parsed)
        # parsed is an array of [command, *args]
        command = parsed[0].decode().lower()
        try:
            method = getattr(self, command)
        except AttributeError:
            try:
                method = getattr(self._redis, command)
            except AttributeError:
                self.transport.write(
                    b'-ERR unknow command ' + parsed[0] + b'\r\n'
                )
                return
            except rediserr.CmdNotExistError:
                return toresp(None)
        try:
            result = method(*parsed[1:])
        except TypeError:
            self.transport.write(
                b'-ERR command ' + parsed[0] 
                + b' need more arguments' + b'\r\n'
            )
            return
        serialized = toresp(result)
        self.transport.write(serialized)

    def lrange(self, listname, start, stop):
        return self._redis.lrange(listname, int(start), int(stop))

class WireRedisConverter(object):
    def __init__(self, redis):
        self._redis = redis

    def __getattr__(self, command):
        return getattr(self._redis, command)

def run(hostname='localhost', port=6379):
    loop = asyncio.get_event_loop()
    wrapped_redis = WireRedisConverter(myredis.RedisDB())
    bound_protocol = functools.partial(RedisServerProtocol, wrapped_redis)
    coro = loop.create_server(bound_protocol,
                              hostname, port)
    server = loop.run_until_complete(coro)
    print("Listening on port {}".format(port))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("User requested shutdown.")
    finally:
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()
        print("Redis is now ready to exit.")
    return 0

if __name__ == '__main__':
    run()
