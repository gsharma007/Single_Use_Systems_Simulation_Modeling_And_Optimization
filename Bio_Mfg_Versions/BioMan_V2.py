#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 14:46:11 2020

@author: gauravsharma
"""


#installing required libraries
import pandas as pd
import numpy as np
import pyDOE2
import random

NUM_PATIENTS = 50    #number of patients to be considered in the system

#Generating patient related information

df = pd.DataFrame()  #initializing a dataframe


#Factor 1- Yield curve component- Two levels
#Yield_Curve_Type 1 shows stressed system
#Yield_Curve_Type 2 shows system with slow growth rate

def yield_curve_level(Yield_Curve_MFG,patients_target_bc):

    if Yield_Curve_MFG == 1:

        #defining characteristics for yield curve 1 (Stressed System)
        #Relaxed alpha low, less delta t, and high alpha up

        alpha_low_mfg = 100000 
        alpha_up_mfg = 4000

        t_low_mfg = []
        for j in range(NUM_PATIENTS):
            t_low_mfg.append(j/alpha_low_mfg)

        delta_t_mfg = 5

        t_up_mfg = []
        for k in t_low_mfg:
            t_up_mfg.append(k+delta_t_mfg)
        #print("t_up : \n", t_up)

        low_level_factor_mfg = 0.90
        up_level_factor_mfg = 1.10


        t_low_new_mfg = []
        for t1 in t_low_mfg:
            t_low_new_mfg.append(t1*low_level_factor_mfg)
        #print("t_low_new : \n", t_low_new)

        t_up_new_mfg = []
        for t2 in t_up_mfg:
            t_up_new_mfg.append(t2*up_level_factor_mfg)
        #print("t_up_new : \n", t_up_new)

        t_normal_mfg = []
        for a in range(NUM_PATIENTS):
            t_normal_mfg.append((t_up_new_mfg[a]+t_low_new_mfg[a])/2)


    else:

        #defining characteristics for yield curve 2 (relaxed system)
        #Sharp alpha low, more delta t, and relaxed alpha up

        alpha_low_mfg = 50000 
        alpha_up_mfg = 20000

        t_low_mfg = []
        for j in range(NUM_PATIENTS):
            t_low_mfg.append(j/alpha_low_mfg)

        delta_t_mfg = 15

        t_up_mfg = []
        for k in t_low_mfg:
            t_up_mfg.append(k+delta_t_mfg)
        #print("t_up : \n", t_up)

        low_level_factor_mfg = 0.90
        up_level_factor_mfg = 1.10


        t_low_new_mfg = []
        for t1 in t_low_mfg:
            t_low_new_mfg.append(t1*low_level_factor_mfg)
        #print("t_low_new : \n", t_low_new)

        t_up_new_mfg = []
        for t2 in t_up_mfg:
            t_up_new_mfg.append(t2*up_level_factor_mfg)
        #print("t_up_new : \n", t_up_new)

        t_normal_mfg = []
        for a in range(NUM_PATIENTS):
            t_normal_mfg.append((t_up_new_mfg[a]+t_low_new_mfg[a])/2)

    df['t_low_new_mfg'] = t_low_new_mfg
    df['t_normal_mfg'] = t_normal_mfg
    df['t_up_new_mfg'] = t_up_new_mfg

    time_level_patients_mfg = np.array((t_low_new_mfg, t_normal_mfg, t_up_new_mfg), dtype=float)
    time_level_patients_mfg = np.transpose(time_level_patients_mfg)

    y1_mfg = alpha_low_mfg * (time_level_patients_mfg[:,0])
    y2_mfg = patients_target_bc
    y3_mfg = patients_target_bc - alpha_up_mfg*(time_level_patients_mfg[:,2])
    
    df['y1_mfg'] = y1_mfg
    df['y2_mfg'] = y2_mfg
    df['y3_mfg'] = y3_mfg

    yield_mfg = np.array((y1_mfg,y2_mfg,y3_mfg))
    yield_mfg = np.transpose(yield_mfg)
    
    return time_level_patients_mfg, yield_mfg


#(time_level_patients_mfg,yield_mfg) = yield_curve_level(Yield_Curve_MFG)


#Factor 2- Patient Component- Two Levels
#Level 1 shows mix of patients with 80% Average response, 10 % Good and 10% Bad response
#Level 2 shows mix of patients with 50% Average response, 25 % Good and 25% Bad response

#time_selected_mfg = []
#yield_selected_mfg = []

def Patient_Mix(Patient_Mix_MFG,time_level_patients_mfg,yield_mfg):
    
    sel_value_list_mfg =[]
    for z in range(NUM_PATIENTS):

        if Patient_Mix_MFG == 1:
            s = np.random.uniform(0, 1)
            if (s <= 0.10):
                sel_value_mfg = 0
            elif (0.10 < s <= 0.90):
                sel_value_mfg = 1
            else:
                sel_value_mfg = 2
        if Patient_Mix_MFG == 2:
            s = np.random.uniform(0, 1)
            if (s <= 0.25):
                sel_value_mfg = 0
            elif (0.25 < s <= 0.50):
                sel_value_mfg = 1
            else:
                sel_value_mfg = 2

        sel_value_list_mfg.append(sel_value_mfg)
        
    time_selected_mfg = [time_level_patients_mfg[z,i] for z,i in zip(range(NUM_PATIENTS),sel_value_list_mfg)]
    yield_selected_mfg = [yield_mfg[z,i] for z,i in zip(range(NUM_PATIENTS),sel_value_list_mfg)]

    df['time_selected_mfg'] = time_selected_mfg
    df['Achieved_Yield_from_mfg'] = yield_selected_mfg
    return time_selected_mfg, yield_selected_mfg




#Factor 3- Quality control policy related to tests with 3 levels
#Level 1 shows the policy where every test is conducted in high fidelity
#Level 2 shows the policy where every test is conducted in low fidelity and if test fails, a second high fidelity test is conducted
#Level 3 Shows the policy where we test in high fidelity with some testing probability 

def high_fidelity_test_case_A():
    
    P_1_HF = 0.99   #P(Ytilda >= Y* / Y' >= Y*) #P(viable/Test = Positive)
    P_2_HF = 0.10   #P(Ytilda >= Y* / Y' < Y*)  #P(viable/Test = Negative)
    P_3_HF = 0.65   #P(Y' >= Y*) #P(Measured Yield < Expected Yield)

    #calculating P(Y'>= Y* / Ytilda>= Y*) 
    #i.e. proability of measured yield being more than expected yield given calculated yield is more than expected
    #P(Y'>= Y* / Ytilda>= Y*)  = P(Ytilda >= Y* / Y' >= Y*) * P(Y' >= Y*) / [P(Ytilda >= Y* / Y' >= Y*) * P(Y' >= Y*) + P(Ytilda >= Y* / Y' < Y*) * P(Y' < Y*)]
    alpha_HF = (P_1_HF * P_3_HF) / (P_1_HF * P_3_HF + P_2_HF * (1 - P_3_HF))

    U1 = np.random.uniform(0, 1)

    if (U1 <= alpha_HF):
        Test_Result = "Sample Passed"
    else:
        Test_Result = "Sample Rejected"
    return Test_Result
        
def high_fidelity_test_case_B():
    
    P_1_HF = 0.99   #P(Ytilda >= Y* / Y' >= Y*) #P(viable/Test = Positive)
    P_2_HF = 0.10   #P(Ytilda >= Y* / Y' < Y*)  #P(viable/Test = Negative)
    P_3_HF = 0.65   #P(Y' >= Y*) #P(Measured Yield < Expected Yield)

    Beta_HF = ((1-P_1_HF)* P_3_HF) / (((1-P_1_HF)* P_3_HF) + ((1-P_2_HF)*(1-P_3_HF)))

    U2 = np.random.uniform(0, 1)

    if (U2 <= Beta_HF):
        Test_Result = "Sample Passed"    #It was fail, but Test confirms Pass
    else:
        Test_Result = "Sample Rejected"  #It was fail, Test Confirms Fail
    return Test_Result

def low_fidelity_test_case_A():
    
    P_1_LF = 0.85   #P(Ytilda >= Y* / Y' >= Y*) #P(viable/Test = Positive)
    P_2_LF = 0.45   #P(Ytilda >= Y* / Y' < Y*)  #P(viable/Test = Negative)
    P_3_LF = 0.40   #P(Y' >= Y*) #P(Measured Yield < Expected Yield)

    #calculating P(Y'>= Y* / Ytilda < Y*)

    alpha_LF = (P_1_LF * P_3_LF) / (P_1_LF * P_3_LF + P_2_LF * (1 - P_3_LF))

    U3 = np.random.uniform(0, 1)

    if (U3 <= alpha_LF):
        Test_Result = "Sample Passed"
    else:
        Test_Result = "Sample Rejected"
    return Test_Result

def low_fidelity_test_case_B():
    
    P_1_LF = 0.85   #P(Ytilda >= Y* / Y' >= Y*) #P(viable/Test = Positive)
    P_2_LF = 0.45   #P(Ytilda >= Y* / Y' < Y*)  #P(viable/Test = Negative)
    P_3_LF = 0.40   #P(Y' >= Y*) #P(Measured Yield < Expected Yield)

    Beta_LF = ((1-P_1_LF)* P_3_LF) / (((1-P_1_LF)* P_3_LF) + ((1-P_2_LF)*(1-P_3_LF)))

    U4 = np.random.uniform(0, 1)

    if (U4 <= Beta_LF):
        Test_Result = "Sample Passed"    #It was fail, but Test confirms Pass
    else:
        Test_Result = "Sample Rejected"  #It was fail, Test Confirms Fail    
    return Test_Result

def quality_policy(QM_Policy_MFG, yield_selected_mfg,patients_target_bc):

    #defining level for each quality control policy
    #Test happens according to that level and the results are recorded
    Test_Outcomes_MFG = []
    Test_Result=""
    for z in range(NUM_PATIENTS):

        if QM_Policy_MFG == 1:

            #test everything in high fidelity

            #Case A
            if (yield_selected_mfg > patients_target_bc):
                Test_Result=high_fidelity_test_case_A()
            #Case B
            else:
                Test_Result=high_fidelity_test_case_B()


        elif QM_Policy_MFG == 2:

            #test everything in low fidelity and if test fails then check again in high fidelity

            #Case A
            if (yield_selected_mfg > patients_target_bc):
                Test_Result = low_fidelity_test_case_A()
                
                if Test_Result == "Sample Rejected":
                    Test_Result = high_fidelity_test_case_A()
                    if Test_Result == "Sample Rejected":
                        Test_Result = "Rejected in Both"
                    else:
                        Test_Result = "Rejected in LF, Passed in HF"

            #Case B
            else:
                Test_Result= low_fidelity_test_case_B()

                if Test_Result == "Sample Rejected":
                    Test_Result = high_fidelity_test_case_B()
                    if Test_Result == "Sample Rejected":
                        Test_Result = "Rejected in Both"
                    else:
                        Test_Result = "Rejected in LF, Passed in HF"
                        
        else:

            U5 = np.random.uniform(0, 1)

            if (U5 <= 0.70):

                if (yield_selected_mfg > patients_target_bc):
                    Test_Result=high_fidelity_test_case_A()
                else:
                    Test_Result=high_fidelity_test_case_B()

            else:
                Test_Result= "Proceeding Sample without contamination"

        Test_Outcomes_MFG.append(Test_Result)

    return Test_Outcomes_MFG


""" Resource allocation for manufacturing"""

def Resource_allocation(MFG_Operators_Count, MFG_Bioreactors_Count, time_selected_mfg):

    Arrivals = np.random.lognormal(mean=0.6, sigma=0.3, size=NUM_PATIENTS)
    mfg_arrival_times = [np.sum(Arrivals[:n]) for n in range(0, len(Arrivals))]
    
    df['Arrivals'] = Arrivals
    df['Arrival times'] = mfg_arrival_times
    
    # =============================================================================
        # # number of operators for setting up machines during mfg
    NUM_OPERATOR_MFG = int(MFG_Operators_Count)
    
    # # number of machines for servicing customers during mfg
    NUM_MACHINES_MFG =int(MFG_Bioreactors_Count)
    #print("Machine Value",NUM_MACHINES_MFG)
    
    # Each operator has unique setup time for each customer
    # drawn from exponential dist with rate of 0.5 hours/30 minutes
    mfg_setup_times = np.random.exponential(scale=0.5, size=NUM_OPERATOR_MFG)
    
    # Each machine has unique Service times for each customer
    mfg_service_times = time_selected_mfg
    
    df['MFG_service times'] = mfg_service_times
    
    #Allocation Logic
    
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
   
    df['MFG_setup_times'] = mfg_setup_times
    df['MFG_operator_allocation'] = mfg_operator_allocation
    df['MFG_machine_allocation'] = mfg_machine_allocation
    df['MFG_wait_times'] = mfg_sample_wait_time
    df['MFG_total_times'] = mfg_sample_total_time
       
    mfg_Departure_times = []
    for n in range(NUM_PATIENTS):
        mfg_Departure_times.append(mfg_arrival_times[n] + mfg_sample_total_time[n])
        
    df['Mfg_Departure_times'] = mfg_Departure_times
    
    return df

def simulation_design():
    
    levels = [2, 2, 3, 3, 3]
    design = pyDOE2.fullfact(levels)
    
    #Factor 1 corresponds to Yield Curve Component having two levels
    #Yield_Curve_Type 1 shows stressed system
    #Yield_Curve_Type 2 shows system with slow growth rate
    
    Yield_Curve_MFG = []
    for i in design[:,0]:
        if i == 0:
            Yield_Curve_Type = 1
        else:
            Yield_Curve_Type = 2
        Yield_Curve_MFG.append(Yield_Curve_Type)
    
    
    #Factor 2 corresponds to Patient component having two levels
    #Level 1 shows mix of patients with 80% Average response, 10 % Good and 10% Bad response
    #Level 2 shows mix of patients with 50% Average response, 25 % Good and 25% Bad response
        
    Patient_Mix_MFG = []
    
    for i in design[:,1]:
        if i == 0:
            Patient_Mix_Policy = 1
        else:
            Patient_Mix_Policy = 2
        Patient_Mix_MFG.append(Patient_Mix_Policy)
        
    #Factor 3 corresponds to Quality control policy related to tests with 3 levels
    #Level 1 shows the policy where every test is conducted in high fidelity
    #Level 2 shows the policy where every test is conducted in low fidelity and if test fails, a second high fidelity test is conducted
    #Level 3 Shows the policy where we test in high fidelity with some testing probability    
        
    QM_Policy_MFG = []
    
    for i in design[:,2]:
        if i == 0:
            Quality_Policy = 1
        elif i == 1:
            Quality_Policy = 2
        else:
            Quality_Policy = 3
        QM_Policy_MFG.append(Quality_Policy)
        
    #Factor 4 corresponds to the Mfg operators count
        
    NUM_OPERATORS_MFG = []
      
    for i in design[:,4]:
        if i == 0:
            OPERATOR_MFG = round(NUM_PATIENTS/5)
        elif i == 1:
            OPERATOR_MFG = round(NUM_PATIENTS/10)
        else:
            OPERATOR_MFG = round(NUM_PATIENTS/20)
        NUM_OPERATORS_MFG.append(OPERATOR_MFG)
    
    #Factor 5 corresponds to the available Mfg machines(bio-reactors) count
    
    NUM_MACHINES_MFG = []
    
    for i in design[:,3]:
    
        if i == 0:
            MACHINES_MFG = round(NUM_PATIENTS/2)
        elif i == 1:
            MACHINES_MFG = round(NUM_PATIENTS/5)
        else:
            MACHINES_MFG = round(2* NUM_PATIENTS/10)
        NUM_MACHINES_MFG.append(MACHINES_MFG)
    
    
    final_design = np.array((Yield_Curve_MFG, Patient_Mix_MFG, QM_Policy_MFG, NUM_OPERATORS_MFG, NUM_MACHINES_MFG), dtype=float)
    final_design = np.transpose(final_design)
    
    return final_design

final_design = simulation_design()

def Consolidated(Yield_Curve_MFG, Patient_Mix_MFG, QM_Policy_MFG, MFG_Operators_Count, MFG_Bioreactors_Count):
    
    #assigning gender to each patient
    patientGender = []
    for amount in range(NUM_PATIENTS):
        flip = random.randint(0, 1)
        if (flip == 0):
            patientGender.append("Male")
        else:
            patientGender.append("Female")
                    
    df['Patient_Gender'] = patientGender
    
    #calculating blood volume of each patient based on the gender
    patients_BV = []
    for person in patientGender:
        if (person == 'Male'):
            BV = np.random.uniform(low = 5, high = 7.5) 
            patients_BV.append(BV)
        else:
            BV = np.random.uniform(low = 3.5, high = 6.0)
            patients_BV.append(BV)
            
    df['Patients_Blood_Volume'] = patients_BV
    
    #conversion factor to calculate the target blood count required in therapy
    #target blood count depends on each patient's blood volume
    CF = 140000
    
    patients_target_bc = []
    for i in patients_BV:
        patients_target_bc.append(i*CF)
        
    df['Target_Blood_Count(Y_bar)'] = patients_target_bc
    
    #yield_curve_level(Yield_Curve_MFG)
    (time_level_patients_mfg,yield_mfg) = yield_curve_level(Yield_Curve_MFG,patients_target_bc)
    
    #Patient_Mix(Patient_Mix_MFG)
    (time_selected_mfg, yield_selected_mfg) = Patient_Mix(Patient_Mix_MFG,time_level_patients_mfg,yield_mfg)
    
    #quality_policy(QM_Policy_MFG)
    Test_Outcomes_MFG = quality_policy(QM_Policy_MFG, yield_selected_mfg,patients_target_bc)
    df['Test_Outcomes_MFG'] = Test_Outcomes_MFG
    
    Resource_allocation(MFG_Operators_Count, MFG_Bioreactors_Count, time_selected_mfg)
    return df

    

def Simulation_run():
    df_consol = pd.DataFrame()
    
    run =0  
    for x in final_design:
        run+=1
        df = Consolidated(x[0],x[1],x[2],x[3],x[4])
        #function1()
        #print(type(df)) 
        df['run'] = run
        df['Yield_Curve_MFG'] = x[0]
        df['Patient_Mix_MFG'] = x[1]
        df['QM_Policy_MFG'] = x[2]
        df['NUM_OPERATORS_MFG'] = x[3]
        df['NUM_MACHINES_MFG'] = x[4]
        df_consol = df_consol.append(df)
    return df_consol     