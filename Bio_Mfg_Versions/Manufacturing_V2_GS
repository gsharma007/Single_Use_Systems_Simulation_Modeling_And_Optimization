#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

"""
1ST STEP: (HARVESTING)
"""

NUM_CUSTOMERS = 20

# time of system
Time = 0

# arrival times with rate of one patient every 2 hour
Arrivals = np.random.exponential(scale=2, size=NUM_CUSTOMERS)
Arrival_times = [np.sum(Arrivals[:n]) for n in range(0, len(Arrivals))]

# constant step time for machine (in hours)
machine_setup_time = 3

# service times with rate of half hour per customer
service_times_harvesting = np.random.exponential(scale=0.5, size=NUM_CUSTOMERS)

Waiting_time_for_service = np.zeros(NUM_CUSTOMERS)

# machine gets set up after the first patient arrives
Time = machine_setup_time + Arrival_times[0]

# calculating wait times
for i in range(0, len(Arrival_times)):

    if (Time - Arrival_times[i]) > 0:
        Waiting_time_for_service[i] = Time - Arrival_times[i]
    else:
        Waiting_time_for_service[i] = 0

    Time = Time + service_times_harvesting[i]

# Dept_time = Arrival_time + wait_time + service_time
Departure_time = np.add(np.add(Arrival_times, Waiting_time_for_service), service_times_harvesting)

Transport_Arrival_times = Departure_time

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

# manufacturing times with rate of one product every 5 hour
manufacturing_times = np.random.exponential(5, NUM_CUSTOMERS)

# constant step time for machine (in hours)
manufacturing_machine_setup_time = 5

Waiting_time_for_manufacturing = np.zeros(NUM_CUSTOMERS)

# machine gets set up after the first product arrives
Time = manufacturing_machine_setup_time + facility_arrival_time[0]

# calculating wait times
for i in range(0, len(facility_arrival_time)):

    if (Time - facility_arrival_time[i]) > 0:
        Waiting_time_for_manufacturing[i] = Time - facility_arrival_time[i]
    else:
        Waiting_time_for_manufacturing[i] = 0

    Time = Time + manufacturing_times[i]

# Dept_time = Arrival_time + wait_time + service_time
Manufacturing_Departure_time = np.add(np.add(facility_arrival_time, Waiting_time_for_manufacturing), manufacturing_times)

ready_return_clinic_times = Manufacturing_Departure_time

Step3_times = np.subtract(Manufacturing_Departure_time, facility_arrival_time)

"""
4TH STEP: (TRANSPORT BACK TO CLINIC)
"""

# transport time, normal dist with mean of 6 hours and std of 2 hours
Transport_return_times = np.random.normal(6, 2, NUM_CUSTOMERS)
Transport_return_times = np.absolute(Transport_return_times)

Transport_return_times_sorted = np.sort(Transport_return_times)

clinic_arrival_times = np.add(Transport_return_times_sorted, ready_return_clinic_times)

End_times = clinic_arrival_times

Step4_times = np.subtract(clinic_arrival_times, ready_return_clinic_times)

# ############ END of Step 4

# total service time from step 1 & 3
Total_Service_Time = np.add(service_times_harvesting, manufacturing_times)
print("mean total service times (Step 1 & 3): ", np.mean(Total_Service_Time))

# total wait time from step 1 & 3
Total_Wait_Time = np.add(Waiting_time_for_service, Waiting_time_for_manufacturing)
print("mean total waite times (Step 1 & 3): ", np.mean(Total_Wait_Time))

# total transport time from step 2 & 4
Total_Transport_time = np.add(Transport_times_sorted, Transport_return_times_sorted)
print("mean total transport times (Step 2 & 4): ", np.mean(Total_Transport_time))

Total_time_in_System = np.subtract(End_times, Arrival_times)
print("mean total time in whole system: ", np.mean(Total_time_in_System),"\n")

print("mean time in Step 1: ", np.mean(Step1_times))
print("mean time in Step 2: ", np.mean(Step2_times))
print("mean time in Step 3: ", np.mean(Step3_times))
print("mean time in Step 4: ", np.mean(Step4_times))
