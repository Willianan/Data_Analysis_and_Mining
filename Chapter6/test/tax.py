#企业偷税漏税识别模型

import pandas as pd

#数据初始化
inputfile = '../data/corporate_tax_evasion.xls'
data = pd.read_excel(inputfile,index_col=0)

#数据探索
data_t = pd.DataFrame(data.groupby([data['销售模式'],data['输出']]).size()).unstack()[0]
data_t['异常比率'] = data_t['异常'] / data_t.sum(axis = 1)
data_t.sort_values('异常比率',ascending = False)

#异常比率直方图
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

plt.bar(range(len(data_t.index)),data_t['异常比率'],tick_label = data_t.index)
plt.xticks(rotation = 90)
plt.show()

#模型构建
#数据预处理
data['输出'] = data['输出'].replace('正常',1)
data['输出'] = data['输出'].replace('异常',0)
for m,n in enumerate(set(data['销售类型'])):
    data['销售类型'] = data['销售类型'].replace(n,m+1)
for m,n in enumerate(set(data['销售模式'])):
    data['销售模式'] = data['销售模式'].replace(n,m+1)

#训练集和测试集
from random import shuffle
data = data.values      #将数据转换为矩阵
shuffle(data)           #随机打乱数据

p = 0.8                 #设置训练数据比例
train = data[:int(len(data)*p),:]
test = data[int(len(data)*p):,:]

#LM神经网络模型
from keras.models import Sequential             #导入神经网络初始化函数
from keras.layers.core import Dense,Activation  #导入神经网络层函数、激活函数

netfile = '../tmp/net1.model'                   #构建的神经网络模型存储路径

net = Sequential()                              #建立神经网络
net.add(Dense(input_dim = 14, units = 10))      #添加输入层（14节点）到隐藏层（10节点）的连接
net.add(Activation('relu'))                     #隐藏层使用relu激活函数
net.add(Dense(input_dim = 10, units = 1))       #添加隐藏层（10节点）到输出层（1节点）的连接
net.add(Activation('sigmoid'))                  #输出层使用sigmoid激活函数
net.compile(loss = 'binary_crossentropy', optimizer = 'adam', metrics = ['accuracy'])   #编译模型，使用adam方法求解
net.fit(train[:,:14],train[:,14],epochs = 1000, batch_size = 1)                         #训练模型，循环1000次
net.save_weights(netfile)                       #保存模型

predict_result = net.predict_classes(train[:,:14]).reshape(len(train))                 #用训练集预测
predict_result_test = net.predict_classes(test[:,:14]).reshape(len(test))              #预测结果变形

from cm_plot import *                           #导入自行编写的混淆矩阵可视化函数
cm_plot(train[:,14],predict_result).show()
cm_plot(test[:,14],predict_result_test).show()

#CART决策树模型
from sklearn.tree import DecisionTreeClassifier #导入决策树模型

treefile = '../tmp/tree1.pkl'                   #训练模型保存路径
tree = DecisionTreeClassifier()                 #建立决策树模型
tree.fit(train[:,:14],train[:,14])              #训练模型

from sklearn.externals import joblib
joblib.dump(tree,treefile)
#混淆矩阵
cm_plot(train[:,14],tree.predict(train[:,:14])).show()
cm_plot(test[:,14],tree.predict(test[:,:14])).show()

#绘制ROC曲线
from sklearn.metrics import roc_curve           #导入ROC曲线函数
import matplotlib.pyplot as plt

#LM模型
predict_result_test = net.predict(test[:,:14]).reshape(len(test))
fpr,fqr,thresholds = roc_curve(test[:,14],predict_result_test,pos_label = 1)
plt.plot(fpr,fqr,linewidth = 2, label = 'ROC of LM',color = 'blue')

#CART模型
predict_result_test = tree.predict_proba(test[:,:14])[:,1]
fpr,fqr,thresholds1 = roc_curve(test[:,14],predict_result_test,pos_label = 1)
plt.plot(fpr,fqr,linewidth = 2, label = 'ROC of CART',color = 'green')

plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.xlim(0,1.05)
plt.ylim(0,1.05)
plt.legend(loc = 4)
plt.show()