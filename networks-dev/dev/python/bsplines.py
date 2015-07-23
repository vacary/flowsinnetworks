import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate as si

points = [[-2, 2], [0, 1], [-2, 0], [0, -1], [-2, -2], [-4, -4], [2, -4], [4, 0], [2, 4], [-4, 4]]

npos = [[17.806, 8.0833, 0.0],[17.758, 7.8375, 0.0],[17.612, 6.7174, 0.0],[16.989, 2.1944, 0.0],[15.764, 2.1944, 0.0],[14.708, 2.1944, 0.0],[14.708, 2.1944, 0.0],[14.708, 2.1944, 0.0],[13.101, 2.1944, 0.0],[13.232, 0.30556, 0.0],[11.625, 0.30556, 0.0],[3.2917, 0.30556, 0.0],[3.2917, 0.30556, 0.0],[3.2917, 0.30556, 0.0],[1.4553, 0.30556, 0.0],[1.261, 3.3579, 0.0],[1.2554, 4.4752, 0.0],[1.25, 4.875, 0.0]]

points = []
for elm in npos:
    points.append([elm[0],elm[1]])

degree = 3

#points = points + points[0:degree + 1]
points = np.array(points)
n_points = len(points)
x = points[:,0]
y = points[:,1]

t = range(len(x))
ipl_t = np.linspace(1.0, len(points) - degree, 1000)

x_tup = si.splrep(t, x, k=degree, per=1)
y_tup = si.splrep(t, y, k=degree, per=1)
x_list = list(x_tup)
xl = x.tolist()
x_list[1] = [0.0] + xl + [0.0, 0.0, 0.0, 0.0]

y_list = list(y_tup)
yl = y.tolist()
y_list[1] = [0.0] + yl + [0.0, 0.0, 0.0, 0.0]

x_i = si.splev(ipl_t, x_list)
y_i = si.splev(ipl_t, y_list)

#==============================================================================
# Plot
#==============================================================================

plt.plot(x, y, '-og')
plt.plot(x_i, y_i, 'r')
plt.xlim([min(x) - 0.3, max(x) + 0.3])
plt.ylim([min(y) - 0.3, max(y) + 0.3])
plt.title('Splined f(x(t), y(t))')

plt.show()

