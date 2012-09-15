from __future__ import with_statement
from threading import Thread, Lock, Condition, Semaphore
from os import _exit as quit
import time, random

# a. Add monitor locks and condition variables to ensure that
#    (a) the club is exclusively Goth or Hipster, i.e. no Goth
#        should enter as long as there are Hipsters in the club,
#        and vice versa,
#    (b) the club should always be used as long as there are 
#        customers
#    Note that starvation is not something you need to worry 
#    about. If the club becomes Goth and remains exclusively 
#    Goth for all time, the waiting Hipsters will just have
#    to get old at the door. 
#    Vary the number of Goths and Hipsters to see how your 
#    club behaves.
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
        self.gothcount = 0
        self.hipstercount = 0
        self.club_lock = Lock()
        self.club_condition = Condition(self.club_lock)

    def __sanitycheck(self):
        if self.gothcount > 0 and self.hipstercount > 0:
            print ("sync error: bad social mixup!")
            exit(1)
        if self.gothcount < 0 or self.hipstercount < 0:
            print ("sync error: lost track of people!")
            exit(1)
        
    def goth_enter(self):
        with self.club_lock:
            while self.hipstercount != 0:
                self.club_condition.wait()
            self.gothcount += 1
            self.__sanitycheck()

    def goth_exit(self):
        with self.club_lock:
            self.gothcount -= 1
            self.__sanitycheck()
            if self.gothcount == 0:
                self.club_condition.notify()

    def hipster_enter(self):
        with self.club_lock:
            while self.gothcount != 0:
                self.club_condition.wait()
            self.hipstercount += 1
            self.__sanitycheck()

    def hipster_exit(self):
        with self.club_lock:
            self.hipstercount -= 1
            self.__sanitycheck()
            if self.hipstercount == 0:
                self.club_condition.notify()

class Goth(Thread):
    def __init__(self, id):
        Thread.__init__(self)
        self.id = id

    def run(self):
        global daclub

        while True:
            daclub.goth_enter()
            print ("goth #%d: in the club\n" % self.id)
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
            print ("hipster #%d: in the club\n" % self.id)
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
