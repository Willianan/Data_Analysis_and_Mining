"""
谱系聚类图
"""

import pandas as pd

standardizefile = '../data/standardized.xls'
data = pd.read_excel(standardizefile,index_col=u'基站编号')

import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage,dendrogram
#使用scipy的层次聚类函数

Z = linkage(data,method='ward',metric='euclidean')  #谱系层次图
p = dendrogram(Z,0)
plt.savefig('../tmp/1.png')
plt.show()