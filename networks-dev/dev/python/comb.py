import math

def nCr(n,r):
    f = math.factorial
    return f(n) / f(r) / f(n-r)

if __name__ == '__main__':
    print 2*nCr(600,2)