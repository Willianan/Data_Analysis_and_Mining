#平稳性检验

import pandas as pd

#参数初始化
discfile = '../data/discdata_processed.xls'

data = pd.read_excel(discfile)
data = data.iloc[:len(data) - 5]        #不使用最后5个数据

#平稳性检测
from statsmodels.tsa.stattools import adfuller as ADF
diff = 0
adf = ADF(data['CWXT_DB:184:D:\\'])
while adf[1] >= 0.05:                   #adf[1]为p值，怕值小于0.05认为是平稳的
    diff = diff + 1
    adf = ADF(data['CWXT_DB:184:D:\\'].diff().dropna())

print(u'原始序列经过%s阶差分后归于平稳，p值为%s' %(diff,adf[1]))