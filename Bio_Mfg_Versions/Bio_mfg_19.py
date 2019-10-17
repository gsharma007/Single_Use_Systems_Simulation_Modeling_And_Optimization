#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 17:20:07 2019

@author: gauravsharma
"""

"""calculating t_low, t_up for each patient"""

import random
import numpy as np
#import matplotlib.pyplot as plt
import pandas as pd

#Defining number of patients in one experiment

NUM_PATIENTS = 50

    
""" full factorial design_genertion """

import pyDOE2




def main_call(mfg_machine, mfg_operator, product_mix,run):
    
    
    """caluclating target blood count for each patient"""
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
    df = pd.DataFrame()
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
    
    #print("Target Blood Count : \n", patients_target_bc)
    df['Target_Blood_Count(Y_bar)'] = patients_target_bc
    
    
    """ system simulation for havesting"""
        
    # fixing seed for testing purpose
    # np.random.seed(26)
    
    # Time between arrivals drawn from log-normal dist
    # which its mean (exp(mu + sigma^2)) equals 2 hours
    Arrivals = np.random.lognormal(mean=0.6, sigma=0.3, size=NUM_PATIENTS)
    Arrival_times = [np.sum(Arrivals[:n]) for n in range(0, len(Arrivals))]
    
    """
    1ST STEP: (HARVESTING)
    """
    # number of operator for setting up machines
    NUM_OPERATOR = 10
    
    # number of machines for servicing customers
    NUM_MACHINES = 20
    
    # Each operator has unique setup time for each customer
    # drawn from exponential dist with rate of 0.5 hours/30 minutes
    setup_times = np.random.exponential(scale=0.5, size=NUM_OPERATOR)
    
    # Each machine has unique Service times for each customer
    # drawn from triangular dist between 3.75 and 4.25 hours
    # with  mode and mean at 4 hour
    service_times_harvesting = np.random.triangular(left=3.75, mode=4, right=4.25, size=NUM_MACHINES)
    
    
    operators = []  #list of all operators with their characteristics
    machines=[]     #list of all machines with their characteristics
    counter=0       #used to indicate operator's index
    for e in setup_times:
        dict_opt = {
            "Name": "O_"+str(counter),
            "setup_time": e,
            "ready_time": 0
        }
        operators.append(dict_opt)   #appending the operator's characteristics dictionraies in one list
        counter = counter+1          #ensuring increment in operator's index
    
    counter=0      #used to indicate machine's index
    for x in service_times_harvesting:
        dict_machine={
            "Name":"M_"+str(counter),
            "service_time":x,
            "ready_time":0
        }
        machines.append(dict_machine) #appending the machine's characteristics dictionraies in one list
        counter= counter+1            #ensuring increment in machine's index
    
    # =============================================================================
    # print(operators)      #final list of operators with their decision values
    # print(machines)       #final list of machines with their decision values
    # =============================================================================
    
    harv_operator_allocation = []
    harv_setup_times = []
    harv_machine_allocation = []
    harv_service_times = []
    harv_wait_time = []
    harv_total_time = []
    
    for patient in Arrival_times:
        wait_time = 0
        temp_o = operators[0]
        for opt in operators:
            if(opt["ready_time"]<=temp_o["ready_time"]):
                if(opt["setup_time"]<=temp_o["setup_time"]):
                    temp_o = opt
    
        temp_m = machines[0]
        for mac in machines:
            if(mac["ready_time"]<=temp_m["ready_time"]):
                if(mac["service_time"]<=temp_m["service_time"]):
                    temp_m = mac
                    
    # =============================================================================
    #     print("temp_o : ", temp_o)
    #     print("temp_m : ", temp_m)
    # =============================================================================
        
        harv_operator_allocation.append(temp_o["Name"])
        harv_setup_times.append(temp_o["setup_time"])
        harv_machine_allocation.append(temp_m["Name"])
        harv_service_times.append(temp_m["service_time"])
        
        if(patient>=temp_o["ready_time"] and patient>=temp_m["ready_time"]):
            total_time = temp_o["setup_time"]+temp_m["service_time"] + patient
        
        else:
            wait_time = max(temp_m["ready_time"], temp_o["ready_time"])-patient
            total_time = wait_time + patient + temp_o["setup_time"]+temp_m["service_time"] + patient
    
        for opt in operators:
            if(temp_o["Name"]==opt["Name"]):
                opt["ready_time"] =wait_time + opt["setup_time"]
    
        for mac in machines:
            if(temp_m["Name"]==mac["Name"]):
                mac["ready_time"] = total_time
                
        harv_wait_time.append(wait_time)
        harv_total_time.append(total_time-patient)
        
    # =============================================================================
    #     print("patient time : ", patient)
    #     print("patient total Time : " , total_time-patient)
    #     print("Operators",operators)
    #     print("Machines", machines)
    #     print("wait time :",wait_time)
    # =============================================================================
    
    #print("Clinic_arrival_times : \n" , Arrival_times)
    #print("Harv_operator_allocation:", harv_operator_allocation)
    #print("Harv_setup_times : \n" , harv_setup_times)
    #print("Harv_machine_allocation : \n", harv_machine_allocation)
    #print("Harv service times : \n" , harv_service_times)
    #print("Harv_wait_times : \n" , harv_wait_time)
    #print("Harv_total_times: \n" , harv_total_time)
      
    
    harv_Departure_times = []
    for n in range(NUM_PATIENTS):
        harv_Departure_times.append(Arrival_times[n] + harv_total_time[n])
     
    #print("Harv_Departure_times : \n", harv_Departure_times)    
    
    
    df['Arrvial_times'] = Arrival_times
    df['Harv_operator_allocation'] = harv_operator_allocation
    df['Harv_setup_times'] = harv_setup_times
    df['harv_machine_allocation'] = harv_machine_allocation
    df['harv_service_times'] = harv_service_times
    df['Harv_wait_times'] = harv_wait_time
    df['Harv_total_times'] = harv_total_time
    df['Harv_Departure_times'] = harv_Departure_times
    
    #achieved yield after harvesting
    df['Yield_after_harvesting'] = 0.85 * df['Target_Blood_Count(Y_bar)']
    
    
    """ system simulation for cryopreservation"""
    
    #considering machines are always available for cryopreservation
    
    cryo_arrivals = harv_Departure_times
    #print("Cryo_arrivals : \n", cryo_arrivals)
    cryo_service_times = np.random.uniform(low = 0.25, high = 0.5, size=NUM_PATIENTS)
    #print("Cryo_service_times : \n", cryo_service_times)
    cryo_departure_times = cryo_arrivals + cryo_service_times 
    #print("Cryo_departure_times : \n", cryo_departure_times)
    cryo_total_time = cryo_departure_times - cryo_arrivals
    
    df['cryo_arrivals'] = cryo_arrivals
    df['Cryo_service_times'] = cryo_service_times
    df['Cryo_departure_times'] = cryo_departure_times
    df['cryo_total_time'] = cryo_total_time    
    
    #achieved yield after cryo
    beta = 100
    df['achvd_yield_after_cryo'] = df['Yield_after_harvesting']-beta* df['cryo_total_time']  
    
    
    """ system simulation for transportation"""
    
    #considering vehicles are always available for transportation and batch processing is not considered
    
    tnsprt_start = cryo_departure_times
    #print("Clinic_departure_time : \n", tnsprt_start)
    tnsprt_times = np.random.triangular(left=9, mode=12, right=15, size=NUM_PATIENTS)
    #print("Transit_transportation_time : \n", tnsprt_times)
    mfg_arrival_times = tnsprt_start + tnsprt_times
    #print("Mfg_arrival_time : \n", mfg_arrival_times)
    
    df['Clinic_departure_time'] = tnsprt_start
    df['Transit_transportation_time'] = tnsprt_times
    
    #achieved_yield_before_mfg
    zeta = 25
    df['achvd_yield_before_mfg'] = df['achvd_yield_after_cryo'] -  zeta*df['Transit_transportation_time']
    
    #expected yield after mfg
    df['exp_yield_after_mfg'] = 0.90 * df['Target_Blood_Count(Y_bar)']
    df['diff_bw_current_&_exp'] = df['exp_yield_after_mfg'] - df['achvd_yield_before_mfg']
    
    achvd_yield_before_mfg = df['achvd_yield_before_mfg']
    
    """calculating t_low, t_up for each patient"""
    
    alpha_low = 100000 
    alpha_up = 4000
    
    t_low = []
    for j in achvd_yield_before_mfg:
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
    
    
    df['Mfg_arrival_time'] = mfg_arrival_times
    
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
    
    
    """ system simulation for manufacturing"""
    
    # =============================================================================
    # # number of operators for setting up machines during mfg
    NUM_OPERATOR_MFG = int(mfg_operator)
    # 
    # # number of machines for servicing customers during mfg
    NUM_MACHINES_MFG =int(mfg_machine)
    #print("Machine Value",NUM_MACHINES_MFG)
    
    # Each operator has unique setup time for each customer
    # drawn from exponential dist with rate of 0.5 hours/30 minutes
    mfg_setup_times = np.random.exponential(scale=0.5, size=NUM_OPERATOR_MFG)
    
    # Each machine has unique Service times for each customer
    # drawn from triangular dist between 3.75 and 4.25 hours
    # with  mode and mean at 4 hour
    mfg_service_times = np.random.triangular(left=168, mode=264, right=384, size=NUM_MACHINES_MFG)
    
    
    
    mfg_operators = []  #list of all operators with their characteristics
    mfg_machines = []     #list of all machines with their characteristics
    mfg_counter = 0       #used to indicate operator's index
    for e in mfg_setup_times:
        dict_opt = {
            "Name": "O_"+str(mfg_counter),
            "mfg_setup_time": e,
            "mfg_ready_time": 0
        }
        mfg_operators.append(dict_opt)   #appending the operator's characteristics dictionraies in one list
        mfg_counter = mfg_counter+1          #ensuring increment in operator's index
    
    mfg_counter=0      #used to indicate machine's index
    for x in mfg_service_times:
        dict_machine={
            "Name":"M_"+str(mfg_counter),
            "mfg_service_time":x,
            "mfg_ready_time":0
        }
        mfg_machines.append(dict_machine) #appending the machine's characteristics dictionraies in one list
        mfg_counter= mfg_counter+1            #ensuring increment in machine's index
    
    # =============================================================================
    # print(operators)      #final list of operators with their decision values
    # print(machines)       #final list of machines with their decision values
    # =============================================================================
    
    mfg_operator_allocation = []
    mfg_setup_times = []
    mfg_machine_allocation = []
    mfg_service_times = []
    mfg_sample_wait_time = []
    mfg_sample_total_time = []
    
    for patient in mfg_arrival_times:
        mfg_wait_time = 0
        mfg_temp_o = mfg_operators[0]
        for opt in mfg_operators:
            if(opt["mfg_ready_time"]<=mfg_temp_o["mfg_ready_time"]):
                if(opt["mfg_setup_time"]<=mfg_temp_o["mfg_setup_time"]):
                    mfg_temp_o = opt
    
        mfg_temp_m = mfg_machines[0]
        for mac in mfg_machines:
            if(mac["mfg_ready_time"]<=mfg_temp_m["mfg_ready_time"]):
                if(mac["mfg_service_time"]<=mfg_temp_m["mfg_service_time"]):
                    mfg_temp_m = mac
                    
    #    print("mfg_temp_o : \n", mfg_temp_o)
    #    print("mfg_temp_m : \n", mfg_temp_m)
    
        
        mfg_operator_allocation.append(mfg_temp_o["Name"])
        mfg_setup_times.append(mfg_temp_o["mfg_setup_time"])
        mfg_machine_allocation.append(mfg_temp_m["Name"])
        mfg_service_times.append(mfg_temp_m["mfg_service_time"])
    
        
        if(patient>=mfg_temp_o["mfg_ready_time"] and patient>=mfg_temp_m["mfg_ready_time"]):
            mfg_total_time = mfg_temp_o["mfg_setup_time"]+mfg_temp_m["mfg_service_time"] + patient
        
        else:
            mfg_wait_time = max(mfg_temp_m["mfg_ready_time"], mfg_temp_o["mfg_ready_time"])-patient
            mfg_total_time = mfg_wait_time + patient + mfg_temp_o["mfg_setup_time"]+mfg_temp_m["mfg_service_time"] + patient
    
        for opt in mfg_operators:
            if(mfg_temp_o["Name"]==opt["Name"]):
                opt["mfg_ready_time"] =mfg_wait_time + opt["mfg_setup_time"]
    
        for mac in mfg_machines:
            if(mfg_temp_m["Name"]==mac["Name"]):
                mac["mfg_ready_time"] = mfg_total_time
                
        mfg_sample_wait_time.append(mfg_wait_time)
        mfg_sample_total_time.append(mfg_total_time)
        
    # =============================================================================
    #     print("patient time : ", patient)
    #     print("patient total Time : " , total_time-patient)
    #     print("Operators",operators)
    #     print("Machines", machines)
    #     print("wait time :",wait_time)
    # =============================================================================
    
#    print("MFG_operator_allocation:", mfg_operator_allocation)
#    print("MFG_setup_times : \n" , mfg_setup_times)
#    print("MFG_machine_allocation : \n", mfg_machine_allocation)
#    print("MFG_service times : \n" , mfg_service_times)
#    print("MFG_wait_times : \n" ,mfg_sample_wait_time)
#    print("MFG_total_times: \n" , mfg_sample_total_time)
    
    df['MFG_operator_allocation'] = mfg_operator_allocation
    df['MFG_setup_times'] = mfg_setup_times
    df['MFG_machine_allocation'] = mfg_machine_allocation
    df['MFG_service times'] = mfg_service_times
    df['MFG_wait_times'] = mfg_sample_wait_time
    df['MFG_total_times'] = mfg_sample_total_time
   
    mfg_Departure_times = []
    for n in range(NUM_PATIENTS):
        mfg_Departure_times.append(mfg_arrival_times[n] + mfg_sample_total_time[n])
    
    
    """ system simulation for transportation back to clinic """
    
    #considering vehicles are always available for transportation and batch processing is not considered
    
    
    back_tnsprt_start = mfg_Departure_times
    #print("Clinic_back_departure_time(hours) : \n", back_tnsprt_start)
    back_tnsprt_times = np.random.triangular(left=9, mode=12, right=15, size=NUM_PATIENTS)
    #print("Transit_back_transportation_time(hours) : \n", back_tnsprt_times)
    clinic_end_arrival_times = back_tnsprt_start + back_tnsprt_times
    #print("Clinic_arrival_time_end(hours) : \n", clinic_end_arrival_times)
    
    Overall_process_time = (clinic_end_arrival_times-Arrival_times)/24
    #print("Overall_process_time(days) : \n", Overall_process_time)
    
    df['Clinic_back_departure_time(hours)'] = back_tnsprt_start
    df['Transit_back_transportation_time(hours)'] = back_tnsprt_times
    df['Clinic_arrival_time_end(hours)'] = clinic_end_arrival_times
    df['Overall_process_time(days)'] = Overall_process_time
    
    #different between actual and achieved yield
    df['diff_exp_achvd_yield_mfg'] = df['Achieved_Yield_from_Mfg'] - df['exp_yield_after_mfg']
    return df


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
        df = main_call(x[0],x[1],x[2],run)
        #function1()
        df['run'] = run
        df['config: product_mix '] =x[2]
        df_consol = df_consol.append(df)
    return df_consol

    
#df_consol.to_excel(r'/Users/gauravsharma/Documents/Simulation_results_2.xls')