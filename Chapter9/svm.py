#水色图像的水质评价

#颜色矩：图像或图像区域的颜色信息进行处理
# import numpy as np
# import pandas as pd
# from sklearn import preprocessing
# from PIL import Image
# import os
#
#
# def PicManage(path, i):
#     pic = Image.open(path)
#     pic.c_x, pic.c_y = (int(i / 2) for i in pic.size)
#     box = (pic.c_x - 50, pic.c_y - 50, pic.c_x + 50, pic.c_y + 50)
#     # 从图片中提取中心100*100的子矩形
#     region = pic.crop(box)
#
#     # 切分RGB
#     r, g, b = np.split(np.array(region), 3, axis=2)
#
#     # 计算一阶矩
#     r_m1 = np.mean(r)
#     g_m1 = np.mean(g)
#     b_m1 = np.mean(b)
#
#     # 二阶矩
#     r_m2 = np.std(r)
#     g_m2 = np.std(g)
#     b_m2 = np.std(b)
#
#     # 三阶矩
#     r_m3 = np.mean(abs(r - r.mean()) ** 3) ** (1 / 3)
#     g_m3 = np.mean(abs(g - g.mean()) ** 3) ** (1 / 3)
#     b_m3 = np.mean(abs(b - b.mean()) ** 3) ** (1 / 3)
#
#     # 将数据标准化，区间在[-1,1]
#     typ = np.array([i])
#     arr = np.array([r_m1, g_m1, b_m1, r_m2, g_m2, b_m2, r_m3, g_m3, b_m3])
#     # df = pd.DataFrame(preprocessing.minmax_scale(arr,feature_range=(-1,1))).T
#     df = pd.DataFrame(arr).T
#     dn = pd.DataFrame(typ).T
#     return df, dn
#
#
# result = []
# type_result = []
# for i in os.listdir('./data/images'):
#     if i.endswith('.jpg'):
#         df, dn = PicManage('./data/images/' + i, int(i[0]))
#         result.append(df)
#         type_result.append(dn)
#
# data = pd.concat(result)
# typ = pd.concat(type_result)
# data = pd.DataFrame(preprocessing.normalize(data, norm='l2'))
# data['type'] = typ.values
# data.to_excel('../data/picData.xls', index=False)

#数据抽样
import pandas as pd
import numpy as np

inputfile = '../data/moment.csv'
outputfile1 = '../tmp/cm_train.xls'
outputfile2 = '../tmp/cm_test.xls'
data = pd.read_csv(inputfile,encoding = 'gbk')
data=data.take(np.random.permutation(len(data)))
data = data.values
k = 0.8                                             #设置训练数据比例

# from random import shuffle                          #引入随机函数
# shuffle(data)

data_train = data[:int(len(data)*k),:]              #选取前80%为训练数据
data_test = data[int(len(data)*k):,:]               #选取前20%为测试数据

#构建支持向量机模型
#构造特征和标签

x_train = data_train[:,2:]*30                       #放大特征
y_train = data_train[:,0].astype(int)
x_test = data_test[:,2:]*30
y_test = data_test[:,0].astype(int)

#导入模型相关的函数，建立并且训练模型
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
plt.savefig('../tmp/svm_result.png')
plt.show()
