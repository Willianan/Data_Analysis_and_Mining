#白噪声检验

import pandas as pd

#参数初始化
discfile = '../data/discdata_processed.xls'

data = pd.read_excel(discfile)
data = data.iloc[:len(data) - 5]

#白噪声检验
from statsmodels.stats.diagnostic import acorr_ljungbox

[[lb],[p]] = acorr_ljungbox(data['CWXT_DB:184:D:\\'],lags = 1)
if p < 0.05:
    print(u'原始序列为非白噪声序列，对应的p值为 %s' %p)
else:
    print(u'原始序列为白噪声序列，对应的p值为 %s' %p)

[[lb],[p]] = acorr_ljungbox(data['CWXT_DB:184:D:\\'].diff().dropna(),lags = 1)
if p < 0.05:
    print(u'一阶差分序列为非白噪声序列，对应的p值为: %s' %p)
else:
    print(u'一阶差分序列为白噪声序列，对应的p值为: %s' % p)