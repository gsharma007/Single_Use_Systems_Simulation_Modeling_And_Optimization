#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 17:51:22 2019

@author: gauravsharma
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 12:57:17 2019

@author: gauravsharma
"""

import numpy as np

# number of customers in system
NUM_CUSTOMERS = 5

# Time between arrivals drawn from log-normal dist
# which its mean (exp(mu + sigma^2)) equals 2 hours
Arrivals = np.random.lognormal(mean=0.6, sigma=0.3, size=NUM_CUSTOMERS)
Arrival_times = [np.sum(Arrivals[:n]) for n in range(0, len(Arrivals))]

"""
1ST STEP: (HARVESTING)
"""

# number of machines for servicing customers
NUM_MACHINES = 2

# number of operator for setting up machines
NUM_OPERATOR = 2

# Each machine has unique Setup time for each customer (2D array)
# drawn from exponential dist with rate of 0.5 hours/30 minutes
setup_times = np.random.exponential(scale=0.5, size=(NUM_MACHINES, NUM_CUSTOMERS))

# Each machine has unique Service times for each customer (2D array)
# drawn from triangular dist between 3.75 and 4.25 hours
# with  mode and mean at 4 hour
service_times_harvesting = np.random.triangular(left=3.75, mode=4, right=4.25, size=(NUM_MACHINES, NUM_CUSTOMERS))

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
          
       # decreasing operator busy times by the time passed
    for j in range(0, len(operator_busy_time)):
        if operator_busy_time[j] > Time_Passed_Since_Last_Arrival:
            operator_busy_time[j] -= Time_Passed_Since_Last_Arrival
        else:
            operator_busy_time[j] = 0       
                
      # length time from now until the machines get ready considering
    # time needed for setting up machines
    machine_ready_times = np.add(machine_busy_times, setup_times[:, i])
    print("iteration",i,"machine ready time",machine_ready_times)
    
        # index of the machine that gets ready first
    First_Ready_MCHN_idx = np.argmin(machine_ready_times)
    print("iteration",i,"First_Ready_MCHN_idx ",First_Ready_MCHN_idx)

        # index of operator that will get free first
    First_Ready_Operator_idx = np.argmin(operator_busy_time)
    print("iteration",i,"First_Ready_Operator_idx ",First_Ready_Operator_idx)

        # the time that the first machine gets ready
    First_machine_ready_time = machine_ready_times[First_Ready_MCHN_idx]
    print("iteration",i,"First_machine_ready_time ",First_machine_ready_time)

    # the time that the first operator gets ready
    First_operator_ready_time = operator_busy_time[First_Ready_Operator_idx]
    print("iteration",i,"First_operator_ready_time ",First_operator_ready_time)
    
        # service time of the first machine
    customers_service_times[i] = service_times_harvesting[First_Ready_MCHN_idx, i]
    print("iteration",i,"customers_service_times ",customers_service_times)

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
cryo_Arrival_times = Departure_time

# total time in step 1
Step1_times = np.subtract(Departure_time, Arrival_times)
