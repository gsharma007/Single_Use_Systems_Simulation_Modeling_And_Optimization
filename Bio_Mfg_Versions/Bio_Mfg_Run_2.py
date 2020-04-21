#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 06:58:27 2020

@author: gauravsharma
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Bio_Mfg_21 import function_2
import seaborn as sns
import scipy.stats as stats
import pylab
from statsmodels.graphics.factorplots import interaction_plot

df_consol_final = pd.DataFrame()

replication = 0
for compa in range(0,5):
    replication+=1
    df = function_2()
    df['replication'] = replication
    df['patient_number'] = df.index
    df_consol_final = df_consol_final.append(df)
    print("iteration number",compa)
    

df_consol_final.to_csv(r'/Users/gauravsharma/Documents/Simulation_Results_V1.csv')