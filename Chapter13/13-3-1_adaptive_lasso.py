"""
Adptive-Lasso变量选择
"""
import numpy as np
import pandas as pd
inputfile = '../data/data1.csv'
data = pd.read_csv(inputfile)

#导入Adaptive-Lasso算法，要在较新的Scikit-learn才有
from sklearn.linear_model import Lasso
model = Lasso(alpha = 0.1)
model.fit(data.iloc[:,0:30],data['y'])
print(model.coef_)