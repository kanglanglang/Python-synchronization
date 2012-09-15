from __future__ import with_statement
from threading import Thread, Lock, Condition, Semaphore

# a. When both threads terminate, what is the largest possible value
#    count may have?

# 10000

# b. When both threads terminate, what is the smallest possible value
#    count may have?

# -10000

# c. What other values can can count have when both threads have 
#    terminated?

# Any number in the range -10000 to 10000

# d. Add appropriate synchronization such that updates to count
#    occur in a critical section, ensuring that the count is 
#    always at 0 when the two threads terminate.

count = 0
count_sema = Semaphore(1)
class Worker1(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        global count
        for i in range(0, 10000):
            count_sema.acquire()
            count += 1
            count_sema.release()

class Worker2(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        global count
        for j in range(0, 10000):
            count_sema.acquire()
            count -= 1
            count_sema.release()

w1 = Worker1()
w2 = Worker2()
w1.start()
w2.start()
