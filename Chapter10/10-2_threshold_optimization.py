#阈值寻优

import pandas as pd
import numpy as np

inputfile = '../data/water_heater.xls'
n = 4                                   #使用以后四个点的平均斜率

threshold = pd.Timedelta(minutes = 5)   #专家阈值
data = pd.read_excel(inputfile)
data[u'发生时间'] = pd.to_datetime(data[u'发生时间'], format = '%Y%m%d%H%M%S')
data = data[data[u'水流量'] > 0]

def event_num(ts):
    d = data[u'发生时间'].diff() > ts    #相邻时间作差分，比较是否大于阈值
    return d.sum() + 1                  #直接返回事件数

dt = [pd.Timedelta(minutes = i) for i in np.arange(1,9,0.25)]
h = pd.DataFrame(dt,columns = [u'阈值'])               #定义阈值列
h[u'事件数'] = h[u'阈值'].apply(event_num)              #计算每个阈值对应的事件数
h[u'斜率'] = h[u'事件数'].diff() / 0.25                 #计算每两个相邻点对应的斜率
h[u'斜率指标'] = pd.DataFrame(h[u'斜率'].abs()).rolling(n).mean()         #采用后n个的斜率绝对值平均作为斜率指标
ts = h[u'阈值'][h[u'斜率指标'].idxmin() - n]            #注：用idxmin返回最小值的Index，由于pd.DataFrame.rolling().mean()
#自动计算的是前n个斜率的绝对值平均，所以结果有要进行平移（-n）

if ts > threshold:
    ts = pd.Timedelta(minutes = 4)

print(ts)