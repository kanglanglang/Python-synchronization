from __future__ import with_statement
from threading import Thread, Lock, Condition, Semaphore
from os import _exit as quit

import time, random

def delay():
    time.sleep(random.randint(0, 2))

#Implement reader-writer locks using monitors with condition variables. 
#Reader-writer locks require that you implement four functions in a monitor,
# named reader_enter(),reader_exit(), writer_enter(), and writer_exit(). 
#Assume that readers of a data structure will bracket their read-only accesses 
#to a data structure with calls to  reader_enter(), and reader_exit(). 
#Writers similarly bracket their accesses with writer_enter() and writer_exit().
#Consequently, we say "there is a writer" to mean that a process has executed
#writer_enter() to completion, but not executed writer_exit() yet (and similarly 
#for readers). Implement these four routines to satisfy the following properties: 
#
#(a) there can be at most N readers
#    simultaneously accessing the protected data structure as long as there are no writers
#(b) there can
#    be at most one writer
#(c) no writer may be accessing the object as long as there are more than 0
#    readers, 
#(d) no reader may access an object as long as there is a writer, and 
#(e) the system must make forward progress when it is possible to do so. 
#
#The number of reader and writer threads that
#may want to use your reader-writer lock implementation is unbounded. 
#Python implements Mesastyle semantics for monitors and #condition variables.

class ReaderWriter:
    def __init__(self, reader_limit):
        self.reader_max = reader_limit
        self.reader_count = 0
        self.writer_count = 0
        self.waiting_readers = 0
        self.waiting_writers = 0
        self.monitor_lock = Lock()
        self.can_write = Condition(self.monitor_lock)
        self.can_read = Condition(self.monitor_lock)
        self.full_readers = Condition(self.monitor_lock)

    def __sanitycheck(self):
        if self.reader_count > self.reader_max:
            print ("sync error: more readers than allowed!")
            exit(1)
        if self.writer_count > 1:
            print ("sync error: more than one writer!")
            exit(1)
        if self.writer_count == 1 and self.reader_count > 0:
            print ("sync error: reading and writing at the same time!")
            exit(1)

    def reader_enter(self):
        with self.monitor_lock:
            while self.writer_count==1 or self.waiting_writers > 0 or self.waiting_readers == self.reader_max-1:
                self.waiting_readers += 1
                self.can_read.wait()
                self.waiting_readers -= 1
            self.reader_count += 1
            if self.reader_count < self.reader_max:
                self.can_read.notify()
            elif self.reader_count == self.reader_max:
                full_readers.wait()

    def reader_exit(self):
        with self.monitor_lock:
            self.reader_count -= 1
            if self.reader_count == 0:
                self.can_write.notify()
            elif self.reader_count == self.reader_max - 1:
                self.full_readers.notify()

    def writer_enter(self):
        with self.monitor_lock:
            while self.writer_count == 1 or self.reader_count >0:
                self.waiting_writers+=1
                self.can_write.wait()
                self.waiting_writers-=1
            self.writer_count = 1

    def writer_exit(self):
        with self.monitor_lock:
            self.writer_count = 0
            self.can_write.notify();self.can_read.notify()

class Reader(Thread):
    def __init__(self, _rw_lock):
        Thread.__init__(self)
        self.rwlock = _rw_lock

    def run(self):
        while True:
            self.rwlock.reader_enter()
            print ("Reader entered")
            delay()
            self.rwlock.reader_exit()
            delay()

class Writer(Thread):
    def __init__(self, _rw_lock):
        Thread.__init__(self)
        self.rwlock = _rw_lock
    
    def run(self):
        while True:     
            self.rwlock.writer_enter()
            print ("Writer entered")
            delay()
            self.rwlock.writer_exit()
            delay()

print ("Reader-Writer Problem")
rwlock = ReaderWriter(10)
for i in range(0, 5):
    r = Reader(rwlock)
    r.start()
    w = Writer(rwlock)
    w.start() 
