"""
个人所得税神经网络预测模型
"""

import pandas as pd

inputfile = '../temp/data5_GM11.xlsx'
outputfile = '../temp/personal_income.xlsx'
modelfile = '../temp/5-net.model'
data = pd.read_excel(inputfile)
feature = ['x1','x4','x5','x7']

data_train = data.loc[list(range(2000,2014))].copy()
data_mean = data_train.mean()
data_std = data_train.std()
data_train = (data_train - data_mean)/data_std
x_train = data_train[feature].values
y_train = data_train['y'].values

from keras.models import Sequential
from keras.layers.core import Dense,Activation

model = Sequential()
model.add(Dense(input_dim=4,units=8))
model.add(Activation('relu'))
model.add(Dense(input_dim=8,units=1))
model.compile(optimizer='adam',loss='mean_squared_error')
model.fit(x_train,y_train,batch_size=16,epochs=15000)
model.save_weights(modelfile)

#预测
x = ((data[feature] - data_mean[feature])/data_std[feature]).values
data[u'y_pred'] = model.predict(x)*data_std['y'] + data_mean['y']
data[u'y_pred'] = data[u'y_pred'].round()
data.to_excel(outputfile)

import matplotlib.pyplot as plt
p = data[['y','y_pred']].plot(subplots = True, style = ['b-o','r-*'])
plt.savefig('../temp/yuce5.png')
plt.show()