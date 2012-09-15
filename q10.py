from __future__ import with_statement
from threading import Thread, Lock, Condition, Semaphore
from os import _exit as quit
import time, random

# Use monitor locks and condition variables to ensure that
#    (a) there are no more than N patrons inside the club
#    (b) no hippies enter if the club is more than 10% techno
#    (c) no technoheads enter if the club is more than 25% grunge
#    (d) no grungerockers enter if the club is more than 15% hippies
#
#    Note that starvation is not something you need to worry 
#    about.

def hangout():
    time.sleep(random.randint(0, 2))

class Bouncer:
    def __init__(self, maxcapacity):
        self.max_patrons = maxcapacity
        self.num_hippies = 0
        self.num_techno = 0
        self.num_grunge = 0
        self.bouncer_lock = Lock()
        self.hippies_can_enter = Condition(self.bouncer_lock)
        self.techno_can_enter = Condition(self.bouncer_lock)
        self.grunge_can_enter = Condition(self.bouncer_lock)

    def sanity_check(self, entering_type):
        if self.total_patrons()+1 > self.max_patrons:
            print ("sync error: too many patrons!")
            exit(1)
        if entering_type == 0 and self.percent_techno()>.1:
            print ("sync error: Hippie Entering with more than 10% techno!")
            exit(1)
        if entering_type == 1 and self.percent_grunge()>.25:
            print("sync error: Technohead entering with more than 25% Grungerockers!")
            exit(1)
        if entering_type == 2 and self.percent_hippies()>.15:
            print("sync error: Grungerocker entering with more than 15% Hipppies!")
            exit(1)

    def total_patrons(self):
        total = 0
        total = total + self.num_hippies+self.num_techno+self.num_grunge
        return total
        
    def percent_hippies(self):
        if self.total_patrons() == 0:
            return 0
        else:
            return (self.num_hippies/self.total_patrons())

    def percent_techno(self):
        if self.total_patrons() == 0:
            return 0
        else:
            return (self.num_techno/self.total_patrons())

    def percent_grunge(self):
        if self.total_patrons() == 0:
            return 0
        else:
            return (self.num_grunge/self.total_patrons())
        
    def hippie_enter(self):
        with self.bouncer_lock:
            while (self.total_patrons() >= self.max_patrons) or self.percent_techno()>.1:
                self.hippies_can_enter.wait()
            self.sanity_check(0)
            self.num_hippies+=1

    def hippie_exit(self):
        with self.bouncer_lock:
            old_percent_hippies = self.percent_hippies()
            self.num_hippies-=1
            if self.total_patrons()==self.max_patrons-1:
                self.hippies_can_enter.notify(); self.techno_can_enter.notify(); self.grunge_can_enter.notify()
            elif old_percent_hippies>.15 and self.percent_hippies()<.15:
                self.grunge_can_enter.notify()

    def technohead_enter(self):
        with self.bouncer_lock:
            while (self.total_patrons() >= self.max_patrons) or self.percent_grunge()>.25:
                self.techno_can_enter.wait()
            self.sanity_check(1)
            self.num_techno+=1

    def technohead_exit(self):
        with self.bouncer_lock:
            old_percent_techno = self.percent_techno()
            self.num_techno-=1
            if self.total_patrons()==self.max_patrons-1:
                self.hippies_can_enter.notify(); self.techno_can_enter.notify(); self.grunge_can_enter.notify()
            elif old_percent_techno>.1 and self.percent_techno()<.1:
                self.hippies_can_enter.notify()

    def grungerocker_enter(self):
        with self.bouncer_lock:
            while (self.total_patrons() >= self.max_patrons) or self.percent_hippies()>.15:
                self.grunge_can_enter.wait()
            self.sanity_check(2)
            self.num_grunge+=1

    def grungerocker_exit(self):
        with self.bouncer_lock:
            old_percent_grunge = self.percent_grunge()
            self.num_grunge-=1
            if self.total_patrons()==self.max_patrons-1:
                self.hippies_can_enter.notify(); self.techno_can_enter.notify(); self.grunge_can_enter.notify()
            elif old_percent_grunge>.25 and self.percent_grunge()<.25:
                self.techno_can_enter.notify()

class Technohead(Thread):
    def __init__(self, id):
        Thread.__init__(self)
        self.id = id

    def run(self):
        global bouncer

        while True:
            bouncer.technohead_enter()
            print ("Technohead #%d: rocking in the club" % self.id)
            hangout()
            bouncer.technohead_exit()
            print ("Technohead #%d: exited" % self.id)

class Grungerocker(Thread):
    def __init__(self, id):
        Thread.__init__(self)
        self.id = id

    def run(self):
        global bouncer

        while True:
            bouncer.grungerocker_enter()
            print ("Grungerocker #%d: mushing in the pit" % self.id)
            hangout()
            bouncer.grungerocker_exit()
            print ("Grungerocker #%d: exited" % self.id)

class Hippie(Thread):
    def __init__(self, id):
        Thread.__init__(self)
        self.id = id

    def run(self):
        global bouncer

        while True:
            bouncer.hippie_enter()
            print ("Hippie #%d: mellowing out in the club" % self.id)
            hangout()
            bouncer.hippie_exit()
            print ("Hippie #%d: exited" % self.id)
            
MAXCAPACITY=12
NUMHIPPIE=10
NUMTECHNO=10
NUMGRUNGE=10
bouncer = Bouncer(MAXCAPACITY)
for i in range(1, NUMHIPPIE):
    Hippie(i).start()

for i in range(1, NUMGRUNGE):
    Grungerocker(i).start()

for i in range(1, NUMTECHNO):
    Technohead(i).start()

