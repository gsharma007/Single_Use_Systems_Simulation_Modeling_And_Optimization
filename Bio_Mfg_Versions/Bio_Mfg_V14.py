#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 9 00:34:32 2019

@author: gauravsharma
"""

import random
import numpy as np
import matplotlib.pyplot as plt
# import pandas as pd


#Defining number of patients in one experiment

NUM_PATIENTS = 50


"""cointoss to assign each patient a count to categorize them as male or female"""

# =============================================================================   
# from random import randint
# flips = [randint(0,1) for r in range(NUM_CUSTOMERS)]
# results = []
# for object in flips:
#         if object == 0:
#             results.append('Heads')
#         elif object == 1:
#             results.append('Tails')
# print (results)
# =============================================================================

patientGender = []
for amount in range(NUM_PATIENTS):
    flip = random.randint(0, 1)
    if (flip == 0):
        patientGender.append("Male")
    else:
        patientGender.append("Female")
 
print(patientGender)
print("Percent Male Patients: ", patientGender.count("Male")/NUM_PATIENTS)
print("percent Female Patients: ",patientGender.count("Female")/NUM_PATIENTS)


"""generating blood volume from uniform distribution based on the gender of the patient"""

patients_BV = []
for person in patientGender:
    if (person == 'Male'):
        BV = np.random.uniform(low = 5, high = 7.5) 
        patients_BV.append(BV)
    else:
        BV = np.random.uniform(low = 3, high = 5.5)
        patients_BV.append(BV)
    
print("Patients Blood Volume : ", patients_BV)
        
# =============================================================================
# https://docs.scipy.org/doc/numpy-1.15.0/reference/generated/numpy.random.uniform.html
# https://www.journalnow.com/archives/science---blood-volume-relates-to-height-weight-gender/article_2809b77a-cfa3-513b-9a5b-d5a9de54e58d.html
# Nadler's Formula:
# For Males = 0.3669 * Ht in M3 + 0.03219 * Wt in kgs + 0.6041
# For Females = 0.3561 * Ht in M3 + 0.03308 x Wt in kgs + 0.1833
# Note:
# * Ht in M = Height in Meters, which is then cubed
# * Wt in kgs = Body weight in kilograms
# =============================================================================

"""calculating target blood cell count for each patient"""

CF = 140000
  
# =============================================================================
# df = pd.Series(patients_BV)
# df_converted = df*CF
# patients_target_bc = df_converted.tolist()
# print(patients_target_bc) 
# =============================================================================

patients_target_bc = []
for i in patients_BV:
    patients_target_bc.append(i*CF)

print("Target Blood Count : ", patients_target_bc)


"""calculating t_low, t_up for each patient"""


alpha_low = 200000 
alpha_up = 100000

t_low = []
for j in patients_target_bc:
    t_low.append(j/alpha_low)
    
print("t_low : ", t_low)

delta_t = 2.5

t_up = []
for k in t_low:
    t_up.append(k+delta_t)
print("t_up : ", t_up)


""" Now calculating t_low_new, t_normal and t_up_new for all"""


low_level_factor = 0.9
up_level_factor = 1.1

t_low_new = []
for t1 in t_low:
    t_low_new.append(t1*low_level_factor)
print("t_low_new : ", t_low_new)

t_up_new = []
for t2 in t_up:
    t_up_new.append(t2*up_level_factor)
print("t_up_new : ", t_up_new)

t_normal = []
for a in range(NUM_PATIENTS):
    t_normal.append((t_up_new[a]+t_low_new[a])/2)
print("t_normal : ", t_normal)  


"""calculating yield(y_hat) for each patient at all three time levels i.e. slow,normal and fast processing"""

time_level_patients = np.array((t_low_new, t_normal, t_up_new), dtype=float)
time_level_patients = np.transpose(time_level_patients)

# yield_harvesting = np.zeros((NUM_PATIENTS,3))    #this will create problem in automating

y1 = alpha_low * (time_level_patients[:,0])
y2 = patients_target_bc
y3 = patients_target_bc - alpha_up*(time_level_patients[:,2])

yield_harvesting = np.array((y1,y2,y3))
yield_harvesting = np.transpose(yield_harvesting)
print ("Harvesting Yield For Patient : ", yield_harvesting)

plt.scatter(time_level_patients[:2],yield_harvesting[:2])
plt.show()
plt.clf()