#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 01:48:29 2019

@author: gauravsharma
"""
import numpy as np
from scipy.stats import erlang
Arrivals = np.random.exponential(scale = 0.333, size=20)
Arrival_times = [np.sum(Arrivals[:n]) for n in range(0,len(Arrivals))]

def queue(Arrival_times) :
    service_times_operator = np.random.exponential(scale = 0.25, size=20)
    
    Departure_time = []
    
    for arrival in Arrival_times:
            
        if len(Departure_time) > 0  and Departure_time[-1]>arrival:
                departure = Departure_time[-1] + service_times_operator[Arrival_times.index(arrival)]
        else:
            departure = arrival + service_times_operator[Arrival_times.index(arrival)]
        Departure_time.append(departure)
    return Departure_time

Departure_time = queue(Arrival_times)
    
service_times_machine_a = np.random.exponential(scale = 0.20, size=20)
service_times_machine_b = np.random.exponential(scale = 0.30, size=20)

Departure_a =[]
Departure_b =[]

for dept in Departure_time:
    if len(Departure_a) == 0 or Departure_a[-1] < dept: 
        end_time = dept + service_times_machine_a[Departure_time.index(dept)]
        Departure_a.append(end_time)
    else:
        if len(Departure_b) == 0 or Departure_b[-1] < dept:
            end_time = dept + service_times_machine_b[Departure_time.index(dept)]
            Departure_b.append(end_time)
        else:
            if (Departure_a[-1] < Departure_b[-1]):
                end_time = Departure_a[-1] + service_times_machine_a[Departure_time.index(dept)]
                Departure_a.append(end_time)
            else :
                end_time = Departure_b[-1] + service_times_machine_b[Departure_time.index(dept)]
                Departure_b.append(end_time)
    
combined_dept_time_machines =  np.concatenate((Departure_a,Departure_b),axis = 0)
sorted_dept_time_machines = np.sort(combined_dept_time_machines)

cryo_arrival_time = queue(sorted_dept_time_machines.tolist())
manufact_arrival_time = queue(cryo_arrival_time)
