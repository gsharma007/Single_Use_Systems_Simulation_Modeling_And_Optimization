#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 21 17:10:24 2019

@author: gauravsharma
"""

import numpy as np

# number of customers in system
NUM_CUSTOMERS = 20

# Time between arrivals drawn from log-normal dist
# which its mean (exp(mu + sigma^2)) equals 2 hours
Arrivals = np.random.lognormal(mean=0.6, sigma=0.3, size=NUM_CUSTOMERS)
Arrival_times = [np.sum(Arrivals[:n]) for n in range(0, len(Arrivals))]

"""
1ST STEP: (HARVESTING)
"""

# number of machines for servicing customers
NUM_MACHINES = 3

# number of operator for setting up machines
NUM_OPERATOR = 3

# Each machine has unique Setup time for each customer (2D array)
# drawn from exponential dist with rate of 3 hours
setup_times = np.random.exponential(scale=3, size=(NUM_MACHINES, NUM_CUSTOMERS))

# Each machine has unique Service times for each customer (2D array)
# drawn from triangular dist between 0.25 and 0.75 hours
# with  mode and mean at 0.5 hour
service_times_harvesting = np.random.triangular(left=0.25, mode=0.5, right=0.75, size=(NUM_MACHINES, NUM_CUSTOMERS))

# customers waiting time to get service
Waiting_time_for_service = np.zeros(NUM_CUSTOMERS)

# customers departure time for step 1
Departure_time = np.zeros(NUM_CUSTOMERS)

# customers service times
customers_service_times = np.zeros(NUM_CUSTOMERS)

# length of time each machine has left of its current task
# Initially all machines are ideal
machine_busy_times = np.zeros(NUM_MACHINES)

# length of time left for operator to finish its task
# Initially all operators is free
operator_busy_time = np.zeros(NUM_OPERATOR)

# time for this step
Time = 0

# getting service
for i in range(0, len(Arrival_times)):
    
      # time since last arrival
    Time_Passed_Since_Last_Arrival = Arrival_times[i] - Time
    
        # decreasing the machine busy times by the time passed
    for j in range(0, len(machine_busy_times)):
        if machine_busy_times[j] > Time_Passed_Since_Last_Arrival:
            machine_busy_times[j] -= Time_Passed_Since_Last_Arrival
        else:
            machine_busy_times[j] = 0
            
                
      # length time from now until the machines get ready considering
    # time needed for setting up machines
    machine_ready_times = np.add(machine_busy_times, setup_times[:, i])
    
        # index of the machine that gets ready first
    First_Ready_MCHN_idx = np.argmin(machine_ready_times)
    
        # index of operator that will get free first
    First_Ready_Operator_idx = np.argmin(operator_busy_time)
    
        # the time that the first machine gets ready
    First_machine_ready_time = machine_ready_times[First_Ready_MCHN_idx]

    # the time that the first operator gets ready
    First_operator_ready_time = operator_busy_time[First_Ready_Operator_idx]
    
        # service time of the first machine
    customers_service_times[i] = service_times_harvesting[First_Ready_MCHN_idx, i]

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
    # END of FOR

    # ready time for transportation
Transport_Arrival_times = Departure_time

# total time in step 1
Step1_times = np.subtract(Departure_time, Arrival_times)


"""
2ND STEP: (TRANSPORT TO MANUFACTURING FACILITY)
"""

# transport time, normal dist with mean of 6 hours and std of 2 hours
Transport_times = np.random.normal(6, 2, NUM_CUSTOMERS)
Transport_times = np.absolute(Transport_times)

Transport_times_sorted = np.sort(Transport_times)

destination_time = np.add(Transport_Arrival_times, Transport_times_sorted)

facility_arrival_time = destination_time

Step2_times = np.subtract(destination_time, Transport_Arrival_times)


"""
3RD STEP: (MANUFACTURING PROCESS)
"""

# number of machines for manufacturing
NUM_MANUF_MACHINES = 3

# number of operator for setting up machines
NUM_MANUF_OPERATOR = 3

# Each machine has unique Setup time for each customer (2D array)
# drawn from exponential dist with rate of 1 hours
manufacturing_setup_times = np.random.exponential(scale=1, size=(NUM_MANUF_MACHINES, NUM_CUSTOMERS))

# Each machine has unique manufacturing times for each customer (2D array)
#  drawn from triangular dist between 3 and 7 hours
#  with  mode and mean at 5 hour
manufacturing_times = np.random.triangular(left=3, mode=5, right=7, size=(NUM_MANUF_MACHINES, NUM_CUSTOMERS))

# customers waiting time to get service
Waiting_time_for_manufacturing = np.zeros(NUM_CUSTOMERS)
# customers departure time for step 3
Manufacturing_Departure_time = np.zeros(NUM_CUSTOMERS)
# customers manufacturing times
customers_manufacturing_times = np.zeros(NUM_CUSTOMERS)

# length of time each machine has left of its current task
# Initially all machines are ideal
manufacturing_machine_busy_times = np.zeros(NUM_MANUF_MACHINES)

# length of time left for operator to finish its task
# Initially all operators is free
manufacturing_operator_busy_time = np.zeros(NUM_MANUF_OPERATOR)

# time for this step
manufacturing_Time = 0

# getting manufacturing
for i in range(0, len(facility_arrival_time)):
    # time since last arrival
    Time_Passed_Since_Last_Arrival = facility_arrival_time[i] - manufacturing_Time

    # decreasing the machine busy times by the time passed
    for j in range(0, len(manufacturing_machine_busy_times)):
        if manufacturing_machine_busy_times[j] > Time_Passed_Since_Last_Arrival:
            manufacturing_machine_busy_times[j] -= Time_Passed_Since_Last_Arrival
        else:
            manufacturing_machine_busy_times[j] = 0

    # decreasing operator busy times by the time passed
    for j in range(0, len(manufacturing_operator_busy_time)):
        if manufacturing_operator_busy_time[j] > Time_Passed_Since_Last_Arrival:
            manufacturing_operator_busy_time[j] -= Time_Passed_Since_Last_Arrival
        else:
            manufacturing_operator_busy_time[j] = 0

    # length time from now until the machines get ready considering
    # time needed for setting up machines
    manufacturing_machine_ready_times = np.add(manufacturing_machine_busy_times, manufacturing_setup_times[:, i])

    # index of the machine that gets ready first
    manufacturing_First_Ready_MCHN_idx = np.argmin(manufacturing_machine_ready_times)

    # index of operator that will get free first
    manufacturing_First_Ready_Operator_idx = np.argmin(manufacturing_operator_busy_time)

    # the time that the first machine gets ready
    manufacturing_First_machine_ready_time = manufacturing_machine_ready_times[manufacturing_First_Ready_MCHN_idx]

    # the time that the first operator gets ready
    manufacturing_First_operator_ready_time = manufacturing_operator_busy_time[manufacturing_First_Ready_Operator_idx]

    # service time of the first machine
    customers_manufacturing_times[i] = manufacturing_times[manufacturing_First_Ready_MCHN_idx, i]

    # checking if operator is busy or not
    if manufacturing_First_operator_ready_time == 0:
        manufacturing_operator_busy_time[manufacturing_First_Ready_Operator_idx] = manufacturing_First_machine_ready_time
    else:
        manufacturing_operator_busy_time[manufacturing_First_Ready_Operator_idx] += manufacturing_First_machine_ready_time

    # computing the time customer will be done with service
    manufacturing_End_Time = manufacturing_operator_busy_time[manufacturing_First_Ready_Operator_idx] + customers_manufacturing_times[i]

    # increasing the busy time of the machine giving service
    manufacturing_machine_busy_times[manufacturing_First_Ready_MCHN_idx] += manufacturing_End_Time

    # computing the time customer is done with service
    Manufacturing_Departure_time[i] = manufacturing_End_Time + facility_arrival_time[i]

    # amount time customer waited to get service
    # considering both operator and machines
    Waiting_time_for_manufacturing[i] = manufacturing_operator_busy_time[manufacturing_First_Ready_Operator_idx]

    # progressing time to next arrival
    manufacturing_Time = facility_arrival_time[i]
    # END of FOR

# ready time for transportation
ready_return_clinic_times = Manufacturing_Departure_time

# total time in step 3
Step3_times = np.subtract(Manufacturing_Departure_time, facility_arrival_time)

"""
4TH STEP: (TRANSPORT BACK TO CLINIC)
"""

# transport time, normal dist with mean of 6 hours and std of 2 hours
Transport_return_times = np.random.normal(6, 2, NUM_CUSTOMERS)
Transport_return_times = np.absolute(Transport_return_times)

Transport_return_times_sorted = np.sort(Transport_return_times)

clinic_arrival_times = np.add(Transport_return_times_sorted, ready_return_clinic_times)

Exit_times = clinic_arrival_times

Step4_times = np.subtract(clinic_arrival_times, ready_return_clinic_times)

# ############ END of Step 4

# total service time from step 1 & 3
Total_Service_Time = np.add(customers_service_times, customers_manufacturing_times)
print("mean total service times (Step 1 & 3): ", np.mean(Total_Service_Time))

# total wait time from step 1 & 3
Total_Wait_Time = np.add(Waiting_time_for_service, Waiting_time_for_manufacturing)
print("mean total waite times (Step 1 & 3): ", np.mean(Total_Wait_Time))

# total transport time from step 2 & 4
Total_Transport_time = np.add(Transport_times_sorted, Transport_return_times_sorted)
print("mean total transport times (Step 2 & 4): ", np.mean(Total_Transport_time))

Total_time_in_System = np.subtract(Exit_times, Arrival_times)
print("mean total time in whole system: ", np.mean(Total_time_in_System), "\n")

print("mean time in Step 1: ", np.mean(Step1_times))
print("mean time in Step 2: ", np.mean(Step2_times))
print("mean time in Step 3: ", np.mean(Step3_times))
print("mean time in Step 4: ", np.mean(Step4_times))
