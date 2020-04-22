#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 11:17:58 2019

@author: gauravsharma
"""

# =============================================================================
# https://smt.readthedocs.io/en/latest/_src_docs/sampling_methods/lhs.html
# https://github.com/tisimst/pyDOE/blob/master/pyDOE/doe_lhs.py
# https://pypi.org/project/pyDOE/
# https://www.statisticshowto.datasciencecentral.com/latin-hypercube-sampling/
# =============================================================================
import numpy as np
import matplotlib.pyplot as plt
from smt.sampling_methods import LHS  #surrogate modeling toolbox

# number of customers considered in the system
NUM_CUSTOMERS = 50

#A 3-factor design
maxmin_range = np.array([[12.0, 18.0], [4.5, 6.0],[25.0,34.0]])
sampling = LHS(xlimits=maxmin_range)

#Generating count of samples/runs to be taken
runs_count = NUM_CUSTOMERS
runs = sampling(runs_count)

print(runs.shape)

BV_harv = runs[:, 0] #Blood volume harvesting
CC_harv = runs[:, 1] #coagulant concentration
Third = runs[:, 2]  #3rd predictor

# =============================================================================
#plt.plot(BV_harv, CC_harv, "o" , markersize=5, color="red")
#plt.xlabel("BV_harv")
#plt.ylabel("CC_harv")
#plt.show()
#plt.clf()
# =============================================================================

# =============================================================================
# # Plotting more than one axes
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter3D(BV_harv, CC_harv, Third, cmap='red')
ax.set_xlabel('BV_harv')
ax.set_ylabel('CC_harv')
ax.set_zlabel('Third');
# =============================================================================
