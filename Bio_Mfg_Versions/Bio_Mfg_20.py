#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 03 10:55:30 2020

@author: gauravsharma
"""


import random
import numpy as np
import pandas as pd
import pyDOE2

"""calculating t_low, t_up for each patient in Harvesting"""

#Defining number of patients in one experiment
NUM_PATIENTS = 50

df = pd.DataFrame()

def main_call(mfg_machine, mfg_operator, product_mix):


    """caluclating target blood count for each patient"""
    """cointoss to assign each patient a count to categorize them as male or female"""
    
    patientGender = []
    for amount in range(NUM_PATIENTS):
        flip = random.randint(0, 1)
        if (flip == 0):
            patientGender.append("Male")
        else:
            patientGender.append("Female")
     
    #print(patientGender)
    #print("Percent Male Patients: \n", patientGender.count("Male")/NUM_PATIENTS)
    #print("percent Female Patients: \n",patientGender.count("Female")/NUM_PATIENTS)
    
    df['Patient_Gender'] = patientGender
    
    """generating blood volume from uniform distribution based on the gender of the patient"""
    
    patients_BV = []
    for person in patientGender:
        if (person == 'Male'):
            BV = np.random.uniform(low = 5, high = 7.5) 
            patients_BV.append(BV)
        else:
            BV = np.random.uniform(low = 3.5, high = 6.0)
            patients_BV.append(BV)
        
    #print("Patients Blood Volume : \n", patients_BV)
    
    df['Patients_Blood_Volume'] = patients_BV
    
    """calculating target blood cell count for each patient"""
    
    CF = 140000
    
    patients_target_bc = []
    for i in patients_BV:
        patients_target_bc.append(i*CF)
        
    #print("Target Blood Count : \n", patients_target_bc)
    df['Target_Blood_Count(Y_bar)'] = patients_target_bc


    """calculating t_low, t_up for each patient"""
    
    alpha_low = 100000 
    alpha_up = 4000
    
    t_low = []
    for j in patients_target_bc:
        t_low.append(j/alpha_low)
        
    #print("t_low : \n", t_low)
    
    delta_t = 5
    
    t_up = []
    for k in t_low:
        t_up.append(k+delta_t)
    #print("t_up : \n", t_up)
        
    """ Now calculating t_low_new, t_normal and t_up_new for all"""
    
    low_level_factor = 0.90
    up_level_factor = 1.10
    
    t_low_new = []
    for t1 in t_low:
        t_low_new.append(t1*low_level_factor)
    #print("t_low_new : \n", t_low_new)
    
    t_up_new = []
    for t2 in t_up:
        t_up_new.append(t2*up_level_factor)
    #print("t_up_new : \n", t_up_new)
    
    t_normal = []
    for a in range(NUM_PATIENTS):
        t_normal.append((t_up_new[a]+t_low_new[a])/2)
    #print("t_normal : \n", t_normal)
        
    
    """calculating yield(y_hat) for each patient at all three time levels i.e. slow,normal and fast processing"""
    
    time_level_patients = np.array((t_low_new, t_normal, t_up_new), dtype=float)
    time_level_patients = np.transpose(time_level_patients)
    
    # yield_harvesting = np.zeros((NUM_PATIENTS,3))    #this will create problem in automating
    
    y1 = alpha_low * (time_level_patients[:,0])
    y2 = patients_target_bc
    y3 = patients_target_bc - alpha_up*(time_level_patients[:,2])
    
    yield_mfg = np.array((y1,y2,y3))
    yield_mfg = np.transpose(yield_mfg)
    #print ("Achieved_Yield_Mfg : \n", yield_mfg)

    """Product Mix Random Allocation"""


    sel_value_list =[]
    for z in range(NUM_PATIENTS):
        if product_mix == 1:
            sel_value = random.choice([0,1,2])
            
        if product_mix == 2:
            s = np.random.uniform(0, 1)
            if (s <= 0.15):
               sel_value = 0
            elif (0.15 < s <= 0.85):
                sel_value = 1
            else:
                sel_value = 2
        if product_mix == 3:
            s = np.random.uniform(0, 1)
            if (s <= 0.70):
                sel_value = 0
            elif (0.70 < s <= 0.85):
                sel_value = 1
            else:
                sel_value = 2
        if product_mix == 4:
            s = np.random.uniform(0, 1)
            if (s <= 0.15):
                sel_value = 0
            elif (0.15 < s <= 0.30):
                sel_value = 1
            else:
                sel_value = 2
        
        sel_value_list.append(sel_value)
        
    time_selected = [time_level_patients[z,i] for z,i in zip(range(NUM_PATIENTS),sel_value_list)]
    yield_mfg_selected = [yield_mfg[z,i] for z,i in zip(range(NUM_PATIENTS),sel_value_list)]
    #print("Selected index:",sel_value_list)
    #print("time_selected",time_selected)
    #print("Yield",yield_mfg_selected)
    
    df['time_selected'] = time_selected
    df['Achieved_Yield_from_Mfg'] = yield_mfg_selected


""" Experimental Design """
    
def function_2():
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
    
    #initializing a dataframe
    
    df_consol = pd.DataFrame()
    run =0 
    for x in final_design:
        run+=1
        df = main_call(x[0],x[1],x[2])
        #function1()
        df['run'] = run
        df['Machine_Count'] = x[0]
        df['Operators_Count'] = x[1]
        df['Product_mix'] =x[2]
        df_consol = df_consol.append(df)
    return df_consol