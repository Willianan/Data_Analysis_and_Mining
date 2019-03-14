
import pandas as pd
from random import shuffle      #导入随机函数shuffle，用来打算数据

datafile = '../data/model.xls'
data = pd.read_excel(datafile)
data = data.values   #将表格转换为矩阵
shuffle(data)   #随机打乱数据

p = 0.8     #设置训练数据比例
Train = data[:int(len(data)*p),:]       #前80%为训练集
test = data[int(len(data)*p):,:]        #后20%为测试集

#构建LM神经网络模型
from keras.models import Sequential                 #导入神经网络初始化函数
from keras.layers.core import Dense,Activation      #导入神经网络层函数、激活函数

netfile = '../tmp/net.model'                        #构建的神经网络模型存储路径

net = Sequential()                                  #建立神经网络
net.add(Dense(input_dim = 3, units = 10))      #添加输入层（3节点）到隐藏层（10节点）的连接
net.add(Activation('relu'))                          #隐藏层使用relu激活函数
net.add(Dense(input_dim = 10,units = 1))       #添加隐藏层（10节点）到输出层（1节点）的连接
net.add(Activation('sigmoid'))                      #输出层使用sigmoid激活函数
net.compile(loss = 'binary_crossentropy' , optimizer = 'adam', metrics=['accuracy'])        #编译模型，使用adam方法求解

net.fit(Train[:,:3],Train[:,3], epochs = 1000, batch_size = 1)            #训练模型，循环1000次
net.save_weights(netfile)                                                   #保存模型

predict_result = net.predict_classes(Train[:,:3]).reshape(len(Train))       #预测结果变形

from cm_plot import *       #导入自行编写的混淆矩阵可视化函数
cm_plot(Train[:,3],predict_result).show()

from sklearn.metrics import roc_curve   #导入ROC曲线函数
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号

predict_result = net.predict(test[:,:3]).reshape(len(test))
fpr,fqr,thresholds = roc_curve(test[:,3],predict_result,pos_label = 1)
plt.plot(fpr,fqr,linewidth = 2, label = 'ROC of LM')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.xlim(0,1.05)
plt.ylim(0,1.05)
plt.legend(loc = 4)
plt.show()