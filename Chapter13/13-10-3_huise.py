"""
营业税灰色预测
"""

import numpy as np
import pandas as pd
from GM11 import *

inputfile = '../data/data3.csv'
outputfile = '../temp/data3_GM11.xlsx'
data = pd.read_csv(inputfile)
data.index = range(1999,2014)

data.loc[2014] = None
data.loc[2015] = None
l = ['x3','x4','x6','x8']

for i in l:
    f = GM11(data[i][list(range(1999,2014))].values)
    f = f[0]
    data[i][2014] = f(len(data) - 1)
    data[i][2015] = f(len(data))
    data[i] = data[i].round()

data[l+['y']].to_excel(outputfile)