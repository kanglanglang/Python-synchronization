from __future__ import with_statement
from threading import Thread, Lock, Condition, Semaphore
from os import _exit as quit

import time

#Life emulation problem
#Scientists have discovered alien life on planet Gliese 538X.
#Unlike earth-based lifeforms,Glieseans have three genders, he, she and it.
#On reaching adulthood, Gliesean organisms go to amating area in search 
#of other Glieseans. When a Gliesean of one gender comes together with two 
#other Glieseans of the other two genders (for example, 
#a she runs into a he and an it) in this area, they form a lifelong 
#physical bond and attach themselves into a triad. Once in a triad, Glieseans
#leave the mating area and are not eligible to form bonds with other Glieseans.
#As an earth scientist,you have been tasked with simulating the mating habits 
#of the Glieseans, using threads, monitors and condition variables. Each Gliesean 
#is modeled by a thread. Fill in the missing code segments below such that
#
#a)the Gliesean triad formation is modeled according to the specification above,
#  paying special attention to make sure that the three-way join is simulated correctly,
#
#b)the code makes forward progress whenever possible to do so (i.e. your simulation 
#  should accommodate every mating opportunity that is present on Gliese 538X. 
#
#Note that Python implements Mesa-style semantics for monitors and condition variable

class MatingArea:
   def __init__(self):
       self.area_lock = Lock()
       self.num_hes = 0
       self.num_shes = 0
       self.num_its = 0
       self.he_needs_triad = Condition(self.area_lock)
       self.she_needs_triad = Condition(self.area_lock)
       self.it_needs_triad = Condition(self.area_lock)

   def he_ready(self):
      with self.area_lock:
         self.num_hes += 1
         if self.num_shes > 0 and self.num_its > 0:
            self.she_needs_triad.notify(); self.it_needs_triad.notify()
            self.num_hes -= 1
         else:
            while self.num_shes == 0 or self.num_its == 0:
               self.he_needs_triad.wait()
            self.num_hes -= 1

   def she_ready(self):
       with self.area_lock:
         self.num_shes += 1
         if self.num_hes > 0 and self.num_its > 0:
            self.he_needs_triad.notify(); self.it_needs_triad.notify()
            self.num_shes -= 1
         else:
            while self.num_hes == 0 or self.num_its == 0:
               self.she_needs_triad.wait()
            self.num_shes -= 1

   def it_ready(self):
       with self.area_lock:
         self.num_its += 1
         if self.num_shes > 0 and self.num_hes > 0:
            self.she_needs_triad.notify(); self.he_needs_triad.notify()
            self.num_its -= 1
         else:
            while self.num_shes == 0 or self.num_hes == 0:
               self.it_needs_triad.wait()
            self.num_its -= 1

ma = MatingArea()

class he(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        print ("He: I'm born!")
        #grow up
        print ("He: Adult now, time to form a triad!")
        ma.he_ready()
        #the code should never get here unless this organism
        #is in a triad
        print ("He: Yay, I'm part of a triad!!!")
        #lives happily ever after, sends laser pulses into 
        #space towards earth.

class she(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        print ("She: I'm born!")
        #grow up
        print ("She: Adult now, time to form a triad!")
        ma.she_ready()
        #the code should never get here unless this organism
        #is in a triad
        print ("She: Yay, I'm part of a triad!!!")
        #lives happily ever after, sends laser pulses into 
        #space towards earth.

class it(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        print ("It: I'm born!")
        #grow up
        print ("It: Adult now, time to form a triad!")
        ma.it_ready()
        #the code should never get here unless this organism
        #is in a triad
        print ("It: Yay, I'm part of a triad!!!")
        #lives happily ever after, sends laser pulses into 
        #space towards earth.

print ("Gleseans Emulation")
for i in range(0, 300):
    m = he()
    m.start()
for i in range(0, 300):
    f = she()
    f.start()
for i in range(0, 300):
    n = it()
    n.start()

