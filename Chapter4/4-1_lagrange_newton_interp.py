import pandas as pd
from scipy.interpolate import lagrange #导入拉格朗日插值函数

inputfile =  'data/catering_sale.xls'
outputfile = 'tmp/sale.xls'

data = pd.read_excel(inputfile)
data[u'销量'][(data[u'销量'] < 400) | (data[u'销量'] > 5000)] = None

def ployinterp_column(s,n,k=5):
    y = s[list(range(n-k,n)) + list(range(n+1,n+1+k))]
    y = y[y.notnull()]
    return lagrange(y.index,list(y))(n)

for i in data.columns:
    for j in range(len(data)):
        if (data[i].isnull())[j]:
            data[i][j] = ployinterp_column(data[i],j)

data.to_excel(outputfile)