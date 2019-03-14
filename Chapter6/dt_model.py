
import pandas as pd
from random import shuffle      #导入随机函数shuffle，用来打算数据

datafile = '../data/model.xls'
data = pd.read_excel(datafile)
data = data.values   #将表格转换为矩阵
shuffle(data)   #随机打乱数据

p = 0.8     #设置训练数据比例
Train = data[:int(len(data)*p),:]       #前80%为训练集
test = data[int(len(data)*p):,:]        #后20%为测试集

#构建CART决策树模型
from sklearn.tree import DecisionTreeClassifier

treefile = '../tmp/tree.pkl'        #模型输出名字
tree = DecisionTreeClassifier()     #建立决策树模型
tree.fit(Train[:,:3],Train[:,3])    #训练

#保存模型
from sklearn.externals import joblib
joblib.dump(tree,treefile)

from cm_plot import *
cm_plot(Train[:,3],tree.predict(Train[:,:3])).show()
#注意到Scikit-Learn使用predict方法直接给出预测结果

from sklearn.metrics import roc_curve   #导入ROC曲线函数
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号

fpr,fqr,thresholds = roc_curve(test[:,3],tree.predict_proba(test[:,:3])[:,1],pos_label = 1)
plt.plot(fpr,fqr,linewidth = 2, label = 'ROC of CART')         #作出ROC曲线
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.ylim(0,1.05)
plt.xlim(0,1.05)
plt.legend(loc = 4)
plt.show()