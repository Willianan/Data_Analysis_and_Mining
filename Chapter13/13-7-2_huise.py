"""
增值税灰色预测
"""

import pandas as pd
import numpy as np
from GM11 import *

inputfile = '../data/data2.csv'
outputfile = '../temp/data2_GM11.xlsx'
data = pd.read_csv(inputfile)
data.index = range(1999,2014)

data.loc[2014] = None
data.loc[2015] = None
l = ['x1','x3','x5']

for i in l:
    f = GM11(data[i][list(range(1999,2014))].values)
    f = f[0]
    data[i][2014] = f(len(data) - 1)
    data[i][2015] = f(len(data))

data[l+['y']].to_excel(outputfile)