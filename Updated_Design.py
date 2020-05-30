#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 05:56:04 2020

@author: gauravsharma
"""


import numpy as np
import pyDOE2
import pandas as pd
#import random
#import matplotlib.pyplot as plt

NUM_PATIENTS = 50

#full factorial design for 7 factors
levels = [2, 2, 3, 3, 3, 3, 3]
design = pyDOE2.fullfact(levels)

#Factor 1 corresponds to Yield Curve Component having two levels
#Yield_Curve_Type 1 shows stressed system
#Yield_Curve_Type 2 shows system with slow growth rate

Yield_Curve = []
for i in design[:,0]:
    if i == 0:
        Yield_Curve_Type = 1
    else:
        Yield_Curve_Type = 2
    Yield_Curve.append(Yield_Curve_Type)


#Factor 2 corresponds to Patient component having two levels
#Level 1 shows mix of patients with 80% Average response, 10 % Good and 10% Bad response
#Level 2 shows mix of patients with 50% Average response, 25 % Good and 25% Bad response
    
Patient_Mix = []

for i in design[:,1]:
    if i == 0:
        Patient_Mix_Policy = 1
    else:
        Patient_Mix_Policy = 2
    Patient_Mix.append(Patient_Mix_Policy)
    
#Factor 3 corresponds to Quality control policy related to tests with 3 levels
#Level 1 shows the policy where every test is conducted in high fidelity
#Level 2 shows the policy where every test is conducted in low fidelity and if test fails, a second high fidelity test is conducted
#Level 3 Shows the policy where we test in high fidelity with some testing probability    
    
QM_Policy = []

for i in design[:,2]:
    if i == 0:
        Quality_Policy = 1
    elif i == 1:
        Quality_Policy = 2
    else:
        Quality_Policy = 3
    QM_Policy.append(Quality_Policy)
    
#Factor 4 corresponds to the harvesting operators count

NUM_OPERATORS_HRV = []
  
for i in design[:,1]:
    if i == 0:
        OPERATOR_HRV = round(NUM_PATIENTS/15)
    elif i == 1:
        OPERATOR_HRV = round(NUM_PATIENTS/25)
    else:
        OPERATOR_HRV = round(NUM_PATIENTS/35)
    NUM_OPERATORS_HRV.append(OPERATOR_HRV)
    
#Factor 5 corresponds to the available harvesting machines count

NUM_MACHINES_HRV = []

for i in design[:,0]:
    if i == 0:
        MACHINES_HRV = round(NUM_PATIENTS/10)
    elif i == 1:
        MACHINES_HRV = round(NUM_PATIENTS/20)
    else:
        MACHINES_HRV = round(2* NUM_PATIENTS/30)
    NUM_MACHINES_HRV.append(MACHINES_HRV)
    
#Factor 6 corresponds to the Mfg operators count
    
NUM_OPERATORS_MFG = []
  
for i in design[:,4]:
    if i == 0:
        OPERATOR_MFG = round(NUM_PATIENTS/5)
    elif i == 1:
        OPERATOR_MFG = round(NUM_PATIENTS/10)
    else:
        OPERATOR_MFG = round(NUM_PATIENTS/20)
    NUM_OPERATORS_MFG.append(OPERATOR_MFG)

#Factor 7 corresponds to the available Mfg machines(bio-reactors) count

NUM_MACHINES_MFG = []

for i in design[:,3]:

    if i == 0:
        MACHINES_MFG = round(NUM_PATIENTS/2)
    elif i == 1:
        MACHINES_MFG = round(NUM_PATIENTS/5)
    else:
        MACHINES_MFG = round(NUM_PATIENTS)
    NUM_MACHINES_MFG.append(MACHINES_MFG)


final_design = np.array((Yield_Curve, Patient_Mix, QM_Policy, NUM_OPERATORS_HRV, NUM_MACHINES_HRV, NUM_OPERATORS_MFG, NUM_MACHINES_MFG), dtype=float)
final_design = np.transpose(final_design)
Design_df = pd.DataFrame(data=final_design, columns=["Yield_Curve", "Patient_Mix", "QM_Policy", "NUM_OPERATORS_HRV", "NUM_MACHINES_HRV", "NUM_OPERATORS_MFG", "NUM_MACHINES_MFG"])
Design_df.reset_index(drop=True)

print(final_design)
Design_df.to_csv(r'/Users/gauravsharma/Documents/Updated_Design.csv')