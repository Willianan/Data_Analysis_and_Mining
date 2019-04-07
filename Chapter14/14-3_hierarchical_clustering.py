"""
层次聚类算法
"""

import pandas as pd

standardizefile = '../data/standardized.xls'
k = 3                                               #聚类数
data = pd.read_excel(standardizefile,index_col=u'基站编号')

from sklearn.cluster import AgglomerativeClustering             #导入sklearn的层次聚类函数
model = AgglomerativeClustering(n_clusters = k, linkage = 'ward')
model.fit(data)

#详细输出原始数据及其类别
r = pd.concat([data,pd.Series(model.labels_,index=data.index)],axis=1)
r.columns = list(data.columns) + [u'聚类类别']                    #重命名表头

import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']                     #用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False                       #用来正常显示负号

style = ['ro-','go-','bo-']
xlabels = [u'工作日人均停留时间',u'凌晨人均停留时间',u'周末人均停留时间',u'日均人流量']
pic_output = '../tmp/type_'                                      #聚类图文件名前缀

for i in range(k):
    plt.figure()
    tmp = r[r[u'聚类类别'] == i].iloc[:,:4]                        #提取每一类
    for j in range(len(tmp)):
        plt.plot(range(1,5),tmp.iloc[j],style[i])

    plt.xticks(range(1,5),xlabels,rotation = 20)                #坐标标签
    plt.subplots_adjust(bottom=0.15)                            #调整底部
    plt.savefig(u'%s%s.png' %(pic_output,i))                    #保存图片
    plt.show()
