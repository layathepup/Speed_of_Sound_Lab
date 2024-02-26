# quantum aware heat capacity

from math import *
from scipy import constants as consts

def j_to_cm(j):
    return j / (consts.c * consts.h * 100)


N_mass = 28.020 / (consts.Avogadro*1000)
C_mass = 12.011 / (consts.Avogadro*1000)
O_mass = 15.999 / (consts.Avogadro*1000)

CO_dist = 116.2 * pow(10, -12)# pm
NN_dist = 109 * pow(10, -12)

I_C02 = 2*O_mass*pow(CO_dist,2)
I_N2 = 2*N_mass*pow(NN_dist/2,2)

CO2_ep = pow(consts.hbar,2) / (2*I_C02)
N2_ep = pow(consts.hbar,2) / (2*I_N2)

print(2*j_to_cm(CO2_ep))
print(2*j_to_cm(N2_ep))
