#用水事件划分

import pandas as pd

threshold = pd.Timedelta(minutes = 4)           #阈值为4分钟
inputfile = '../data/water_heater.xls'
outputfile = '../tmp/dividsequence.xls'

data = pd.read_excel(inputfile)
data[u'发生时间'] = pd.to_datetime(data[u'发生时间'],format = '%Y%m%d%H%M%S')
data = data[data[u'水流量'] > 0]
d = data[u'发生时间'].diff() > threshold           #相邻时间作差分，比较是否大于阈值
data[u'事件编号'] = d.cumsum() + 1                 #通过累积求和的方式为事件编号

data.to_excel(outputfile)