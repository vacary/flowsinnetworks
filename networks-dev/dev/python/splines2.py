from scipy import interpolate
import numpy as np
import matplotlib.pyplot as plt

# sampling
x = np.linspace(0, 10, 10)
y = np.sin(x)

# spline trough all the sampled points
tck = interpolate.splrep(x, y)
print tck
x2 = np.linspace(0, 10, 200)
y2 = interpolate.splev(x2, tck)

# spline with all the middle points as knots (not working yet)
knots = np.asarray(x[1:-1])  # it should be something like this
#knots = np.array([x[1]])  # not working with above line and just seeing what this line does
nknots = 5
idx_knots = (np.arange(1,len(x)-1,(len(x)-2)/np.double(nknots))).astype('int')
knots = x[idx_knots]
print knots

weights = np.concatenate(([1],np.ones(x.shape[0]-2)*.01,[1]))
tck = interpolate.splrep(x, y,  t=knots, w=weights)
x3 = np.linspace(0, 10, 200)
y3 = interpolate.splev(x2, tck)

# plot
plt.plot(x, y, 'go', x2, y2, 'b', x3, y3,'r')
plt.show()