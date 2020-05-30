#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 23 05:33:55 2020

@author: gauravsharma
"""


#installing required libraries
import pandas as pd
import numpy as np
import pyDOE2
import random

NUM_PATIENTS =50   #number of patients to be considered in the system

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
        for j in patients_target_bc:
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

        alpha_low_mfg =  85000
        alpha_up_mfg = 20000

        t_low_mfg = []
        for j in patients_target_bc:
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


    df['t_low_mfg'] = t_low_mfg
    df['t_up_mfg'] = t_up_mfg
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

    time_selected_mfg_hours = [element * 24 for element in time_selected_mfg]

    df['time_selected_mfg (days)'] = time_selected_mfg
    df['time_selected_mfg (hours)'] = time_selected_mfg_hours
    df['Achieved_Yield_from_mfg'] = yield_selected_mfg
    return time_selected_mfg_hours, yield_selected_mfg

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

def quality_policy(QM_Policy_MFG, yield_selected_mfg,patients_target_bc, val):

    #defining level for each quality control policy
    #Test happens according to that level and the results are recorded
    index = val["Pat_no"]
    
    Test_Result=""

    if QM_Policy_MFG == 1:

        #test everything in high fidelity

        #Case A
        if (yield_selected_mfg[index] < patients_target_bc[index]):
            Test_Result=high_fidelity_test_case_A()
        #Case B
        else:
            Test_Result=high_fidelity_test_case_B()

# =============================================================================
#         #test
#         #Case A    
#         if (yield_selected_mfg > patients_target_bc):
#             Test_Result=high_fidelity_test_case_B()
#         #Case B
#         else:
#             Test_Result=high_fidelity_test_case_A()
# =============================================================================


    elif QM_Policy_MFG == 2:

        #test everything in low fidelity and if test fails then check again in high fidelity


        #Case A
        if (yield_selected_mfg[index] < patients_target_bc[index]):
            Test_Result = low_fidelity_test_case_A()
            
            if Test_Result == "Sample Rejected":
                Test_Result = high_fidelity_test_case_A()
                if Test_Result == "Sample Rejected":
                    Test_Result = "Rejected in LF and HF Both"
                else:
                    Test_Result = "Rejected in LF but Passed in HF"

        #Case B
        else:
            Test_Result= low_fidelity_test_case_B()

            if Test_Result == "Sample Rejected":
                Test_Result = high_fidelity_test_case_B()
                if Test_Result == "Sample Rejected":
                    Test_Result = "Rejected in LF and HF Both"
                else:
                    Test_Result = "Rejected in LF, Passed in HF"

# =============================================================================
#                     
#         #test            
#         #Case A
#         if (yield_selected_mfg > patients_target_bc):
#             Test_Result = low_fidelity_test_case_B()
#             
#             if Test_Result == "Sample Rejected":
#                 Test_Result = high_fidelity_test_case_B()
#                 if Test_Result == "Sample Rejected":
#                     Test_Result = "Rejected in LF and HF Both"
#                 else:
#                     Test_Result = "Rejected in LF but Passed in HF"
# 
#         #Case B
#         else:
#             Test_Result= low_fidelity_test_case_A()
# 
#             if Test_Result == "Sample Rejected":
#                 Test_Result = high_fidelity_test_case_A()
#                 if Test_Result == "Sample Rejected":
#                     Test_Result = "Rejected in LF and HF Both"
#                 else:
#                     Test_Result = "Rejected in LF, Passed in HF"
# =============================================================================
                    
    else:

        U5 = np.random.uniform(0, 1)

        if (U5 <= 0.70):

            if (yield_selected_mfg[index] < patients_target_bc[index]):
                Test_Result=high_fidelity_test_case_A()
            else:
                Test_Result=high_fidelity_test_case_B()

        else:
            Test_Result= "Proceeding Sample without contamination"

    return Test_Result

""" Resource allocation for harvesting"""

def Hrv_Resource_allocation(Hrv_Operators_Count, Hrv_Bioreactors_Count):

    setup_time = np.random.randint(1, 3, size=NUM_PATIENTS)
    # len(setup_time)
    
    Inter_Arrivals = np.random.randint(4, 10, size=NUM_PATIENTS)
    arrival_times = [np.sum(Inter_Arrivals[:n]) for n in range(1, len(Inter_Arrivals)+1)]
    #arrival_times = np.around(arrival_times)
    
    service_time = np.random.randint(6,9, size=NUM_PATIENTS)
    
    #Resource Count
    
    Num_Operators = int(Hrv_Operators_Count)
    Num_Machines = int(Hrv_Bioreactors_Count)
    
    #Initialization
    
    clock =0
    setup_depart = [0]*Num_Operators
    depart_time = [0]*Num_Machines
    queue_level = 0
    Event_Num = 0
    Event_calendar = []
    departures = []
    service_queue = []
    Queue_track = []
    results = []
    num_in_service = 0
    B_t = []
    
    def handle_arrival_event(queue_level):
        
        # print("min_depart_time:", min(depart_time))
        # print("min_setup_depart:", min(setup_depart))
        # print("Entering_1")
        # print("clock_now:", clock)
        
        index = arrival_times.index(clock)
        #print("index_value:", index)
        
        if(clock >=min(depart_time) and clock >= min(setup_depart)  and len(service_queue)==0):
            
            #setup_time = np.random.randint(25,38)
            #setup_times.append(setup_time)
            
            # print("Entering_1A")
            setup_index = setup_depart.index(min(setup_depart))
            # print("setup_index:", setup_index)
            depart_index = depart_time.index(min(depart_time))
            # print("depart_index:",depart_index)
            setup_depart[setup_index] = clock + setup_time[index]
            depart_time[depart_index] =  setup_depart[setup_index] + service_time[index]
            # print("This is setup_depart time:",setup_depart)
            # print("This is depart Time:",depart_time)
            
            Event_info = {"Patient": "P"+str(index), "Event_time" : clock, 
                          "Event_Type" : "Arrival and Service Start", 
                          "Setup_finish" : setup_depart[setup_index],
                          "Departure" : depart_time[depart_index]}
            
            # print("Event_info\n:", Event_info)
            Event_calendar.append(Event_info)
            
            results.append(Event_info)
            
            Queue_track.append(queue_level)
            
            # num_in_service += 1
            # B_t.append(num_in_service)
            
            #departures.append(depart_time)
            
            # U = np.random.uniform(0,1)
            # print("U_value", U)
            # if U > 0.5:
            #     print("sample passes and depart time as it is")
            # else:
            #     bisect.insort(arrival_times, depart_time[depart_index])
                
            
        else:
            # print("Entering_1B")
            service_queue.append(index)
            # print("Service_Queue:", service_queue)
            queue_level = len(service_queue)
            # print("queue_level:", queue_level)
            
            Queue_track.append(queue_level)
            
            B_t.append(num_in_service)
            
            Event_info = {"Patient": "P"+str(index), "Event_time" : clock, 
                          "Event_Type" : "Arrival and in Queue"}
            # print("Event_info:\n", Event_info)
            Event_calendar.append(Event_info)
    
    def handle_departure_event():
        
        #setup_time = np.random.randint(25, 38)
        #setup_times.append(setup_time)
        
        # print("clock_now:", clock)
        
        # print("min_depart_time:", min(depart_time))
        # print("min_setup_depart:", min(setup_depart))
        
        # print("Entering_2")
        index = service_queue.pop(0)
        
        queue_level = len(service_queue)
        # print("queue_level:", queue_level)
        
        Queue_track.append(queue_level)
        
        # print("service_queue:", service_queue)
        # print("index:", index)
        
        setup_index = setup_depart.index(min(setup_depart))
        # print("setup_index:", setup_index)
        depart_index = depart_time.index(min(depart_time))
        # print("depart_index:",depart_index)
        setup_depart[setup_index] = clock + setup_time[index]
        depart_time[depart_index] =  setup_depart[setup_index] + service_time[index]
        # print("This is setup_depart time:",setup_depart)
        # print("This is depart Time:",depart_time)
        
        Event_info = {"Patient": "P"+str(index), "Event_time" : clock, 
                      "Event_Type" : "Service_Start", "Setup_finish" : setup_depart[setup_index],
                      "Departure" : depart_time[depart_index]}
        print("Event_info:\n", Event_info)
        
        Event_calendar.append(Event_info)
        
        results.append(Event_info)
        
        # num_in_service += 1
        # B_t.append(num_in_service)
        
        # U = np.random.uniform(0,1)
        # print("U_value", U)
        # if U > 0.5:
        #     print("depart time as it is")
        # else:
        #     bisect.insort(arrival_times, depart_time[depart_index])
        
        #departures.append(depart_time)
    
    """Simulation"""
    
    # print(arrival_times)
    while(clock<10000):
        #print("clock:", clock)   
        
        if(clock in arrival_times):
            
            handle_arrival_event(queue_level)  
            
        if(clock>=min(depart_time) and clock >= min(setup_depart) and len(service_queue)!=0):
             
            handle_departure_event()
            
            
        clock+=1
        
    
    """Storing Results"""
    
    # print("Full_Event_Calendar:\n" , Event_calendar)
    Event_calendar = pd.DataFrame(Event_calendar)
    Event_calendar['queue'] = Queue_track
    #Event_calendar["B(t)"] = B_t
    
    df = pd.DataFrame(results)
    df["arrival_times"] = arrival_times
    df["setup_times"] = setup_time
    df["service_time"] = service_time
    df["waiting_time"]= df["Event_time"]-df["arrival_times"]
    #df["Arrival_times"] = arrival_times
    
    return df, Event_calendar

""" Resource allocation for Manufacturing"""

def Mfg_Resource_allocation(df_1, time_selected_mfg_hours, Mfg_Operators_Count, Mfg_Bioreactors_Count, QM_Policy_MFG, yield_selected_mfg, patients_target_bc):
    
    
    arrival_times = df_1["Departure"]
    arrival_times = np.around(arrival_times)
    
    service_time = time_selected_mfg_hours
    service_time = np.around(service_time)
    
    setup_time = np.random.uniform(5, 8,size=NUM_PATIENTS)
    setup_time = np.around(setup_time)
    
    #Resource Count
    
    print("Mfg_Operators_Count:", Mfg_Operators_Count)
    print("Mfg_Bioreactors_Count:", Mfg_Bioreactors_Count)
    
    Num_Operators = int(Mfg_Operators_Count)
    Num_Machines = int(Mfg_Bioreactors_Count)
    
    #Initialization
    clock =0
    setup_depart = [0]*(Num_Operators)
    depart_time = [0]*(Num_Machines)
    queue_level = 0
    Event_Num = 0
    Event_calendar = []
    departures = []
    service_queue = []
    Queue_track = []
    results = []
    num_in_service = 0
    B_t = []
    
    
    pat_data = []
    Test_time = 2
    for x in range(0,len(arrival_times)):
        temp = {}
        temp["Pat_no"] = x
        temp["Arrival_Time"] = arrival_times[x]
        temp["service_time"] = service_time[x]
        temp["setup_time"] = setup_time[x]
        pat_data.append(temp)
    
    
    while(clock<10000):
        
        # print("Clock:", clock)
        val = next((item for item in pat_data if item["Arrival_Time"] == clock), False)
        # print("val:", val)
        
        # print("min_dpeart_time", min(depart_time))
        # print("min_setup_time", min(setup_depart))
        # print("len(service_queue)",len(service_queue))
        
        if(val!=False):
            
            # print("Entering_1\n")
            
            if(clock >=min(depart_time) and clock >= min(setup_depart) and len(service_queue)==0):
                
                # print("Clock:", clock)
                
                # print("Entering_1_A\n")
                
                setup_index = setup_depart.index(min(setup_depart))
                # print("setup_index:" , setup_index)
                
                depart_index = depart_time.index(min(depart_time))
                # print("depart_index:" , depart_index)
                
                setup_depart[setup_index] = clock + val["setup_time"]
                # print("setup_depart[setup_index]", setup_depart[setup_index])
                
                depart_time[depart_index] =  setup_depart[setup_index] + val["service_time"]
                # print("depart_time[depart_index]", depart_time[depart_index])
                
                #status = bool(random.getrandbits(1))
                
# =============================================================================
#                 print("******************************")
#                 print("Setup Depart Time Array: ", setup_depart)
#                 print("Service Depart Time Array: ",depart_time)
#                 print("Patient Number: ", val["Pat_no"])
#                 print("Test Status: ",Test_Result)
#                 print("*******************************")
# =============================================================================
                
                Test_Result = quality_policy(QM_Policy_MFG, yield_selected_mfg, patients_target_bc, val)
                
                Event_info = {"Patient": val["Pat_no"], 
                              "Arrival_time": val["Arrival_Time"],
                              "Event_time" : clock, 
                              "Event_Type" : "Arrival and Service Start", 
                              "Operator": "O"+str(setup_index),
                              "Setup_time" : val["setup_time"],
                              "Bioreactor": "M"+str(depart_index),
                              "Service_time": val["service_time"],
                              "Setup_finish" : setup_depart[setup_index],
                              "Departure" : depart_time[depart_index], "Test_Reseult": Test_Result}
                
                # print("Event_info:\n", Event_info)
                
                Event_calendar.append(Event_info)
                results.append(Event_info)
                
                Queue_track.append(queue_level)
                
                if Test_Result in ("Sample Rejected","Rejected in LF and HF Both"):
                    
                    print("Adding Rework into the Arrivals")
                    
                    new_arrival = depart_time[depart_index] + Test_time
                    
                    rework_dict = {}
                    
                    rework_dict["Pat_no"] = val["Pat_no"]
                    rework_dict["Arrival_Time"] = new_arrival
                    rework_dict["service_time"] = val["service_time"]
                    rework_dict["setup_time"] = val["setup_time"]
                    
                    #val["Arrival_Time"] = depart_time[depart_index] + Test_time
                    
# =============================================================================
#                     print("***************")
#                     print("False Status")
#                     # print("Arrival Value:", val["Arrival_Time"])
#                     print("Arrival Value:", new_arrival)
#                     print("****************")
# =============================================================================
                    
                    # print("rework:", rework_dict)
                    
                    pat_data.append(rework_dict)
                    
                    # print("pat_data_updated:", pat_data)
                    
            else:
                
                # print("Clock:", clock)
                
                # print("Entering 1_B\n")
                service_queue.append(val)
                
                # print("service_queue:" , service_queue)
                
                Event_info = {"Patient": val["Pat_no"], 
                              "Arrival_time": val["Arrival_Time"],
                              "Event_time" : clock, 
                              "Event_Type" : "Arrival and in Queue"}
                
                # print("Event_info:\n", Event_info)
                
                Event_calendar.append(Event_info)
                
                queue_level = len(service_queue)
                # print("queue_level:", queue_level)
            
                Queue_track.append(queue_level)
                
        
        if(clock>=min(depart_time) and clock >= min(setup_depart) and len(service_queue)!=0):
        
            
            # print("Clock:", clock)
            # print("Entering_2\n")
            
            val = service_queue.pop(0)
            # print("val_now:", val)
            # print("service_queue:", service_queue)
            
            queue_level = len(service_queue)
            # print("queue_level:", queue_level)
        
            Queue_track.append(queue_level)
            
            setup_index = setup_depart.index(min(setup_depart))
            # print("setup_index:" , setup_index)
            
            depart_index = depart_time.index(min(depart_time))
            # print("depart_index:" , depart_index)
            
            setup_depart[setup_index] = clock +  val["setup_time"]
            # print("setup_depart[setup_index]", setup_depart[setup_index])
    
            depart_time[depart_index] =  setup_depart[setup_index] + val["service_time"]
            # print("depart_time[depart_index]", depart_time[depart_index])
            
            # val["setup_depart"] = setup_depart[setup_index]
            # val["depart_time"] = depart_time[depart_index]
            
            # print("changed_val:", val)
            
            #status = bool(random.getrandbits(1))
# =============================================================================
#             print("******************************")
#             print("Setup Depart Time Array: ", setup_depart)
#             print("Service Depart Time Array: ",depart_time)
#             print("Patient Number: ", val["Pat_no"])
#             print("Test Status: ",Test_Result)
#             print("*******************************")
# =============================================================================
            
            Test_Result = quality_policy(QM_Policy_MFG, yield_selected_mfg, patients_target_bc, val)
            
            
            Event_info = {"Patient": val["Pat_no"], "Arrival_time": val["Arrival_Time"],
                          "Event_time" : clock, "Event_Type" : "Service_Start", 
                          "Operator": "O"+str(setup_index),
                          "Setup_time" : val["setup_time"],
                          "Bioreactor": "M"+str(depart_index),
                          "Service_time": val["service_time"],
                          "Setup_finish" : setup_depart[setup_index],
                          "Departure" : depart_time[depart_index], "Test_Reseult": Test_Result}
# =============================================================================
#             print("Event_info:\n", Event_info)
# =============================================================================
            
            Event_calendar.append(Event_info)
            results.append(Event_info)
            
            if Test_Result in ("Sample Rejected","Rejected in LF and HF Both"):
                
                print("Adding Rework into the Arrivals")
                
                new_arrival = depart_time[depart_index] + Test_time
                    
                rework_dict = {}
                
                rework_dict["Pat_no"] = val["Pat_no"]
                rework_dict["Arrival_Time"] = new_arrival
                rework_dict["service_time"] = val["service_time"]
                rework_dict["setup_time"] = val["setup_time"]
                
                # val["Arrival_Time"] = depart_time[depart_index] + Test_time
                
# =============================================================================
#                 print("***************")
#                 print("False Status")
#                 # print("Arrival Value:", val["Arrival_Time"])
#                 print("Arrival Value:", new_arrival)
#                 print("****************")
# =============================================================================
                
                pat_data.append(rework_dict)
                
# =============================================================================
#                 print("pat_data_updated:", pat_data)
# =============================================================================
    
        clock+=1
        
    """Storing Results"""
    
    #print("Full_Event_Calendar:\n" , Event_calendar)
    Event_calendar = pd.DataFrame(Event_calendar)
    Event_calendar['queue'] = Queue_track
    Patient_Data = pd.DataFrame(pat_data)
    
    mfg_df = pd.DataFrame(results)
    mfg_df["waiting_time"]= mfg_df["Event_time"]-mfg_df["Arrival_time"]
        
    return mfg_df, Event_calendar

def simulation_design():
    
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
    
    
    final_design = np.array((Yield_Curve, Patient_Mix, QM_Policy, NUM_OPERATORS_HRV, 
                             NUM_MACHINES_HRV, NUM_OPERATORS_MFG, NUM_MACHINES_MFG), dtype=float)
    final_design = np.transpose(final_design)
    
    return final_design

final_design = simulation_design()

def Consolidated(Yield_Curve_MFG, Patient_Mix_MFG, QM_Policy_MFG, Hrv_Operators_Count, Hrv_Bioreactors_Count, MFG_Operators_Count, MFG_Bioreactors_Count):
    
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
    (time_selected_mfg_hours, yield_selected_mfg) = Patient_Mix(Patient_Mix_MFG,time_level_patients_mfg,yield_mfg)
    
    (df_1, Event_calendar_hrv) = Hrv_Resource_allocation(Hrv_Operators_Count, Hrv_Bioreactors_Count)
    
    #Test_Result = quality_policy(QM_Policy_MFG, yield_selected_mfg, patients_target_bc)
    
    (mfg_df, Event_calendar_mfg) = Mfg_Resource_allocation(df_1, time_selected_mfg_hours, MFG_Operators_Count, MFG_Bioreactors_Count, QM_Policy_MFG, yield_selected_mfg, patients_target_bc)
    
    # #quality_policy(QM_Policy_MFG)
    # Test_Outcomes_MFG = quality_policy(QM_Policy_MFG, yield_selected_mfg,patients_target_bc)
    # df['Test_Outcomes_MFG'] = Test_Outcomes_MFG
    
    return df_1, Event_calendar_hrv, mfg_df, Event_calendar_mfg

def Simulation_run():
    df_consol = pd.DataFrame()
    hrv_event_calendar = pd.DataFrame()
    mfg_df_consol = pd.DataFrame()
    mfg_event_calendar = pd.DataFrame()
    run =0  
    for x in final_design:
        run+=1
        (df_1, Event_calendar_hrv, mfg_df, Event_calendar_mfg) = Consolidated(x[0],x[1],x[2],x[3],x[4],x[5],x[6])
        #function1()
        #print(type(df)) 
        df_1['run'] = run
        df_1['Yield_Curve_MFG'] = x[0]
        df_1['Patient_Mix_MFG'] = x[1]
        df_1['QM_Policy_MFG'] = x[2]
        df_1['Hrv_Operators_Count'] = x[3]
        df_1['Hrv_Bioreactors_Count'] = x[4]
        df_1['MFG_Operators_Count'] = x[5]
        df_1['MFG_Bioreactors_Count'] = x[6]
        
        hrv_event_calendar['run'] = run
        mfg_df_consol['run'] = run
        mfg_event_calendar['run'] = run
        
        df_consol = df_consol.append(df_1)
        hrv_event_calendar = hrv_event_calendar.append(Event_calendar_hrv)
        mfg_df_consol = mfg_df_consol.append(mfg_df)
        mfg_event_calendar = mfg_event_calendar.append(Event_calendar_mfg)
        
    return df_consol, hrv_event_calendar, mfg_df_consol, mfg_event_calendar
