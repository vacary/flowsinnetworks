
import sys
import time
from numpy import *

# range

tstart = time.time()

#total = 0
for i in range(9999999): i**2
#    total = total + i 
#print 'sum:'+str(total)
tend = time.time() - tstart
print 'tend:'+str(tend)

# xrange

tstart = time.time()

#total = 0
for i in xrange(9999999): i**2
#    total = total + i 
#print 'sum:'+str(total)
tend = time.time() - tstart
print 'tend:'+str(tend)

# arange

tstart = time.time()

#total = 0
for i in arange(9999999): i**2
#    total = total + i
#print 'sum:'+str(total)
tend = time.time() - tstart
print 'tend:'+str(tend)

# while

tstart = time.time()

#total = 0
i = 0
while i < 9999999: 
    i**2
    i = i + 1
#    total = total + i
#print 'sum:'+str(total)
tend = time.time() - tstart
print 'tend:'+str(tend)

