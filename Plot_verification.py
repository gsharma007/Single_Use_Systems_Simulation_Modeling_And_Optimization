#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 11:45:56 2019

@author: gauravsharma
"""

NUM_CUSTOMERS = 500
NUM_OPERATOR = 200

import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

setup_times = np.random.exponential(scale=0.5, size=NUM_OPERATOR)

plt.figure()
sns.set(color_codes=True)
sns.distplot(setup_times,hist=False, rug=True)

plt.figure()
plt.hist(setup_times)
plt.title('setup_times')
plt.show()
plt.clf()


Arrivals = np.random.lognormal(mean=0.6, sigma=0.3, size=NUM_CUSTOMERS)
Arrival_times = [np.sum(Arrivals[:n]) for n in range(0, len(Arrivals))]

plt.figure()
sns.set(color_codes=True)
sns.distplot(Arrivals,hist=False, rug=True)

plt.figure()
plt.hist(Arrivals)
plt.title('Arrivals')
plt.show()
plt.clf()

