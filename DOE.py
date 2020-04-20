#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 05:56:04 2020

@author: gauravsharma
"""


#import random
import numpy as np
#import matplotlib.pyplot as plt
#import pandas as pd
import pyDOE2

NUM_PATIENTS = 50

levels = [3, 3, 4, 3, 3, 4]

design = pyDOE2.fullfact(levels)


NUM_OPERATORS_HRV = []
  
for i in design[:,1]:
    if i == 0:
        OPERATOR_HRV = round(NUM_PATIENTS/15)
    elif i == 1:
        OPERATOR_HRV = round(NUM_PATIENTS/25)
    else:
        OPERATOR_HRV = round(NUM_PATIENTS/35)
    NUM_OPERATORS_HRV.append(OPERATOR_HRV)

NUM_MACHINES_HRV = []

for i in design[:,0]:

    if i == 0:
        MACHINES_HRV = round(NUM_PATIENTS/10)
    elif i == 1:
        MACHINES_HRV = round(NUM_PATIENTS/20)
    else:
        MACHINES_HRV = round(2* NUM_PATIENTS/30)
    NUM_MACHINES_HRV.append(MACHINES_HRV)

Product_mix_HRV = []

for i in design[:,2]:
    if i == 0:
        Product_mix_1 = 1
    elif i == 1:
        Product_mix_1 = 2
    elif i == 2:
        Product_mix_1 = 3
    else:
        Product_mix_1 = 4
    Product_mix_HRV.append(Product_mix_1)

    
NUM_OPERATORS_MFG = []
  
for i in design[:,4]:
    if i == 0:
        OPERATOR_MFG = round(NUM_PATIENTS/5)
    elif i == 1:
        OPERATOR_MFG = round(NUM_PATIENTS/10)
    else:
        OPERATOR_MFG = round(NUM_PATIENTS/20)
    NUM_OPERATORS_MFG.append(OPERATOR_MFG)

NUM_MACHINES_MFG = []

for i in design[:,3]:

    if i == 0:
        MACHINES_MFG = round(NUM_PATIENTS/2)
    elif i == 1:
        MACHINES_MFG = round(NUM_PATIENTS/5)
    else:
        MACHINES_MFG = round(2* NUM_PATIENTS/10)
    NUM_MACHINES_MFG.append(MACHINES_MFG)

Product_mix_MFG = []

for i in design[:,5]:
    if i == 0:
        Product_mix_2 = 1
    elif i == 1:
        Product_mix_2 = 2
    elif i == 2:
        Product_mix_2 = 3
    else:
        Product_mix_2 = 4
    Product_mix_MFG.append(Product_mix_2)

final_design = np.array((NUM_OPERATORS_HRV, NUM_MACHINES_HRV, Product_mix_HRV, NUM_OPERATORS_MFG, NUM_MACHINES_MFG, Product_mix_MFG), dtype=float)
final_design = np.transpose(final_design)

print(final_design.head)