"""
Adaptive-lasso变量选择
"""

import pandas as pd

inputfile = '../data/data2.csv'
data = pd.read_csv(inputfile)

#导入Adaptive-Lasso算法
from sklearn.linear_model import Lasso
model = Lasso(alpha=0.1)
model.fit(data.iloc[:,0:6],data['y'])
print(model.coef_)