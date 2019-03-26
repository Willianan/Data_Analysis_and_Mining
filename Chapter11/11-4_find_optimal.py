#确定最佳p、d、p值

import pandas as pd

#参数初始化
discfile = '../data/discdata_processed.xls'
data = pd.read_excel(discfile,index_col = 'COLLECTTIME')
data = data.iloc[:len(data) - 5]
xdata = data['CWXT_DB:184:D:\\']

from statsmodels.tsa.arima_model import ARIMA

#定阶
pmax = int(len(data)/10)
qmax = int(len(data)/10)
bic_matrix = []             #bic矩阵
for p in range(pmax + 1):
    tmp = []
    for q in range(qmax + 1):
        try:
            tmp.append(ARIMA(xdata,(p,1,q)).fit().bic)
        except:
            tmp.append(None)
    bic_matrix.append(tmp)

bic_matrix = pd.DataFrame(bic_matrix).astype('float64')     #从中可以找出最小值

p,q = bic_matrix.stack().idxmin()           #先用stack展平，然后用idxmin找出最小值位置
print(u'BIC最小的p值和q值为：%s、%s' %(p,q))