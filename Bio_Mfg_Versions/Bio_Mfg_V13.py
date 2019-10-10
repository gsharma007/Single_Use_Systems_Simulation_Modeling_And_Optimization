#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 04:57:15 2019

@author: gauravsharma
"""

import numpy as np
import matplotlib.pyplot as plt
from smt.sampling_methods import LHS  #surrogate modeling toolbox
from scipy import stats
import seaborn as sns

# number of customers considered in the system
NUM_CUSTOMERS = 10

#A 3-factor design
maxmin_range = np.array([[12.0, 18.0], [4.5, 6.0]]) #,[25.0,34.0]])
sampling = LHS(xlimits=maxmin_range)

#Generating count of samples/runs to be taken
runs_count = NUM_CUSTOMERS
runs = sampling(runs_count)

print(runs.shape)

BV_harv = runs[:, 0] #Blood volume harvesting
CC_harv = runs[:, 1] #coagulant concentration
# Third = runs[:, 2]  #3rd predictor

## Plotting more than one axes
# =============================================================================
# fig = plt.figure()
# ax = plt.axes(projection='3d')
# ax.scatter3D(BV_harv, CC_harv, Third, cmap='Greens')
# ax.set_xlabel('BV_harv')
# ax.set_ylabel('CC_harv')
# ax.set_zlabel('Third');
# =============================================================================

plt.plot(BV_harv, CC_harv, "o" , markersize=5, color="red")
plt.xlabel("BV_harv")
plt.ylabel("CC_harv")
plt.show()
plt.clf()

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
NUM_OPERATOR = 50

# number of machines for servicing customers
NUM_MACHINES = 4

# Each operator has unique setup time for each customer
# drawn from exponential dist with rate of 0.5 hours/30 minutes
# =============================================================================
# https://seaborn.pydata.org/tutorial/distributions.html
# =============================================================================
setup_times = np.random.exponential(scale=0.5, size=NUM_OPERATOR)

# =============================================================================
# plt.figure()
# sns.set(color_codes=True)
# sns.distplot(setup_times,hist=False, rug=True)
# =============================================================================

# =============================================================================
plt.figure()
plt.hist(setup_times)
plt.title('setup_times')
plt.show()
plt.clf()
# =============================================================================

""" service time generation """
# Each machine has unique Service times for each customer
# drawn from triangular dist between 3.75 and 4.25 hours
# with  mode and mean at 4 hour
# service_times_harvesting = np.random.triangular(left=3.75, mode=4, right=4.25, size=NUM_MACHINES)
#lower, upper, mu, and sigma are four parameters
lower, upper = 2, 6
mu, sigma = 4, 2
#instantiate an object X using the above four parameters,
X = stats.truncnorm((lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma)
#generate sample data for each machine
service_times_harvesting = X.rvs(NUM_MACHINES)
#compute the PDF of the sample data
pdf_probs = stats.truncnorm.pdf(service_times_harvesting, (lower-mu)/sigma, (upper-mu)/sigma, mu, sigma)
#compute the CDF of the sample data
cdf_probs = stats.truncnorm.cdf(service_times_harvesting, (lower-mu)/sigma, (upper-mu)/sigma, mu, sigma)
#make a histogram for the samples
plt.figure()
plt.hist(service_times_harvesting, bins= 5,normed=True,alpha=0.3,label='histogram');
#plot the PDF curves 
plt.plot(service_times_harvesting[service_times_harvesting.argsort()],pdf_probs[service_times_harvesting.argsort()],linewidth=2.3,label='PDF curve')
#plot CDF curve        
plt.plot(service_times_harvesting[service_times_harvesting.argsort()],cdf_probs[service_times_harvesting.argsort()],linewidth=2.3,label='CDF curve')
#legend
plt.legend(loc='best')
plt.show()
plt.clf()


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

#print(operators)      #final list of operators with their decision values
#print(machines)       #final list of machines with their decision values

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
                
    # print("temp_o : ", temp_o)
    # print("temp_m : ", temp_m)
    
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

    # print("patient time : ", patient)
    # print("patient total Time : " , total_time-patient)
    # print("Operators",operators)
    # print("Machines", machines)
    # print("wait time :",wait_time)
    
print("Step 1 arrival times:" , Arrival_times)
print("step1_operator_allocation:", step1_operator_allocation)
print("Step1_machine_allocation:", step1_machine_allocation)
#print("Step 1 wait times:" ,step1_wait_time)
#print("Step1 service times:" , step1_service_times)
#print("Step 1 total times:" , step1_total_time)

#visualizing patient waiting times
# =============================================================================
# plt.plot(step1_wait_time)
# plt.title('step1_wait_time')
# plt.show()
# plt.clf
# =============================================================================

#visualizing patient service times
# =============================================================================
# plt.plot(step1_service_times)
# plt.title('Step1_service_times')
# plt.show()
# plt.clf
# =============================================================================

#visualizing patient total time in step 1
plt.plot(step1_total_time)
plt.title('step1_total_time')
plt.show()
plt.clf

t_lower_harv = 4 #maximum growth harvest time
t_max_harv = 6.0 #maximum time before cell count loss
t_min_harv = 2.5 #minimum time for harvesting before we start observing effects
alpha_harv = 12000 #model cofficient
alpha1_harv = 15000 #patient cofficient
alpha2_harv = 19000 #chemical process effectiveness coefficient
alpha3_G_harv = 30000 #rowth coefficient before t_lower_harv is hit
alpha3_D_harv = 35000 #decay coefficient after t_max_harv hit

yield_harvesting = []
for t_harv in step1_service_times:  #time spent for harvesting
    if(t_harv >= t_min_harv and t_harv <= t_lower_harv):
        Y_harv = alpha_harv + alpha1_harv * BV_harv + alpha2_harv * CC_harv + alpha3_G_harv * t_harv 
    elif (t_harv >= t_max_harv):
        Y_harv = alpha_harv + alpha1_harv * BV_harv + alpha2_harv * CC_harv + alpha3_D_harv * t_harv
        
    else:
        Y_harv = alpha_harv + alpha1_harv * BV_harv + alpha2_harv * CC_harv

    yield_harvesting.append(Y_harv)
    
#print("Harvesting Yield:" , yield_harvesting)

#visualizing yiled variation for each patient    
plt.boxplot(yield_harvesting)
plt.title('Harvesting_Yield')
plt.show()
plt.clf
