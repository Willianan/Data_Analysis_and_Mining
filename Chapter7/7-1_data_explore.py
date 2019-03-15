#对数据进行基本的探索
#返回缺失值个数以及最大最小值

import pandas as pd

datafile = '../data/air_data.csv'
resultfile = '../tmp/explore.xls'
data = pd.read_csv(datafile,encoding = 'utf-8')                 #读取原始数据，指定utf-8编码
explore = data.describe(percentiles = [], include = 'all').T    #包括对数据的基本描述
#percentiles参数指定计算多少的分位数表，T是转置，方便查阅
explore['null'] = len(data) - explore['count']                  #describe()函数自动计算非空值数

explore = explore[['null','max','min']]
explore.columns = [u'空值数',u'最大值',u'最小值']

explore.to_excel(resultfile)
