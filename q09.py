from __future__ import with_statement
from threading import Thread, Lock, Condition, Semaphore
from os import _exit as quit
import time, random

# modify the parent thread to create 200 child threads, each with a unique id,
# wait for the children to print to the screen 5 times each,
# then the parent should print that the children are done.
# 
# the parent and children should use semaphores for synchronization

num_children = 200
num_children_done = 0
child_can_print = Semaphore(1)
parent_can_print = Semaphore(0)

class Child(Thread):
    def __init__(self, myid):
        Thread.__init__(self)
        self.myid = myid

    def run(self):
        global num_children_done
        global child_can_print
        global parent_can_print
        child_can_print.acquire()
        for i in range(0, 5):
            print ("hello from child %d" %self.myid)
        num_children_done += 1
        if num_children_done == num_children:
            parent_can_print.release()
        child_can_print.release()

class Parent(Thread):
    def __init__(self):
        Thread.__init__(self)
    
    def run(self):
        global num_children
        global parent_can_print
        for i in range(0,num_children):
            c = Child(i)
            c.start()
        parent_can_print.acquire()
        print("All children done!")

p = Parent()
p.start()
