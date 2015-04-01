import numpy as np
import scipy.optimize as opt

#Some variables
cost = np.array([1.800, 0.433, 0.180])
p = np.array([0.480, 0.080, 0.020])
e = np.array([0.744, 0.800, 0.142])

#Our function
fun = lambda x: np.sum(x*cost)

#Our conditions
cond = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 100},
        {'type': 'ineq', 'fun': lambda x: np.sum(p*x) - 24},
        {'type': 'ineq', 'fun': lambda x: np.sum(e*x) - 76},
        {'type': 'ineq', 'fun': lambda x: -1*x[2] + 2})


bnds = ((0,100),(0,100),(0,100))
guess = [20,30,50]
print opt.minimize(fun, guess, method='SLSQP', bounds=bnds, constraints = cond)

#Some variables
cost = np.array([1.800, 0.433, 0.180])
p = np.array([0.480, 0.080, 0.020])
e = np.array([0.744, 0.800, 0.142])

#Our function
fun = lambda x: np.sum(x*cost)

#Our conditions
cond = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 100},
        {'type': 'ineq', 'fun': lambda x: np.sum(p*x) - 24},
        {'type': 'ineq', 'fun': lambda x: np.sum(e*x) - 76},
        {'type': 'ineq', 'fun': lambda x: -1*x[2] + 2})


bnds = ((0,100),(0,100),(0,100))
guess = [20,30,50]
print opt.minimize(fun, guess, method='SLSQP', bounds=bnds, constraints = cond)

# _C1: - q + x_sw <= 0
# _C10: - x_s0w - x_sw + x_wt = 0
# _C11: - x_s0v + x_vt = -0.5
# _C2: - 3 q + x_s0s <= 0
# _C3: - q + x_s0w <= 0
# _C4: - 2 q + x_s0v <= 0
# _C5: - q + x_wt <= 0
# _C6: - 2 q + x_vt <= 0
# _C7: - x_s0s + x_sw = -2
# _C8: x_s0s + x_s0v + x_s0w = 5.5
# _C9: - x_vt - x_wt = -3

size = 7
cost = np.zeros(size)
cost[0] =1.0

#Our function
fun = lambda x: np.sum(x*cost)
