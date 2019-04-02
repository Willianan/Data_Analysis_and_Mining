"""
地方财政收入灰色预测
"""

import numpy as np
import pandas as pd
from GM11 import *

inputfile = '../data/data1.csv'
outputfile = '../temp/data1_GM11.xlsx'
data = pd.read_csv(inputfile)
data.index = range(1994,2014)

data.loc[2014] = None
data.loc[2015] = None
l = ['x1','x2','x3','x4','x5','x7']
for i in l:
    f = GM11(data[i][list(range(1994,2014))].values)
    f = f[0]
    data[i][2014] = f(len(data) - 1)                        #2014年预测结果
    data[i][2015] = f(len(data))
    data[i] = data[i].round(2)

data[l+['y']].to_excel(outputfile)