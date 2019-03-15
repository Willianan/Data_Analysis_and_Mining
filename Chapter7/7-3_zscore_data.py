#标准差标准化

import pandas as pd

datafile = '../data/zscoredata.xls'
zscoredfile = '../tmp/zscoreddata.xls'

#标准化处理
data = pd.read_excel(datafile)
data = (data - data.mean(axis = 0)) / (data.std(axis = 0))
data.columns = ['Z' + i for i in data.columns]

data.to_excel(zscoredfile,index = False)