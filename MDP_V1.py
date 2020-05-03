#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 21:03:57 2019

@author: gauravsharma
"""

import numpy as np

Measurment_count = 4

Measurment_times = np.random.uniform(low = 0, high = 4, size= Measurment_count)
Measurment_times.sort()
Measurment_times_cumulative = [np.sum(Measurment_times[:n]) for n in range(0, len(Measurment_times)+1)]
Measurment_times_cumulative.remove(Measurment_times_cumulative[0])

time_values = []
for i in range(0, len(Measurment_times)+1):
    indexed_time = ("t" +str(i))
    time_values.append(indexed_time) 

m_times = []
counter=1  
for e in time_values:
    dict_opt = {
        "Measurement_time": "t_"+str(counter),
        "alpha_values": ["alpha_"+str(a) for a in range(1, counter+3)]
        #{"alpha_"+str(counter),"alpha_"+str(counter+1),"alpha_"+str(counter+2)}
    }
    m_times.append(dict_opt)
    counter = counter+1 
    #print(dict_opt)
print(m_times)

from random import randint

# =============================================================================
# for x in m_times:
#     value = randint(0, 3)
#     print(x['alpha_values'][value])
# =============================================================================

alpha_selected = []    
for x in m_times:
    print(x)
    value = randint(0,len(x['alpha_values']))
    print(value)
    random_alpha = x['alpha_values'][value]
    print(random_alpha)
    alpha_selected.append(random_alpha)
print(alpha_selected)   

   


# =============================================================================
# import random
# for value in m_times:
#     print(random.choice(value["alpha_values"]))    
# =============================================================================
 

#import random

#for key, value in dict.items():
 #   print random.choice(value), key
    


# =============================================================================
# aplha_1 = 2
# alpha_2 = 1.3*aplha_1
# 
# 
# for i in Measurment_times:
#     alpha_index = i
# =============================================================================
