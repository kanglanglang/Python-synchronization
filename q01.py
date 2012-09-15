from __future__ import with_statement
from threading import Thread, Lock, Condition, Semaphore

# a. Run the following concurrent program. Are there any particular
#    patterns in the output? Is the interleaving of the output from 
#    the two threads predictable in any way?

# The outputs cycle back and forth. It is very predictable.

# b. If the answer to part (a) is affirmative, run the same program
#    while browsing the web. Does the pattern you outlined in section
#    (a) hold?

# The pattern does not hold. It is mostly alternating but sometimes a
# thread repeats

# c. In general, can one rely on a particular timing/interleaving of 
#    executions of concurrent processes?

# No, since the the execution of concurrent processes is highly unpredictable.

# d. Given that there are no synchronization operations in the code
#    below, any interleaving of executions should be possible. When
#    you run the code, do you believe that you see a large fraction
#    of the possible interleavings? If so, what do you think makes
#    this possible? If not, what does this imply about the 
#    effectiveness of testing as a way to find synchronization 
#    errors?

# I think there is much more possible interleaving that we are not seeing.
# This would imply that testing to find synchronization errors is almost
# pointless

class Worker1(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            print ("Hello from Worker 1")

class Worker2(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            print ("Hello from Worker 2")

w1 = Worker1()
w2 = Worker2()
w1.start()
w2.start()
