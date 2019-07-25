#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 00:01:18 2019

@author: gauravsharma
"""

import numpy as np
NUM_MACHINES = 2
NUM_CUSTOMERS = 5
NUM_OPERATOR = 2

Arrivals = np.random.lognormal(mean=0.6, sigma=0.3, size=NUM_CUSTOMERS)
Arrival_times = [np.sum(Arrivals[:n]) for n in range(0, len(Arrivals))]
setup_times = np.random.exponential(scale=0.5, size=(NUM_MACHINES, NUM_CUSTOMERS))
service_times_harvesting = np.random.triangular(left=3.75, mode=4, right=4.25, size=(NUM_MACHINES, NUM_CUSTOMERS))

Waiting_time_for_service = np.zeros(NUM_CUSTOMERS)
Departure_time = np.zeros(NUM_CUSTOMERS)
customers_service_times = np.zeros(NUM_CUSTOMERS)
machine_busy_times = np.zeros(NUM_MACHINES)
operator_busy_time = np.zeros(NUM_OPERATOR)

Time = 0

for i in range(0, len(Arrival_times)):
    print("iteration",i,"Time",Time)
    print("iteration",i,"Arrival_times of",i, "is", Arrival_times[i])
    Time_Passed_Since_Last_Arrival = Arrival_times[i] - Time
    print("iteration",i,"Time_Passed_Since_Last_Arrival",Time_Passed_Since_Last_Arrival)
    
    for j in range(0, len(machine_busy_times)):
        if machine_busy_times[j] > Time_Passed_Since_Last_Arrival:
            machine_busy_times[j] -= Time_Passed_Since_Last_Arrival
        else:
            machine_busy_times[j] = 0
    print("iteration",j,"machine_busy_times",machine_busy_times)
    
    
    for j in range(0, len(operator_busy_time)):
        if operator_busy_time[j] > Time_Passed_Since_Last_Arrival:
            operator_busy_time[j] -= Time_Passed_Since_Last_Arrival
        else:
            operator_busy_time[j] = 0 
    print("iteration",j,"operator_busy_time",operator_busy_time)
    
    print("iteration",i,"setup time for i is",setup_times[:,i])
    machine_ready_times = np.add(machine_busy_times, setup_times[:, i])
    print("iteration",i,"machine ready time",machine_ready_times)
    
    First_Ready_MCHN_idx = np.argmin(machine_ready_times)
    print("iteration",i,"First_Ready_MCHN_idx ",First_Ready_MCHN_idx)
    
    First_Ready_Operator_idx = np.argmin(operator_busy_time)
    print("iteration",i,"First_Ready_Operator_idx ",First_Ready_Operator_idx)
    
    First_machine_ready_time = machine_ready_times[First_Ready_MCHN_idx]
    print("iteration",i,"First_machine_ready_time ",First_machine_ready_time)
    
    First_operator_ready_time = operator_busy_time[First_Ready_Operator_idx]
    print("iteration",i,"First_operator_ready_time ",First_operator_ready_time)
    
    customers_service_times[i] = service_times_harvesting[First_Ready_MCHN_idx, i]
    print("iteration",i,"customers_service_times ",customers_service_times)
    
    if First_operator_ready_time == 0:
        operator_busy_time[First_Ready_Operator_idx] = First_machine_ready_time
    else:
        operator_busy_time[First_Ready_Operator_idx] += First_machine_ready_time
    print("iteration",i,"operator_busy_time ",operator_busy_time)
        
    Customer_End_Time = operator_busy_time[First_Ready_Operator_idx] + customers_service_times[i]
    print("iteration",i,"Customer_End_Time ",Customer_End_Time)
    
    machine_busy_times[First_Ready_MCHN_idx] += Customer_End_Time
    print("iteration",i,"machine_busy_times ",machine_busy_times)

    Departure_time[i] = Customer_End_Time + Arrival_times[i]
    print("iteration",i,"Departure_time ",Departure_time)

    Waiting_time_for_service[i] = operator_busy_time[First_Ready_Operator_idx]
    print("iteration",i,"Waiting_time_for_service ",Waiting_time_for_service)
    
    Time = Arrival_times[i]
    print("iteration",i,"Time",Time, "\n")

       
    