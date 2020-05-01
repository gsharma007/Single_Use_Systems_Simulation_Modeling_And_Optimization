#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 21:58:21 2020

@author: gauravsharma
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from BioMan_V2 import Simulation_run
import seaborn as sns
import scipy.stats as stats
import pylab
from statsmodels.graphics.factorplots import interaction_plot

df_consol_final = pd.DataFrame()



replication = 0
for compa in range(0,5):
    replication+=1
    df = Simulation_run()
    df['replication'] = replication
    df['patient_number'] = df.index
    df_consol_final = df_consol_final.append(df)
    print("iteration number",compa)



# =============================================================================
# plt.figure(figsize=[10,8])
# 
# plt.bar(df_consol_final['MFG_service_times'], width = 0.5, color='#0504aa')
# plt.grid(axis='y', alpha=0.75)
# plt.xlabel('Pixels',fontsize=15)
# plt.ylabel('Frequency of Pixels',fontsize=15)
# plt.xticks(fontsize=15)
# plt.yticks(fontsize=15)
# plt.ylabel('Frequency',fontsize=15)
# plt.title('Natural Image Histogram',fontsize=15)
# plt.show()
# =============================================================================



    

df_consol_final.to_csv(r'/Users/gauravsharma/Documents/Simulation_results_V1.csv')