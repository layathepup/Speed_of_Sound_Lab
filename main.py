import math
import itertools
import numpy as np
import scipy as sp
import csv
import molmass
import uncertainties.core

from scipy import constants as phys_const
from uncertainties.umath import *
from uncertainties import ufloat as uf

temp = 21.1 + phys_const.zero_Celsius
tube = 1.70


# FWHM = 2sqrt(2ln2)sigma


def read_csv(file_path: str) -> list:
    reader_val = csv.reader(open(file_path), delimiter=',');
    next(reader_val)  # skip header row
    reader_err = reader_val

    ret = []
    for vals, errs in zip(reader_val, reader_err):
        uflts = []
        for val, err in zip(vals[1:], errs[1:]):  # skip header column
            uflts.append(uf(float(val), float(err) / 2.35597))  # convert to stddev
        ret.append(uflts)
    return ret


def sound_speed(freq: float, n: int, l: float):
    return freq * 2 * l / n


def gamma(speed, mm, t):
    return pow(speed, 2) * mm * 0.001 / (phys_const.R * t)


class Measures:
    def __init__(self, frequencies, n, formula):
        self.n = n
        self.formula = formula

        self.frequencies = frequencies
        self.sound_speed = [[sound_speed(freq, index + n, tube) for index, freq in enumerate(trial)]
                            for trial in self.frequencies]
        self.gamma = [[gamma(speed, molmass.Formula(self.formula).mass, temp) for speed in trial]
                      for trial in self.sound_speed]


def stddev_of_error(values_with_err: list[uncertainties.core.Variable]):
    vals = []
    errs = []
    for uflt in values_with_err:
        vals.append(uflt.nominal_value)
        errs.append(uflt.std_dev)

    mean = np.nanmean(vals)
    sm = 0
    for val, err in zip(vals, errs):
        sm += math.pow(val - mean, 2) + math.pow(err, 2)
    ret = math.sqrt(sm/len(vals))
    return ret


Co2 = read_csv('dat/Co2.csv')
N2 = read_csv('dat/N2.csv')
He = read_csv('dat/He.csv')

data = {'C02': Measures(Co2, 1, 'CO2'),
        'N2': Measures(N2, 1, 'N2'),
        'He': Measures(He, 1, 'He')}

print("Gamma")
for name, species in data.items():
    print(name, ':', end=' '),
    gam_uflts = [entry for trial in species.gamma for entry in trial]
    gam_vals = [uflt.nominal_value for uflt in gam_uflts]
    print(np.nanmean(gam_vals), np.std(gam_vals))  # arith mean, but ignores NaNs

print("Gamma?")
for name, species in data.items():
    print(name, ':', end=' '),
    print(stddev_of_error([entry for trial in species.gamma for entry in trial]))

for name, species in data.items():
    print(name)
    print(species.sound_speed[0])

var = uf(1, 1)
print(type(var))