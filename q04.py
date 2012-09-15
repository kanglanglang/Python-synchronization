from __future__ import with_statement
from threading import Thread, Lock, Condition, Semaphore
from os import _exit as quit
import time, random

# a. Add semaphores to ensure that
#    (a) the club is exclusively Goth or Hipster, i.e. no Goth
#        should enter as long as there are Hipsters in the club,
#        and vice versa,
#    (b) the club should always be used as long as there are 
#        customers
#    Note that starvation is not something you need to worry 
#    about. If the club becomes Goth and remains exclusively 
#    Goth for all time, the waiting Hipsters will just have
#    to get old at the door. 
#
# Modify only the code of the class Club to make the program
# correct.
# Place your synchronization variables inside the Club instance.
# Make sure nobody is holding a Club synchronization variable
# while executing outside the Club code.

def hangout():
    time.sleep(random.randint(0, 2))

class Club:
    def __init__(self):
        self.goth_mutex = Semaphore(1)
        self.hipster_mutex = Semaphore(1)
        self.goth_count = 0
        self.hipster_count = 0
        self.club_control = Semaphore(1)
        
    def goth_enter(self):
        self.goth_mutex.acquire()
        self.goth_count += 1
        if self.goth_count == 1:
            self.club_control.acquire()
        self.goth_mutex.release()

    def goth_exit(self):
        self.goth_mutex.acquire()
        self.goth_count -= 1
        if self.goth_count == 0:
            self.club_control.release()
        self.goth_mutex.release()

    def hipster_enter(self):
        self.hipster_mutex.acquire()
        self.hipster_count += 1
        if self.hipster_count == 1:
            self.club_control.acquire()
        self.hipster_mutex.release()

    def hipster_exit(self):
        self.hipster_mutex.acquire()
        self.hipster_count -= 1
        if self.hipster_count == 0:
            self.club_control.release()
        self.hipster_mutex.release()


class Goth(Thread):
    def __init__(self, id):
        Thread.__init__(self)
        self.id = id

    def run(self):
        global daclub

        while True:
            daclub.goth_enter()
            print ("goth #%d: in the club" % self.id)
            hangout()
            daclub.goth_exit()
            
class Hipster(Thread):
    def __init__(self, id):
        Thread.__init__(self)
        self.id = id

    def run(self):
        global daclub

        while True:
            daclub.hipster_enter()
            print ("hipster #%d: in the club" % self.id)
            hangout()
            daclub.hipster_exit()

NUMGOTH=3
NUMHIPSTER=3
daclub = Club()
for i in range(0, NUMGOTH):
    g = Goth(i)
    g.start()    
for i in range(0, NUMHIPSTER):
    h = Hipster(i)
    h.start()    

