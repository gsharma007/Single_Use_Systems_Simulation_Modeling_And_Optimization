#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 15:39:35 2019

@author: gauravsharma
"""


import numpy as np
NUM_PATIENTS = 50


""" full factorial design_genertion """

import pyDOE2

levels = [3, 3, 4]

design = pyDOE2.fullfact(levels)

NUM_MACHINES_MFG = []

for i in design[:,0]:
    if i == 0:
        MACHINES_MFG = round(NUM_PATIENTS/5)
    elif i == 1:
        MACHINES_MFG = round(NUM_PATIENTS/2)
    else:
        MACHINES_MFG = round(2* NUM_PATIENTS/3)
    NUM_MACHINES_MFG.append(MACHINES_MFG)

print(NUM_MACHINES_MFG)
    
NUM_OPERATORS_MFG = []  
for i in design[:,1]:
    if i == 0:
        OPERATOR_MFG = round(NUM_PATIENTS/5)
    elif i == 1:
        OPERATOR_MFG = round(NUM_PATIENTS/10)
    else:
        OPERATOR_MFG = round(NUM_PATIENTS/20)
    NUM_OPERATORS_MFG.append(OPERATOR_MFG)

print(NUM_OPERATORS_MFG)

Product_mix_MFG = []
for i in design[:,2]:
    if i == 0:
        Product_mix = 1
    elif i == 1:
        Product_mix = 2
    elif i == 2:
        Product_mix = 3
    else:
        Product_mix = 4
    Product_mix_MFG.append(Product_mix)
print(Product_mix_MFG)

final_design = np.array((NUM_MACHINES_MFG, NUM_OPERATORS_MFG, Product_mix_MFG), dtype=float)
final_design = np.transpose(final_design)

# =============================================================================
# mfg_machines = ["5","10","15"]
# mfg_operators = ["5","2","3"]
# product_mix = ["b","tu","tl","ttl"]
# 
# full_factorial_combinations = itertools.product(mfg_machines, mfg_operators, product_mix)
# =============================================================================




