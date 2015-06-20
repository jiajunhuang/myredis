#!/usr/bin/env python3

import functools
import asyncio
from utils import to_arglist, to_resp
import myredis_deque as myredis
from aof import startaof

filename = 'redis.rds'

class MyRedisProtocol(asyncio.Protocol):
    def __init__(self, redis, msgqueue):
        self._redis = redis
        self.msgqueue = msgqueue
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        arglist = to_arglist(data)
        if arglist == False:
            return
        # arglist is an array of [command, *args]
        command = arglist[0].decode().lower()
        try:
            method = getattr(self._redis, command)
        except AttributeError:
            self.transport.write(
                    b'-ERR unknow command ' + arglist[0] + b'\r\n'
                    )
            return
        except NameError:
            self.transport.write(
                    b'-ERR ' + listname + b' not exists\r\n'
                    )
        result = method(*arglist[1:])
        #try:
            #result = method(*arglist[1:])
        #except TypeError:
            #self.transport.write(
                #b'-ERR command ' + arglist[0] 
                #+ b' need more arguments' + b'\r\n'
            #)
            #return
        # command execute successfully, send it to AOF
        self.msgqueue.put(data.decode())
        resp_result = to_resp(result)
        self.transport.write(resp_result)


class RedisWrapper(object):
    '''RedisWrapper is just a wrapper of RedisDB(). 

    because in python's function, we can't directly change argument's reference 
    to another object(it will not work after it return). so when it is needed, 
    we need a wrapper to receive the object return from RedisDB, and change 
    the reference of the change needed object in wrapper to that.
    '''
    def __init__(self, redis):
        self._redis = redis

    def __getattr__(self, command):
        return getattr(self._redis, command)

    def lrange(self, listname, start, stop):
        return self._redis.lrange(listname, int(start), int(stop))

    def ltrim(self, listname, start, stop):
        self._redis._db[listname] = self._redis.lrange(listname, 
                int(start), int(stop))
        return True

    def lpushx(self, listname, value):
        try:
            return self._redis.lpush(listname, value)
        except KeyError:
            return 0

    def rpushx(self, listname, value):
        try:
            return self._redis.rpush(listname, value)
        except KeyError:
            return 0

    def lrem(self, listname, count, value):
        self._redis._db[listname], removed = self._redis.lrem(listname,
                int(count),
                value)
        return removed

def run(hostname='localhost', port=6379):
    # get proc_aof and message queue
    proc_aof, msgqueue = startaof(filename)

    # create asynchronous io loop
    loop = asyncio.get_event_loop()
    wrapped_redis = RedisWrapper(myredis.RedisDB())
    bound_protocol = functools.partial(MyRedisProtocol, 
            wrapped_redis, msgqueue)
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
        proc_aof.join()
        print("Redis is now ready to exit.")
    return 0

if __name__ == '__main__':
    run()
