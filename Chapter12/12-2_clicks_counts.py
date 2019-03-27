#点击次数分析
#统计分析原始数据用户浏览网页次数的情况（以‘realIP’区分）

import pandas as pd
import numpy as np
from sqlalchemy import create_engine

#python 访问数据库
engine = create_engine('mysql+pymysql://root:1234567890@127.0.0.1:3306/test?charset=utf8')
sql = pd.read_sql('all_gzdata',engine,chunksize = 10000)

counts1 = [i['realIP'].value_counts() for i in sql]                     #分块统计各个IP出现的次数
counts1 = pd.concat(counts1).groupby(level = 0).sum()                   #合并统计结果，level=0表示按index分组

counts1_ = pd.DataFrame(counts1)
counts1_[1] = 1                                                         #添加一列全为1
IPcounts = counts1_.groupby('realIP').sum()                             #统计各个不同IP分别出现的次数
IPcounts.columns = [u'用户数']
IPcounts.index.name = u'点击次数'
IPcounts[u'用户百分比'] = (IPcounts[u'用户数']/IPcounts[u'用户数'].sum())*100
IPcounts[u'记录百分比'] = (IPcounts[u'用户数']*IPcounts.index/counts1_['realIP'].sum())*100
IPcounts.sort_index(inplace = True)
IPcountsB = IPcounts.iloc[:7,:]
IPcountsC = IPcountsB.T
print(IPcountsC)

#统计1~7次及7次以上的
IPcountsC.insert(0,u'总计',[IPcounts[u'用户数'].sum(),100,100])
IPcountsC[u'7次以上'] = IPcountsC.iloc[:,0] - IPcountsC.iloc[:,1:].sum(1)
IPcountsC.to_excel('../tmp/1_2_1clickTimes.xlsx')
print(IPcountsC)

IPcountsD = IPcountsC.T
format = lambda x: '%.2f' % x
#IPcountsD.round(4)
IPcountsD = IPcountsD.applymap(format)
#分析浏览次数7次以上的数据
Times = counts1_.index[7:]
bins = [7,100,1000,50000]
cats = pd.cut(Times,bins,right = True,labels = ['8~100','101~1000','1000以上'])
catscounts = cats.value_counts()
catscounts = pd.DataFrame(catscounts,columns = [u'用户数'])
catscounts.index.name = u'点击次数'
catscounts[u'用户数'] = np.nan
catscounts.loc[u'8~100',u'用户数'] = IPcounts.loc[8:100,:][u'用户数'].sum()
catscounts.loc[u'101~1000',u'用户数'] = IPcounts.loc[101:1000,:][u'用户数'].sum()
catscounts.loc[u'1000以上',u'用户数'] = IPcounts.loc[1001:,:][u'用户数'].sum()
catscounts.sort_values(by = u'用户数', ascending = False, inplace = True)
catscounts.reset_index(inplace = True)
print(catscounts)

#对浏览一次的用户行为进行分析
#获取浏览一次的所有数据
oneIP = counts1_[counts1_['realIP'] == 1]
del oneIP[1]
oneIP.columns = [u'点击次数']
oneIP.index.name = 'realIP'

#python 访问数据库
engine = create_engine('mysql+pymysql://root:1234567890@127.0.0.1:3306/test?charset=utf8')
sql = pd.read_sql('all_gzdata',engine,chunksize = 10000)

oneIPg = [i[['fullURLId','fullURL','realIP']] for i in sql]
oneIPg = pd.concat(oneIPg)
oneIPh = pd.merge(oneIP,oneIPg,right_on = 'realIP', left_index = True,how = 'left')
print(oneIPh)

#浏览一次的用户的网页类型ID分析
oneIPi = oneIPh['fullURLId'].value_counts()
oneIPi = pd.DataFrame(oneIPi)
oneIPi.rename(columns = {'fullURLId':u'个数'},inplace = True)
oneIPi.index.name = u'网页类型ID'
oneIPi[u'百分比'] = (oneIPi[u'个数']/oneIPi[u'个数'].sum())*100
oneIPi.to_excel('../tmp/1_2_2typeID.xlsx')
print(oneIPi)

#点击1次用户浏览网页统计
oneIPk = pd.DataFrame(oneIPh['fullURL'].value_counts())
oneIPk.index.name = u'网址'
oneIPk.columns = [u'点击数']
oneIPm = oneIPk[oneIPk[u'点击数'] > 100]
oneIPm.loc[u'其他',u'点击数'] = oneIPk[oneIPk[u'点击数'] <= 100][u'点击数'].sum()
oneIPm[u'百分比'] = (oneIPm[u'点击数']/oneIPm[u'点击数'].sum())*100
oneIPm.to_excel('../tmp/1_2_3lookMorethan100.xlsx')
print(oneIPm)