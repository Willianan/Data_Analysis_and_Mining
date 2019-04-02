"""
原始数据概括性度量
"""

#描述分析
import numpy as np
import pandas as pd

inputfile = '../data/data1.csv'
data = pd.read_csv(inputfile)
r = [data.min(),data.max(),data.mean(),data.std()]
r = pd.DataFrame(r,index=['Min','Max','Mean','STD'])           #计算相关系数矩阵
print(np.round(r,2).T)                                           #保留两位小数