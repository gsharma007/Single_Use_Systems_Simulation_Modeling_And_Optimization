#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 14:21:38 2019

@author: gauravsharma
"""

""" 
Step 1- Cell harvesting at Clinic
"""

import numpy as np

Num_Patients = 5  #limiting number of patients in the system for the analysis

# generating an array of random interarrival times from lognormal distribution to achieve the expected arrival time of 2 hours 
# which its mean (exp(mu + sigma^2/2)) equals 2 hours
Inter_arrival_hrs = np.random.lognormal(mean=0.655, sigma=0.3, size= Num_Patients) 
Inter_arrival_mins = Inter_arrival_hrs*60 #coverting the interarrivals times from hrs to mins

#calculating actual arrival times by adding interarrival times
Arrival_times = [np.sum(Inter_arrival_mins[:n]) for n in range(0, len(Inter_arrival_mins)+1)]

Operator_count = 2  # number of avilable operators for setting up the machines
Machine_count = 2  # number of machines for harvesting cells from customers
# Each machine has unique Setup time for each customer (2D array)
# drawn from exponential dist with rate of 30 minutes
setup_times_S1 = np.random.exponential(scale=30, size=(Machine_count, Num_Patients))  

# Each machine has unique Service times for each customer (2D array)
# drawn from triangular dist between 180 and 300 minutes 
# with  mode and mean at 240 minutes
service_times_S1 = np.random.triangular(left=180, mode=240, right=300, size=(Machine_count, Num_Patients))

"""
Logic for operator and machine allocation to the customer
"""

# customers waiting time in queue to get service
Waiting_time_for_service = np.zeros(Num_Patients)

# customers departure time from step 1
Departure_time = np.zeros(Num_Patients)

# customers service times
customers_service_times = np.zeros(Num_Patients)

# length of time each machine has left of its current task
# Initially all machines are ideal
machine_busy_times = np.zeros(Machine_count)

# length of time left for operator to finish its task
# Initially all operators is free
operator_busy_time = np.zeros(Num_Patients)

# time for this step
Time = 0

# getting service
for i in range(0, len(Inter_arrival_mins)):
    
      # time since last arrival
    Time_Passed_Since_Last_Arrival = Inter_arrival_mins[i] - Time
    
        # decreasing the machine busy times by the time passed
    for j in range(0, len(machine_busy_times)):
        if machine_busy_times[j] > Time_Passed_Since_Last_Arrival:
            machine_busy_times[j] -= Time_Passed_Since_Last_Arrival
        else:
            machine_busy_times[j] = 0
            
    # length time from now until the machines get ready considering
    # time needed for setting up machines
    machine_ready_times = np.add(machine_busy_times, setup_times_S1[:, i])
    
        # index of the machine that gets ready first
    First_Ready_MCHN_idx = np.argmin(machine_ready_times)
    
        # index of operator that will get free first
    First_Ready_Operator_idx = np.argmin(operator_busy_time)
    
        # the time that the first machine gets ready
    First_machine_ready_time = machine_ready_times[First_Ready_MCHN_idx]

    # the time that the first operator gets ready
    First_operator_ready_time = operator_busy_time[First_Ready_Operator_idx]
    
        # service time of the first machine
    customers_service_times[i] = service_times_S1[First_Ready_MCHN_idx, i]

    # checking if operator is busy or not
    if First_operator_ready_time == 0:
        operator_busy_time[First_Ready_Operator_idx] = First_machine_ready_time
    else:
        operator_busy_time[First_Ready_Operator_idx] += First_machine_ready_time

    # computing the time customer will be done with service
    Customer_End_Time = operator_busy_time[First_Ready_Operator_idx] + customers_service_times[i]

    # increasing the busy time of the machine giving service
    machine_busy_times[First_Ready_MCHN_idx] += Customer_End_Time

    # computing the time customer is done with service
    Departure_time[i] = Customer_End_Time + Arrival_times[i]

    # amount time customer waited to get service
    # considering both operator and machines
    Waiting_time_for_service[i] = operator_busy_time[First_Ready_Operator_idx]

    # progressing time to next arrival
    Time = Arrival_times[i]
    
# total time in step 1
Step1_times = np.subtract(Departure_time, Arrival_times)

# ready time for transportation
Transport_Arrival_times = Departure_time