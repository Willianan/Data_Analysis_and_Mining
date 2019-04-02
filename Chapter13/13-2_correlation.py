"""
原始数据求解Pearson相关系数
"""

#相关分析
import numpy as np
import pandas as pd
inputfile = '../data/data1.csv'
data = pd.read_csv(inputfile)
a = np.round(data.corr(method='pearson'),2)                     #计算相关系数矩阵，保留两位小数
print(a)