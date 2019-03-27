from __future__ import division
import pandas as pd
import numpy as np
import re
from sqlalchemy import create_engine


#python 访问数据库
engine = create_engine('mysql+pymysql://root:1234567890@127.0.0.1:3306/test?charset=utf8')
sql = pd.read_sql('all_gzdata',engine,chunksize = 10000)

def clickfreq(i):
    j = i[['fullURL','fullURLId','realIP']][i['fullURL'].str.contains('\.html')]
    return j

counts1 = [clickfreq(i) for i in sql]
counts1 = pd.concat(counts1)

counts1_ = counts1['fullURL'].value_counts()
counts1_ = pd.DataFrame(counts1_)
counts1_.columns = [u'点击次数']
counts1_.index.name = u'网址'
counts1_a = counts1_.sort_values(u'点击次数',ascending= False).iloc[:20,:]
print(counts1_a)

#获取网页点击排名数筛选出点击次数大于50的网址
counts1_b = counts1_.reset_index()
counts1_c = counts1_b[counts1_b[u'点击次数'] > 50][counts1_b[u'网址'].str.contains('/\d+?_*\d+?\.html')]
counts1_c.set_index(u'网址', inplace = True)
counts1_c.sort_index(inplace = True)
print(counts1_c)

#翻页网页统计，对浏览网页翻页的情况进行统计
pattern = re.compile('http://(.*\d+?)_\w+_\w+_\.html$|http://(.*\d+?)_\w+_\.html$|http://(.*\w+?).html$',re.S)
counts1_c['websitemain'] = np.nan
for i in range(len(counts1_c)):
    items = re.findall(pattern,counts1_c.index[i])
    if len(items) == 0:
        temp = np.nan
    else:
        for j in items[0]:
            if j !='':
                temp = j
    counts1_c.iloc[i,1] = temp
print(counts1_c)

#获取所有网页主体的网页数
counts1_d = counts1_c['websitemain'].value_counts()
counts1_d = pd.DataFrame(counts1_d)
print(counts1_d)

#统计网页主体出现次数为不少于2次的，即存在翻页的网址
counts1_e = counts1_d[counts1_d['websitemain'] >= 2]
counts1_e.columns = ['Times']                                   #记录某网页及子网页出现的次数
counts1_e.index.name = 'websitemain'

counts1_e['num'] = np.arange(1,len(counts1_e)+1)
counts1_f = pd.merge(counts1_c,counts1_e,left_on = 'websitemain', right_index = True, how = 'right')
counts1_f.sort_index(inplace = True)
counts1_f['per'] = np.nan
print(counts1_f)

#统计翻子页的点击率与上一页点击率的比重（注意：网页翻页后序号有10页以上的合适）
def getper(x):
    x.sort_index(inplace = True)
    for i in range(len(x)-1):
        x.iloc[i+1,-1] = x.iloc[i+1,0]//x.iloc[i,0]
    return x
result = pd.DataFrame([])
for i in range(1,counts1_f['num'].max()+1):
    counts1_k = getper(counts1_f[counts1_f['num'] == i])
    result = pd.concat([result,counts1_k])                      #每次进行一次操作

counts1_f['Times'].value_counts()
flipPageResult = result[result['Times'] < 10]
flipPageResult.to_excel('../tmp/1_3_1flipPageResult.xlsx')
print(flipPageResult)