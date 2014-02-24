#!/usr/bin/env python

import os
import matplotlib
matplotlib.use('Agg')
from pylab import *

#xlabel('xlabel')
#ylabel('ylabel')
x = [1,2,3,4,5,6]
y = [2,5,4,6,8,7]
plt.plot(x,y)

filename = "/tmp/output.png"
plt.savefig(os.getcwd() + filename)


print "Content-type: text/html\n"
print "<html><body>"
print """<img src="%s" alt="graph">""" % filename
print "</body></html>"
