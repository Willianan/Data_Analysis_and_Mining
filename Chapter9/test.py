#环境质量评估模型

import pandas as pd
import numpy as np

inputfile = '../data/12.xls'
outputfile1 = '../tmp/air_cm_train.xls'
outputfile2 = '../tmp/air_cm_test.xls'
data = pd.read_excel(inputfile)
data = data.take(np.random.permutation(len(data)))
data = data.values

k = 0.8

data_train = data[:int(len(data)*k),:]
data_test = data[int(len(data)*k):,:]

#构造特征和标签
x_train = data_train[:,2:]*30
y_train = data_train[:,0].astype(int)
x_test = data_test[:,2:]*30
y_test = data_test[:,0].astype(int)

#导入模型相关函数，建立并训练模型
from sklearn import svm
model = svm.SVC()
model.fit(x_train,y_train)
import pickle
pickle.dump(model,open('../data/svm.model','wb'))
#保存模型
#model = pickle.load(open('../tmp/svm.model','rb'))

#导入输出相关的库，生成混淆矩阵
from sklearn import metrics
cm_train = metrics.confusion_matrix(y_train,model.predict(x_train))         #训练样本的混淆矩阵
cm_test = metrics.confusion_matrix(y_test,model.predict(x_test))            #测试样本的混淆矩阵

#保存结果
pd.DataFrame(cm_train,index = range(1,6),columns = range(1,6)).to_excel(outputfile1)
pd.DataFrame(cm_test,index = range(1,6),columns = range(1,6)).to_excel(outputfile2)

import matplotlib.pyplot as plt
from plot_confusion_matrix import *
fig=plt.figure(figsize=(10,5))
ax=fig.add_subplot(121)
plot_confusion_matrix(cm_train,classes=range(5),title='Confusion matrix on train-set')
ax=fig.add_subplot(122)
plot_confusion_matrix(cm_test,classes=range(5),title='Confusion matrix on test-set')
plt.savefig('../tmp/air_quality_result1.png')
plt.show()
