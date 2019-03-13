#shiyID3决策树算法预测销量高低

import pandas as pd

#参数初始化
filename = 'data/sales_data.xls'
data = pd.read_excel(filename,index_col=u'序号')

#数据是类别标签，转换为数据
#用1表示“好” “是” “高” 这三个属性，用-1表示“坏” “否” “低”
data[data == u'好'] = 1
data[data == u'是'] = 1
data[data == u'高'] = 1
data[data != 1] = -1
x = data.iloc[:,:3].values.astype(int)
y = data.iloc[:,3].values.astype(int)

from sklearn.tree import DecisionTreeClassifier as DTC
dtc = DTC(criterion='entropy')          #建立决策树模型，基于信息熵
dtc.fit(x,y)    #训练模型

#导入相关函数，可视化决策树
#到处是结果是一个dot文件，需要安装Graphviz才能将它转换为pdf或png格式
from sklearn.tree import export_graphviz
from sklearn.externals.six import StringIO
x = pd.DataFrame(x)
with open("tree.dot","w") as f:
    f = export_graphviz(dtc,feature_names=x.columns,out_file=f)
