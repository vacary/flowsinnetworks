import numpy as np
import matplotlib.pyplot as plt
from scipy.special import binom

def Bernstein(n, k):
    """Bernstein polynomial.

    """
    coeff = binom(n, k)

    def _bpoly(x):
        return coeff * x ** k * (1 - x) ** (n - k)

    return _bpoly


def Bezier(points, num=20):
    """Build Bezier curve from points.

    """
    N = len(points)
    t = np.linspace(0, 1, num=num)
    curve = np.zeros((num, 2))
    for ii in range(N):
        curve += np.outer(Bernstein(N - 1, ii)(t), points[ii])
    return curve

xp = np.array([2,3,4,5])
yp = np.array([2,1,4,0])
x, y = Bezier(list(zip(xp, yp))).T

plt.plot(x,y)
plt.plot(xp,yp,"ro")
plt.plot(xp,yp,"b--")

plt.show()