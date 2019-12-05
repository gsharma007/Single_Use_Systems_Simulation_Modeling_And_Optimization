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
from statsmodels.graphics.factorplots import interaction_plot


df_consol_final = pd.DataFrame() 

replication = 0
for compa in range(0,3):    
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
# =============================================================================
# plt.figure()
# Plot1 = df_consol_final.boxplot(column=['Achieved_Yield_from_Mfg'], notch= True, usermedians= None)
# #result = [item.get_ydata() for item in Plot1['whiskers']]
# quartiles = np.percentile(df_consol_final.Achieved_Yield_from_Mfg, [25, 50, 75])
# #data_min, data_max = df_consol_final.min(), df_consol_final.max()
# print('5_number_summary', quartiles)
# #print('data_min', data_min, 'data_max', data_max)
# plt.show()
# 
# plt.figure()
# Plot1 = df_consol_final.boxplot(by ='run', column =['Achieved_Yield_from_Mfg'], grid= False, rot=90, fontsize=5)
# plt.show()
# 
# plt.figure()
# Plot2 = df_consol_final.boxplot(by ='run', column =['diff_exp_achvd_yield_mfg'], grid= False, rot=90, fontsize=5)
# fig2 = Plot2.get_figure()
# plt.show()
# 
# plt.figure()
# # Construct the colormap
# from matplotlib.colors import ListedColormap
# current_palette = sns.color_palette("muted", n_colors=5)
# cmap = ListedColormap(sns.color_palette(current_palette).as_hex())
# N=90000
# colors = np.random.randint(0,5,N)
# Plot3 = plt.scatter(df_consol_final.run, df_consol_final.Achieved_Yield_from_Mfg, c=colors, cmap=cmap)
# fig3 = Plot3.get_figure()
# plt.show()
# 
# plt.figure()
# # Construct the colormap
# from matplotlib.colors import ListedColormap
# current_palette = sns.color_palette("muted", n_colors=5)
# cmap = ListedColormap(sns.color_palette(current_palette).as_hex())
# N=90000
# colors = np.random.randint(0,5,N)
# Plot4 = plt.scatter(df_consol_final.run, df_consol_final.diff_exp_achvd_yield_mfg, c=colors, cmap=cmap)
# plt.show()
# 
# =============================================================================
#plt.figure()
#plt.boxplot(['patient_number','Achieved_Yield_from_Mfg'])

#plt.boxplot(df_consol_final)
#plt.xticks(['patient_number'], ['Achieved_Yield_from_Mfg'])



# =============================================================================
# plt.figure()
# Plot5 = df_consol_final.plot.hexbin(x='run', y='Achieved_Yield_from_Mfg', gridsize=25)
# plt.show()
# 
# #from pandas.plotting import scatter_matrix 
# #scatter_matrix([df_consol_final.patient_number,df_consol_final.Achieved_Yield_from_Mfg], alpha=0.2, figsize=(6, 6), diagonal='kde')
# 
# plt.figure()
# sns.set_style("whitegrid") 
# Plot6 = sns.boxplot(x = 'run', y = 'Achieved_Yield_from_Mfg', data = df_consol_final, width=0.5, palette="colorblind")
# plt.show()
# 
# plt.figure()
# sns.set_style("whitegrid") 
# Plot7 = sns.boxplot(x = 'run', y = 'diff_exp_achvd_yield_mfg', data = df_consol_final, width=0.5, palette="colorblind")
# plt.show()
# 
# =============================================================================

#Plot1.figure.savefig('Plot1.png')
#Plot2.figure.savefig('Plot2.png')
#Plot3.figure.savefig('Plot3.png')
#Plot4.figure.savefig('Plot4.png')
#Plot5.figure.savefig('Plot5.png')
#Plot6.figure.savefig('Plot6.png')
#Plot7.figure.savefig('Plot7.png')
#Plot8.figure.savefig('Plot8.png')
#Plot9.figure.savefig('Plot9.png')
#Plot10.figure.savefig('Plot10.png')



#DOE Plots

#DOE_Plot1 = stats.probplot(df_consol_final.Machine_Count, dist="norm", plot=pylab)
#pylab.show()
#
#DOE_Plot2 = stats.probplot(df_consol_final.Operators_Count, dist="norm", plot=pylab)
#pylab.show()
#
#DOE_Plot3 = stats.probplot(df_consol_final.Product_mix, dist="norm", plot=pylab)
#pylab.show()
#
#DOE_Plot4 = stats.probplot(df_consol_final.Achieved_Yield_from_Mfg, dist="norm", plot=pylab)
#pylab.show()
#
#DOE_Plot5 = stats.probplot(df_consol_final.diff_exp_achvd_yield_mfg, dist="norm", plot=pylab)
#pylab.show()
#
#DOE_Plot6_1 = df_consol_final.boxplot(by ='Machine_Count', column =['Achieved_Yield_from_Mfg'], grid= False, fontsize=5)
#plt.show()
#DOE_Plot6_2 = sns.boxplot(x = 'Machine_Count', y = 'Achieved_Yield_from_Mfg', data = df_consol_final, width=0.5, palette="colorblind")
#plt.show()
#
#DOE_Plot7_1 = df_consol_final.boxplot(by ='Operators_Count', column =['Achieved_Yield_from_Mfg'], grid= False, fontsize=5)
#plt.show()
#DOE_Plot7_2 = sns.boxplot(x = 'Operators_Count', y = 'Achieved_Yield_from_Mfg', data = df_consol_final, width=0.5, palette="colorblind")
#plt.show()
#
#DOE_Plot8_1 = df_consol_final.boxplot(by ='Product_mix', column =['Achieved_Yield_from_Mfg'], grid= False, fontsize=5)
#plt.show()
#DOE_Plot8_2 = sns.boxplot(x = 'Product_mix', y = 'Achieved_Yield_from_Mfg', data = df_consol_final, width=0.5, palette="colorblind")
#plt.show()
#
#DOE_Plot9 = interaction_plot(df_consol_final.Machine_Count,df_consol_final.Operators_Count, df_consol_final.Achieved_Yield_from_Mfg, ms=10)
#plt.show()
#
#DOE_Plot10 = interaction_plot(df_consol_final.Machine_Count,df_consol_final.Product_mix, df_consol_final.Achieved_Yield_from_Mfg, ms=10)
#plt.show()
#
#DOE_Plot11 = interaction_plot(df_consol_final.Operators_Count,df_consol_final.Product_mix, df_consol_final.Achieved_Yield_from_Mfg, ms=10)
#plt.show()

#DOE_Plot6 = interaction_plot(df_consol_final.Operators_Count,df_consol_final.Achieved_Yield_from_Mfg, colors=['red','blue'], markers=['D','^'], ms=10)
#plt.show()

#DOE_Plot7 = interaction_plot(df_consol_final.Product_mix,df_consol_final.Achieved_Yield_from_Mfg, colors=['red','blue'], markers=['D','^'], ms=10)
#plt.show()


sns.set_style("darkgrid")
# Draw a pointplot to show response as a function of three categorical factors
DOE_Plot12 = sns.catplot(x="Machine_Count", y="Achieved_Yield_from_Mfg", hue="Operators_Count", col="Product_mix",
                capsize=.2, palette="husl", height=3, aspect=0.6,
                kind="point", data=df_consol_final)
DOE_Plot12.despine(left=True)
plt.show()
#DOE_Plot12.figure.savefig('DOE_Plot12.png')

DOE_Plot13 = sns.catplot(x="Machine_Count", y="Achieved_Yield_from_Mfg", hue="Operators_Count", col="Product_mix",
                capsize=.2, palette="hls", height=3, aspect=0.60,
                kind="point", data=df_consol_final)

DOE_Plot14 = sns.catplot(x="Machine_Count", y="Achieved_Yield_from_Mfg", hue="Operators_Count", col="Product_mix",
                capsize=.2, palette="Paired", height=3, aspect=0.60,
                kind="point", data=df_consol_final)

DOE_Plot15 = sns.catplot(x="Machine_Count", y="Achieved_Yield_from_Mfg", hue="Operators_Count", col="Product_mix",
                capsize=.2, palette="Set2", height=3, aspect=0.60,
                kind="point", data=df_consol_final)
plt.show()

DOE_Plot16 = sns.catplot(x="Machine_Count", y="Achieved_Yield_from_Mfg", hue="Operators_Count", col="Product_mix", palette="husl", height=4, aspect=0.50,
                kind="box", data=df_consol_final)
plt.show()

DOE_Plot17 = sns.catplot(x="Machine_Count", y="Achieved_Yield_from_Mfg", hue="Operators_Count", col="Product_mix", palette="husl", height=4, aspect=0.50,
                kind="bar", data=df_consol_final)
#DOE_Plot16.set(ylim=(80000, 150000))
plt.show()

sns.set_style("ticks")

DOE_Plot18 = sns.catplot(x="Machine_Count", y="Achieved_Yield_from_Mfg", hue="Operators_Count", col="Product_mix",
                capsize=.2, palette="Set2", height=3, aspect=0.60,
                kind="point", data=df_consol_final)

DOE_Plot19 = sns.catplot(x="Machine_Count", y="Achieved_Yield_from_Mfg", hue="Operators_Count", col="Product_mix",
                capsize=.2, palette="husl", height=3, aspect=0.6,
                kind="point", data=df_consol_final)
DOE_Plot19.despine(left=True)
plt.show()
#DOE_Plot12.figure.savefig('DOE_Plot12.png')

DOE_Plot20 = sns.catplot(x="Machine_Count", y="Achieved_Yield_from_Mfg", hue="Operators_Count", col="Product_mix",
                capsize=.2, palette="hls", height=3, aspect=0.60,
                kind="point", data=df_consol_final)
plt.show()

DOE_Plot21 = sns.catplot(x="Machine_Count", y="Achieved_Yield_from_Mfg", hue="Operators_Count", col="Product_mix",
                capsize=.2, palette="Paired", height=3, aspect=0.60,
                kind="point", data=df_consol_final)

DOE_Plot22 = sns.catplot(x="Machine_Count", y="Achieved_Yield_from_Mfg", hue="Operators_Count", col="Product_mix", palette="husl", height=4, aspect=0.50,
                kind="box", data=df_consol_final)
plt.show()

DOE_Plot23 = sns.catplot(x="Machine_Count", y="Achieved_Yield_from_Mfg", hue="Operators_Count", col="Product_mix", palette="husl", height=4, aspect=0.50,
                kind="bar", data=df_consol_final)


# =============================================================================
# custom_palette = ["red","green","orange","blue","yellow","purple"]
# sns.set_palette(custom_palette)
# DOE_Plot18 = sns.catplot(x="Machine_Count", y="Achieved_Yield_from_Mfg", hue="Operators_Count", col="Product_mix",
#                 capsize=.2, palette="custom_palette", height=3, aspect=0.60,
#                 kind="point", data=df_consol_final)
# =============================================================================
#DOE_Plot16.set(ylim=(80000, 150000))

# =============================================================================
# from pandas.plotting import scatter_matrix
# DOE_Plot13 = scatter_matrix(df_consol_final[['Machine_Count', 'Operators_Count', 'Product_mix','Achieved_Yield_from_Mfg']], diagonal= 'kde')
# plt.show()
# =============================================================================

# from pandas.tools import plotting
# DOE_Plot13 = plotting.scatter_matrix(df_consol_final[['Machine_Count', 'Operators_Count', 'Product_mix','Achieved_Yield_from_Mfg']], diagonal= 'hist')
# plt.show()
# =============================================================================

df_consol_final.to_csv(r'/Users/gauravsharma/Documents/Simulation_results_5.csv')

#DOE_Plot14 = sns.residplot(df_consol_final[['Machine_Count', 'Operators_Count', 'Product_mix']], df_consol_final[['Achieved_Yield_from_Mfg']], lowess=True, color="g")
#plt.show()


#DOE_Plot1.figure.savefig('DOE_Plot1.png')
#DOE_Plot2.figure.savefig('DOE_Plot2.png')
#DOE_Plot3.figure.savefig('DOE_Plot3.png')
#DOE_Plot4.figure.savefig('DOE_Plot4.png')
#DOE_Plot5.figure.savefig('DOE_Plot5.png')
DOE_Plot12.savefig('DOE_Plot12.png')
DOE_Plot13.savefig('DOE_Plot13.png')
DOE_Plot14.savefig('DOE_Plot14.png')
DOE_Plot15.savefig('DOE_Plot15.png')
DOE_Plot16.savefig('DOE_Plot16.png')
DOE_Plot17.savefig('DOE_Plot17.png')
DOE_Plot18.savefig('DOE_Plot18.png')
DOE_Plot19.savefig('DOE_Plot19.png')
DOE_Plot20.savefig('DOE_Plot20.png')
DOE_Plot21.savefig('DOE_Plot21.png')
DOE_Plot22.savefig('DOE_Plot22.png')
DOE_Plot23.savefig('DOE_Plot23.png')

#df_consol_final.to_excel(r'/Users/gauravsharma/Documents/Simulation_results_3.xls') 

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
#df_consol_final.boxplot(by ='patient_number == 0', column =['Achieved_Yield_from_Mfg'], grid= False)