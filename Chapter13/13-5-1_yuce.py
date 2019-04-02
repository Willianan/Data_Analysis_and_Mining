"""
地方财政收入神经网络预测模型
"""

import pandas as pd

inputfile = '../temp/data1_GM11.xlsx'
outputfile = '../data/revenue.xls'
modelfile = '../temp/1-net.model'

data = pd.read_excel(inputfile)
feature = ['x1','x2','x3','x4','x5','x7']

data_train = data.loc[list(range(1994,2014))].copy()
data_mean = data_train.mean()
data_std = data_train.std()
data_train = (data_train - data_mean)/data_std                  #数据标准化
x_train = data_train[feature].values                            #特征数据
y_train = data_train['y'].values                                #标签数据

from keras.models import Sequential
from keras.layers.core import Dense,Activation

model = Sequential()                                            #建立模型
model.add(Dense(input_dim=6,units=12))
model.add(Activation('relu'))
model.add(Dense(input_dim=12,units=1))
model.compile(loss='mean_squared_error',optimizer='adam')      #编译模型
model.fit(x_train,y_train,nb_epoch=10000,batch_size=16)
model.save_weights(modelfile)                                  #保存模型参数

#预测
x = ((data[feature] - data_mean[feature])/data_std[feature]).values
data[u'y_pred'] = model.predict(x) * data_std['y'] + data_mean['y']
data.to_excel(outputfile)

#画出预测结果图
import matplotlib.pyplot as plt
p = data[['y','y_pred']].plot(subplots = True, style = ['b-o','r-*'])
plt.savefig('../temp/yuce1.png')
plt.show()