from __future__ import with_statement
from threading import Thread, Lock, Condition, Semaphore
from os import _exit as quit
import time, random

# modify the parent thread to create a child thread, 
# wait for it to print to the screen 5 times,
# then the parent should print that the child is done.
# 
# the parent and child should use monitors and condition
# variables for synchronization

class Child(Thread):
    def __init__(self):
        Thread.__init__(self)
    
    def run(self):
        global print_monitor
        print_monitor.child_enter()
        for i in range(0, 5):
            print ("hello from child", i)
        print_monitor.child_exit()

class Parent(Thread):
    def __init__(self):
        Thread.__init__(self)
    
    def run(self):
        global print_monitor
        print("Created a child thread")
        print_monitor.parent_enter()
        print("Printed 5 times")
        print_monitor.parent_exit()
        

class Print_Monitor:
    def __init__(self):
        self.child_done = False
        self.print_lock = Lock()
        self.print_control = Condition(self.print_lock)

    def parent_enter(self):
        with self.print_lock:
            c = Child()
            c.start()
            while not self.child_done:
                self.print_control.wait()

    def parent_exit(self):
        print("Child is done")

    def child_enter(self):
        pass

    def child_exit(self):
        with self.print_lock:
            self.child_done = True
            self.print_control.notify()

print_monitor = Print_Monitor()
p = Parent()
p.start()
