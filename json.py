#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 20:32:08 2019

@author: gauravsharma
"""

import pandas as pd
df_1 = pd.read_json('/Users/gauravsharma/cases.2019-11-03.json')
df_1.to_excel('new_file_1.xlsx')


df_2 = pd.read_json('/Users/gauravsharma/biospecimen.cases_selection.2019-11-03.json')
df_2.to_excel('new_file_2.xlsx')



