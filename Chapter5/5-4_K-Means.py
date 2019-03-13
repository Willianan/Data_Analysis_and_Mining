#使用K-Means算法聚类消费行为特征数据

import pandas as pd

#参数初始化
inputfile = 'data/consumption_data.xls'
outputfile = 'tmp/data_type.xls'
K = 3   #聚类的类别
iteration = 500    #聚类最大循环次数
data = pd.read_excel(inputfile,index_col='Id')
data_zs = 1.0*(data - data.mean())/data.std()   #数据标准化

from sklearn.cluster import KMeans
model = KMeans(n_clusters=K,n_jobs=4,max_iter=iteration)    #分为K类，并发数4
model.fit(data_zs)  #开始聚类

r1 = pd.Series(model.labels_).value_counts()    #统计各类别的数目
r2 = pd.DataFrame(model.cluster_centers_)       #找出聚类中心
r = pd.concat([r2,r1],axis=1)                   #横向连接，得到聚类中心对应的类别下的数目
r.columns = list(data.columns) + [u'类别数目']   #重命名表头
print(r)

#详细输出原始数据及其类别
r = pd.concat([data,pd.Series(model.labels_,index=data.index)],axis=1)  #详细输出每个样本对应的类别
r.columns = list(data.columns) + [u'聚类类别']   #重命名表头
r.to_excel(outputfile)

def density_plot(data,title):
    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    plt.figure()
    for i in range(len(data.iloc[0])):#逐列作图
        (data.iloc[:,i]).plot(kind = 'kde',label = data.columns[i],linewidth = 2)
    plt.ylabel(u'密度')
    plt.ylabel(u'人数')
    plt.title(u'聚类类别%s各属性的密度曲线' %title)
    plt.legend()
    return plt
def density_plot(data): #自定义作图函数
  import matplotlib.pyplot as plt
  plt.rcParams['font.sans-serif'] = ['SimHei'] #用来正常显示中文标签
  plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号
  p = data.plot(kind='kde', linewidth = 2, subplots = True, sharex = False)
  [p[i].set_ylabel(u'密度') for i in range(K)]
  plt.legend()
  return plt

pic_output = 'tmp/pd_' #概率密度图文件名前缀
for i in range(K):
  density_plot(data[r[u'聚类类别']==i]).savefig(u'%s%s.png' %(pic_output, i))