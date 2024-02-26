from math import *
from scipy import constants as consts

def aten_vib(x):
    term1 = pow(x/2, 2)
    term2 = 1 / pow(sinh(x/2), 2)
    return term1 * term2

def thaw_vib(ep, t):
    x = consts.k * t / (ep * 100 * consts.h * consts.c)
    return aten_vib(x)

def cm_from_x(x, t):
    e = consts.k * t * x
    return e / (consts.h * consts.c * 100)

def approx_val(targ, func, mn, mx, err, corr=1):
    if not corr: mx, mn = mn, mx
    mid = (mx+mn)/2 + mn
    res = func(mid)
    while abs(res - targ) > err:
        if res > targ:
            mn = mid
            mid = (mx - mn) / 2 + mn
            res = func(mid)
        elif res < targ:
            mx = mid
            mid = (mx - mn) / 2 + mn
            res = func(mid)
    return mid



#print(cm_from_x(0.222, 300))
#print(cm_from_x(5.76, 300))

#print(cm_from_x(4.939, 300))
#print(cm_from_x(0.941, 300))

#print(thaw_vib(526, 300))


val = (approx_val(0.99, aten_vib, 0,100, 0.0001, corr = -1))
print(val, aten_vib(val), cm_from_x(val, 300))