"""
离差标准化
"""

#数据标准化到[0,1]

import pandas as pd

filename = '../data/business_circle.xls'
standardizefile = '../tmp/standardized.xlsx'

data = pd.read_excel(filename)
data = (data - data.min())/(data.max() - data.min())            #离差标准化
data = data.reset_index()

data.to_excel(standardizefile,index=False)