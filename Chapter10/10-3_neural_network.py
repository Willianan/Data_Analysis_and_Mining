#建立、训练多层神经网络，并完成模型的检验

from __future__ import print_function
import pandas as pd

inputfile1 = '../data/train_neural_network_data.xls'
inputfile2 = '../data/test_neural_network_data.xls'
testoutputfile ='../tmp/test_output_data.xls'

data_train = pd.read_excel(inputfile1)
data_test = pd.read_excel(inputfile2)

#训练样本标签
y_train = data_train.iloc[:,4].values
x_train = data_train.iloc[:,5:17].values
#测试样本标签
y_test = data_test.iloc[:,4].values
x_test = data_test.iloc[:,5:17].values

from keras.models import Sequential
from keras.layers.core import Dense,Dropout,Activation

model = Sequential()                                        #建立模型
model.add(Dense(input_dim = 11,units = 17))                 #添加输入层，隐藏层的连接
model.add(Activation('relu'))                               #Relu函数为激活函数
model.add(Dense(input_dim = 17,units = 10))                 #添加隐藏层、隐藏层连接
model.add(Activation('relu'))
model.add(Dense(input_dim = 10, units = 1))                 #添加隐藏层、输出层的连接
model.add(Activation('sigmoid'))                            #sigmoid函数为激活函数
#编译模型，损失函数为binary_crossentropy，用adam法求解
model.compile(loss = 'binary_crossentropy', optimizer = 'adam',metrics = ['accuracy'])

model.fit(x_train,y_train,epochs = 100, batch_size = 1)     #训练模型
model.save_weights('../tmp/net.model')                    #保存模型参数

r = pd.DataFrame(model.predict_classes(x_test),columns = [u'预测结果'])
pd.concat([data_test.iloc[:,:5],r], axis = 1).to_excel(testoutputfile)
model.predict(x_test)