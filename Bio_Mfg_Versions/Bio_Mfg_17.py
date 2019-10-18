#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 23:40:08 2019

@author: gauravsharma
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Bio_mfg_19 import function_2
import seaborn as sns
import scipy.stats as stats
import pylab


df_consol_final = pd.DataFrame()

replication = 0
for compa in range(0,50):    
    replication+=1
    df = function_2()
    df['replication'] = replication
    df['patient_number'] = df.index
    df_consol_final = df_consol_final.append(df)
    print("iteration number",compa)
       


"""
plt.scatter(time_level_patients[:2],yield_harvesting[:2])
plt.show()
plt.clf()
"""
#df_consol_final = df_consol_final.set_index('patient_number')
#df.T.boxplot()


"""
for p in df.patient_number:
    plt.boxplot(p, df.Achieved_Yield_from_Mfg)
    plt.show()
    plt.clf()
"""
plt.figure()
Plot1 = df_consol_final.boxplot(column=['Achieved_Yield_from_Mfg'], notch= True, usermedians= None)
#result = [item.get_ydata() for item in Plot1['whiskers']]
quartiles = np.percentile(df_consol_final.Achieved_Yield_from_Mfg, [25, 50, 75])
#data_min, data_max = df_consol_final.min(), df_consol_final.max()
print('5_number_summary', quartiles)
#print('data_min', data_min, 'data_max', data_max)
fig1 = Plot1.get_figure()
plt.show()

plt.figure()
Plot2 = df_consol_final.boxplot(by ='patient_number', column =['Achieved_Yield_from_Mfg'], grid= False, rot=90, fontsize=5)
fig2 = Plot2.get_figure()
plt.show()

plt.figure()
Plot3 = df_consol_final.boxplot(by ='run', column =['Achieved_Yield_from_Mfg'], grid= False, rot=90, fontsize=5)
fig3 = Plot3.get_figure()
plt.show()

plt.figure()
Plot4 = df_consol_final.boxplot(by ='patient_number', column =['diff_exp_achvd_yield_mfg'], grid= False, rot=90, fontsize=5)
fig4 = Plot4.get_figure()
plt.show()

plt.figure()
Plot5 = df_consol_final.boxplot(by ='run', column =['diff_exp_achvd_yield_mfg'], grid= False, rot=90, fontsize=5)
fig5 = Plot5.get_figure()
plt.show()

plt.figure()
# Construct the colormap
from matplotlib.colors import ListedColormap
current_palette = sns.color_palette("muted", n_colors=5)
cmap = ListedColormap(sns.color_palette(current_palette).as_hex())
N=90000
colors = np.random.randint(0,5,N)
Plot6 = plt.scatter(df_consol_final.patient_number, df_consol_final.diff_exp_achvd_yield_mfg, c=colors, cmap=cmap)
fig6 = Plot6.get_figure()
plt.show()

plt.figure()
# Construct the colormap
from matplotlib.colors import ListedColormap
current_palette = sns.color_palette("muted", n_colors=5)
cmap = ListedColormap(sns.color_palette(current_palette).as_hex())
N=90000
colors = np.random.randint(0,5,N)
Plot7 = plt.scatter(df_consol_final.run, df_consol_final.diff_exp_achvd_yield_mfg, c=colors, cmap=cmap)
fig7 = Plot7.get_figure()
plt.show()

#plt.figure()
#plt.boxplot(['patient_number','Achieved_Yield_from_Mfg'])

#plt.boxplot(df_consol_final)
#plt.xticks(['patient_number'], ['Achieved_Yield_from_Mfg'])

##df_consol_final.to_excel(r'/Users/gauravsharma/Documents/Simulation_results_3.xls') 

plt.figure()
Plot8 = df_consol_final.plot.hexbin(x='patient_number', y='Achieved_Yield_from_Mfg', gridsize=25)
fig8 = Plot8.get_figure()
plt.show()

#from pandas.plotting import scatter_matrix 
#scatter_matrix([df_consol_final.patient_number,df_consol_final.Achieved_Yield_from_Mfg], alpha=0.2, figsize=(6, 6), diagonal='kde')

plt.figure()
sns.set_style("whitegrid") 
Plot9 = sns.boxplot(x = 'patient_number', y = 'Achieved_Yield_from_Mfg', data = df_consol_final, width=0.5, palette="colorblind")
plt.show()
fig9 = Plot9.get_figure()
fig9.savefig("Plot8.png")

Plot10 = stats.probplot(df_consol_final.Achieved_Yield_from_Mfg, dist="norm", plot=pylab)
fig10 = Plot10.get_figure()
pylab.show()

Plot1.savefig('Plot1.png')
Plot2.savefig('Plot2.png')
Plot3.savefig('Plot3.png')
Plot4.savefig('Plot4.png')
Plot5.savefig('Plot5.png')
Plot6.savefig('Plot6.png')
Plot7.savefig('Plot7.png')
Plot8.savefig('Plot8.png')
Plot9.savefig('Plot9.png')
Plot10.savefig('Plot10.png')

#fig1.savefig('Plot1.png')
#fig2.savefig('Plot2.png')
#fig3.savefig('Plot3.png')
#fig4.savefig('Plot4.png')
#fig5.savefig('Plot5.png')
#fig6.savefig('Plot6.png')
#fig7.savefig('Plot7.png')
#fig8.savefig('Plot8.png')
#fig9.savefig('Plot9.png')

##bplot = sns.stripplot(y='Achieved_Yield_from_Mfg', x='patient_number', data=df_consol_final, jitter=True, marker='o', alpha=0.5, color='black')
#
## output file name
#plot_file_name="boxplot_and_swarmplot_with_seaborn.jpg"
# 
## save as jpeg
##bplot.figure.savefig(plot_file_name, format='jpeg', dpi=1000)
#bplot1.figure.savefig(plot_file_name, format='jpeg', dpi=1000)
#
##df_consol_final.boxplot(by ='patient_number == 0', column =['Achieved_Yield_from_Mfg'], grid= False)