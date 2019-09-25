#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 16:49:44 2019

@author: gauravsharma
"""

import csv

filename="/Users/gauravsharma/Documents/design.csv"
listofruns=[]
with open (filename, "r", newline = "") as csvfile:
    designs = csv.reader(csvfile)
    flag_first_row=False
    for row in designs:
        if flag_first_row==False:
            headers=row
            flag_first_row=True
        else:
            listofruns.append(row)


import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# number of customers considered in the system
NUM_CUSTOMERS = 5

# fixing seed for testing purpose
# np.random.seed(26)

# Time between arrivals drawn from log-normal dist
# which its mean (exp(mu + sigma^2)) equals 2 hours
Arrivals = np.random.lognormal(mean=0.6, sigma=0.3, size=NUM_CUSTOMERS)
Arrival_times = [np.sum(Arrivals[:n]) for n in range(0, len(Arrivals))]

"""
1ST STEP: (HARVESTING)
"""
# number of operator for setting up machines
NUM_OPERATOR = 2

# number of machines for servicing customers
NUM_MACHINES = 15

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

print(operators)      #final list of operators with their decision values
print(machines)       #final list of machines with their decision values

step1_wait_time = []
step1_total_time = []
step1_service_times = []
step1_machine_allocation = []
step1_operator_allocation = []

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
                
    print("temp_o : ", temp_o)
    print("temp_m : ", temp_m)
    
    step1_operator_allocation.append(temp_o["Name"])
    step1_machine_allocation.append(temp_m["Name"])
    step1_service_times.append(temp_m["service_time"])
    
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
            
    step1_wait_time.append(wait_time)
    step1_total_time.append(total_time-patient)

    print("patient time : ", patient)
    print("patient total Time : " , total_time-patient)
    print("Operators",operators)
    print("Machines", machines)
    print("wait time :",wait_time)
    
    print("Step 1 arrival times:" , Arrival_times)
    print("Step 1 wait times:" ,step1_wait_time)
    print("Step 1 total times:" , step1_total_time)
    print("Step1_machine_allocation:", step1_machine_allocation)
    print("step1_operator_allocation:", step1_operator_allocation)
    print("Step1 service times:" , step1_service_times)
    
BV_harv = 5 #Blood volume harvesting
CC_harv = 2 #coagulant concentration
t_lower_harv = 4#maximum growth harvest time
t_max_harv = 2.9 #maximum time before cell count loss
t_min_harv = 6 #minimum time for harvesting before we start observing effects
alpha_harv = 7 #model cofficient
alpha1_harv = 8 #patient cofficient
alpha2_harv = 9 #chemical process effectiveness coefficient
alpha3_G_harv = 10 #rowth coefficient before t_lower_harv is hit
alpha3_D_harv = 11 #decay coefficient after t_max_harv hit

yield_harvesting = []
for ST_H in step1_service_times:
    t_harv = ST_H #time spent for harvesting
    if(t_harv >= t_min_harv and t_harv <= t_lower_harv):
        Y_harv = alpha_harv + alpha1_harv * BV_harv + alpha2_harv * CC_harv + alpha3_G_harv * t_harv 
    elif (t_harv >= t_max_harv):
        Y_harv = alpha_harv + alpha1_harv * BV_harv + alpha2_harv * CC_harv + alpha3_D_harv * t_harv
        
    else:
        Y_harv = alpha_harv + alpha1_harv * BV_harv + alpha2_harv * CC_harv

    yield_harvesting.append(Y_harv)

print("Harvesting Yield:" , yield_harvesting)

plt.plot(step1_wait_time)
plt.xlabel('time in mins')
plt.title('Step 1 wait time')
plt.show()
plt.clf
    
plt.boxplot(yield_harvesting)
plt.title('Harvesting in Yield')
plt.show()
plt.clf

sns.set(color_codes=True)
sns.distplot(step1_wait_time, hist=False, rug=True);


"""
2nd Step: (Cryopreservation)
"""

cryo_arrivals = step1_total_time

# number of operator for setting up machines
cryo_Num_OPERATOR = 2

# number of machines for servicing customers
cryo_Num_MACHINES = 3

# Each operator has unique setup time for each customer
# drawn from exponential dist with rate of 0.5 hours/30 minutes
Cryo_setup_times = np.random.exponential(scale=0.5, size=cryo_Num_OPERATOR)

# Each machine has unique Service times for each customer
# drawn from triangular dist between 3.75 and 4.25 hours
# with  mode and mean at 4 hour
Cryo_service_times = np.random.triangular(left=3.75, mode=4, right=4.25, size=cryo_Num_MACHINES)


cryo_operators = []  #list of all operators with their characteristics
cryo_machines=[]     #list of all machines with their characteristics
counter=0       #used to indicate operator's index
for e in Cryo_setup_times:
    dict_cryo_opt = {
        "Name": "O_"+str(counter),
        "cryo_setup_time": e,
        "cryo_o_ready_time": 0
    }
    cryo_operators.append(dict_cryo_opt)   #appending the operator's characteristics dictionraies in one list
    counter = counter+1          #ensuring increment in operator's index

counter=0      #used to indicate machine's index
for x in Cryo_service_times:
    dict_cryo_machine={
        "Name":"M_"+str(counter),
        "cryo_service_time":x,
        "cryo_m_ready_time":0
    }
    cryo_machines.append(dict_cryo_machine) #appending the machine's characteristics dictionraies in one list
    counter= counter+1            #ensuring increment in machine's index

print(cryo_operators)      #final list of operators with their decision values
print(cryo_machines)       #final list of machines with their decision values

step2_wait_time = []
step2_total_time = []
step2_service_times = []
step2_machine_allocation = []
step2_operator_allocation = []

for patient in cryo_arrivals:
    cryo_wait_time = 0
    cryo_temp_o = cryo_operators[0]
    for cryo_opt in cryo_operators:
        if(cryo_opt["cryo_o_ready_time"]<=cryo_temp_o["cryo_o_ready_time"]):
            if(cryo_opt["cryo_setup_time"]<=cryo_temp_o["cryo_setup_time"]):
                cryo_temp_o = cryo_opt

    cryo_temp_m = cryo_machines[0]
    for cryo_mac in cryo_machines:
        if(cryo_mac["cryo_m_ready_time"]<=cryo_temp_m["cryo_m_ready_time"]):
            if(cryo_mac["cryo_service_time"]<=cryo_temp_m["cryo_service_time"]):
                cryo_temp_m = cryo_mac
                
    print("cryo_temp_o : ", cryo_temp_o)
    print("cryo_temp_m : ", cryo_temp_m)
    
    step2_operator_allocation.append(cryo_temp_o["Name"])
    step2_machine_allocation.append(cryo_temp_m["Name"])
    step2_service_times.append(cryo_temp_m["cryo_service_time"])
    
    if(patient>=cryo_temp_o["cryo_o_ready_time"] and patient>=cryo_temp_m["cryo_m_ready_time"]):
        cryo_total_time = cryo_temp_o["cryo_setup_time"]+cryo_temp_m["cryo_service_time"] + patient
    
    else:
        cryo_wait_time = max(cryo_temp_m["cryo_m_ready_time"], cryo_temp_o["cryo_o_ready_time"])-patient
        cryo_total_time = cryo_wait_time + patient + cryo_temp_o["cryo_setup_time"]+cryo_temp_m["cryo_service_time"] + patient

    for cryo_opt in cryo_operators:
        if(cryo_temp_o["Name"]==cryo_opt["Name"]):
            cryo_opt["cryo_o_ready_time"] =cryo_wait_time + cryo_opt["cryo_setup_time"]

    for cryo_mac in cryo_machines:
        if(cryo_temp_m["Name"]==cryo_mac["Name"]):
            cryo_mac["cryo_m_ready_time"] = cryo_total_time
            
    step2_wait_time.append(cryo_wait_time)
    step2_total_time.append(cryo_total_time-patient)

    print("S2 patient time : ", patient)
    print("S2 patient total Time : " , cryo_total_time-patient)
    print("S2 Operators",cryo_operators)
    print("S2 Machines", cryo_machines)
    print("S2 wait time :",cryo_wait_time)
    
    print("Step2 arrival times:" , cryo_arrivals)
    print("Step2 wait times:" ,step2_wait_time)
    print("Step2 total times:" , step2_total_time)
    print("Step2_machine_allocation:", step2_machine_allocation)
    print("step2_operator_allocation:", step2_operator_allocation)
    print("Step2_service times:" , step2_service_times)

plt.plot(step2_wait_time)
plt.xlabel('time in mins')
plt.title('Step 2 wait time')
plt.show()
plt.clf

sns.set(color_codes=True)
sns.distplot(step2_wait_time, hist=False, rug=True)