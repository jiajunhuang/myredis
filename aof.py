#!/usr/bin/env python3

# this file implement redis AOF.

from multiprocessing import Process,Queue
import signal
import os
import sys
from time import sleep

def aof(msgqueue, filename):
    try:
        print('aof processs pid: {%d}' % os.getpid())
        with open (filename, 'a') as f:
            while True:
                msg = msgqueue.get()
                f.write(str(msg))
    except KeyboardInterrupt:
        sys.exit()

def startaof(filename):
    msgqueue = Queue()
    proc_aof = Process(target=aof, args=(msgqueue, filename,))
    proc_aof.start()
    print('redis aof get ready!')
    return (proc_aof, msgqueue)
