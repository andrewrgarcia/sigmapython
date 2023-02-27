# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 23:21:28 2019

@author: garci
"""
'CONVERT SPSS FILES (.SAV) TO PYTHON DATAFRAME (LINE 12) PASS AS .CSV FILE (LINE 14)'

import pyreadstat
import pandas as pd

df, meta = pyreadstat.read_sav("example.sav")
#print(df)
df.to_csv('out.csv')