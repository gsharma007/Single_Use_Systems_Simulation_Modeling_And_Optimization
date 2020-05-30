#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 21:58:21 2020

@author: gauravsharma
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Bio_Man_V3 import Simulation_run
import seaborn as sns
import scipy.stats as stats
import pylab
from statsmodels.graphics.factorplots import interaction_plot

df_consol_final = pd.DataFrame()

replication = 0
for compa in range(0,1):
    print("iteration number",compa)
    replication+=1
    (df_consol, hrv_event_calendar, mfg_df_consol, mfg_event_calendar)  = Simulation_run()
    print("Simrun done...")
    df_consol['replication'] = replication
    df_consol['patient_number'] = df_consol.index
    df_consol_final = df_consol_final.append(df_consol)
    

# =============================================================================
# 
# #cols = df_consol_final.columns.tolist()
# #cols
# 
# print("Lognormal Distribution For Generated InterArrival Times in Hours")
# sns.distplot(df_consol_final['Interarrival times(hours)'])
# plt.show()
# 
# print("Distribution For Generated Arrival Times in Hours")
# sns.distplot(df_consol_final['Arrival times(hours)'])
# plt.show()
# 
# Arrival_times_run_wise = df_consol_final.groupby(['run']).mean()['Arrival times(hours)']
# sns.distplot(Arrival_times_run_wise)
# plt.show()
# 
# print("Distribution For target_blood_count")
# sns.distplot(df_consol_final['Target_Blood_Count(Y_bar)'])
# plt.show()
# 
# print("Distribution For t_low in days")
# sns.distplot(df_consol_final['t_low_mfg'])
# plt.show()
# 
# target_0 = df_consol_final.loc[df_consol_final['Yield_Curve_MFG'] == 1]
# target_1 = df_consol_final.loc[df_consol_final['Yield_Curve_MFG'] == 2]  
# 
# plt.figure()
# print("Distribution for each level for t_low in days")
# sns.distplot(df_consol_final['t_low_mfg'])
# sns.distplot(target_0[['t_low_mfg']], hist=False, rug=True)
# sns.distplot(target_1[['t_low_mfg']], hist=False, rug=True)
# plt.show()
# 
# print("Distribution For t_low_new in days")
# sns.distplot(df_consol_final['t_low_new_mfg'])
# plt.show()
# 
# print("Distribution For t_up in days")
# sns.distplot(df_consol_final['t_up_mfg'])
# plt.show()
# 
# print("Distribution For t_up_new in days")
# sns.distplot(df_consol_final['t_up_new_mfg'])
# plt.show()
# 
# print("Distribution For t_normal in days")
# sns.distplot(df_consol_final['t_normal_mfg'])
# plt.show()
# 
# # print("Visualizing time selected vs yield")
# # df_consol_final.plot.scatter(x='time_selected_mfg (hours)', y='Achieved_Yield_from_mfg')
# # plt.show()
# 
# #Checking if time selected is specified as processing time
# dfobj = df_consol_final.loc[~(df_consol_final['time_selected_mfg (hours)'] != df_consol_final['Achieved_Yield_from_mfg'])]
# if dfobj.empty == True:
#     print('All Selected values are same as Mfg Service Times')
# else:
#     print('Check, there is some problem')
#     
# #df_consol_final.boxplot(by ='run', column =['Target_Blood_Count(Y_bar)'], grid= False, fontsize=5)
# 
# 
# # sns.distplot(df_consol_final['time_selected_mfg'])
# # plt.show()
# # #sns.distplot(df_consol_final['time_selected_mfg'], by = 'run')
# 
# # sns.distplot(df_consol_final['Mfg_Departure_times'])
# # plt.show()
# 
# # sns.lineplot(x = 'time_selected_mfg', y = 'Achieved_Yield_from_mfg', hue= 'Yield_Curve_MFG', data= df_consol_final)
# # plt.show()
# 
# # df_result = df_consol_final.groupby('Test_Outcomes_MFG').agg(['sum']).reset_index()
# # df_result.plot(x='Test_Outcomes_MFG',kind="bar")
# # plt.show()
# 
# 
# # sns.distplot(df_consol_final['MFG_setup_times'])
# # plt.show()
# 
# # sns.distplot(df_consol_final['MFG_wait_times'])
# # plt.show()
# 
# # =============================================================================
# # plt.figure(figsize=[10,8])
# # 
# # plt.bar(df_consol_final['MFG_service_times'], width = 0.5, color='#0504aa')
# # plt.grid(axis='y', alpha=0.75)
# # plt.xlabel('Pixels',fontsize=15)
# # plt.ylabel('Frequency of Pixels',fontsize=15)
# # plt.xticks(fontsize=15)
# # plt.yticks(fontsize=15)
# # plt.ylabel('Frequency',fontsize=15)
# # plt.title('Natural Image Histogram',fontsize=15)
# # plt.show()
# # =============================================================================
# 
# 
# 
#     
# 
# df_consol_final.to_csv(r'/Users/gauravsharma/Documents/Simulation_results_V1.csv')
# =============================================================================
