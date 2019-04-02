"""
企业所得税神经网络预测模型
"""
import numpy as np
import pandas as pd

inputfile = '../temp/data4_GM11.xlsx'
outputfile = '../temp/enterprise_income.xlsx'
modelfile = '../temp/4-net.model'
data = pd.read_excel(inputfile)
feature = ['x1','x2','x3','x4','x6','x7','x9','x10']

data_train = data.loc[list(range(2002,2014))].copy()
data_mean = data_train.mean()
data_std = data_train.std()
data_train = (data_train - data_mean)/data_std
x_train = data_train[feature].values
y_train = data_train['y'].values

from keras.models import Sequential
from keras.layers.core import Dense,Activation

model = Sequential()
model.add(Dense(input_dim=8,units=6))
model.add(Activation('relu'))
model.add((Dense(input_dim=6,units=1)))
model.compile(loss='mean_squared_error',optimizer='adam')
model.fit(x_train,y_train,nb_epoch=5000,batch_size=16)
model.save_weights(modelfile)

#预测
x = ((data[feature] - data_mean[feature])/data_std[feature]).values
data[u'y_pred'] = model.predict(x)*data_std['y'] + data_mean['y']
data[u'y_pred'] = data[u'y_pred'].round()
data.to_excel(outputfile)

import matplotlib.pyplot as plt
p = data[['y','y_pred']].plot(subplots = True, style = ['b-o','r-*'])
plt.savefig('../temp/yuce4.png')
plt.show()