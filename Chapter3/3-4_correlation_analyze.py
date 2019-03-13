#餐饮销量数据相关性分析
from __future__ import print_function
import pandas as pd

catering_sale = 'data/catering_sale_all.xls'
data = pd.read_excel(catering_sale,index_col = u'日期')

data.corr()
data.corr()[u'百合酱蒸凤爪']
data[u'百合酱蒸凤爪'].corr(data[u'翡翠蒸香茜饺'])