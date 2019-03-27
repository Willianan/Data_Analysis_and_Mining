from __future__ import division
import pandas as pd
import numpy as np
import re
from sqlalchemy import create_engine


def savetoSQL(DF,tablename):
    import pandas as pd
    from sqlalchemy import create_engine
    yconnect = create_engine('mysql+pymysql://root:1234567890@127.0.0.1:3306/test?charset=utf8')
    pd.io.sql.to_sql(DF, tablename, yconnect, schema = 'test', if_exists ='append')


'''
删除12-4中的规则1，2，4
对网址的操作（只要.html结尾的 & 截取问号左边的值 & 只要包含主网址（lawtime）的 & 网址中间没有midques_的）
'''
#python 访问数据库
engine = create_engine('mysql+pymysql://root:1234567890@127.0.0.1:3306/test?charset=utf8')
sql = pd.read_sql('all_gzdata',engine,chunksize = 10000)

for i in sql:
    j = i[['realIP','fullURL','pageTitle','userID','timestamp_format']]     #只要网址列
    j = j[(j['fullURL'].str.contains('\.html'))].copy()                     #只含有.html的网址
    j.to_sql('cleaned_one',engine,index = False, if_exists = 'append')

'''
对网页标题的操作（删除 快车-律师助手 & 免费发布法律咨询 & 咨询发布成功 $ 法律快搜）
'''

#python 访问数据库
engine = create_engine('mysql+pymysql://root:1234567890@127.0.0.1:3306/test?charset=utf8')
sql = pd.read_sql('cleaned_one',engine,chunksize = 10000)

#对网址的操作
for i in sql:
    d = i[['realIP','fullURL','pageTitle','userID','timestamp_format']]
    d['pageTitle'].fillna(u'空',inplace = True)
    d = d[(d['pageTitle'].str.contains(u'快车-律师助手') == False) & (d['pageTitle'].str.contains(u'咨询发布成功') == False) & (d['pageTitle'].str.contains(u'免费发布法律咨询') == False) & (d['pageTitle'].str.contains(u'法律快搜') == False)].copy()
    d.to_sql('cleaned_two',engine,index = False, if_exists = 'append')


'''
删除重复记录
'''
#python 访问数据库
engine = create_engine('mysql+pymysql://root:1234567890@127.0.0.1:3306/test?charset=utf8')
sql = pd.read_sql('cleaned_two',engine,chunksize = 10000)

def dropduplicate(i):
    j = i[['realIP','fullURL','pageTitle','userID','timestamp_format']].copy()
    return j

counts6 = [dropduplicate(i) for i in sql]
counts6 = pd.concat(counts6)
print(len(counts6))
counts7 = counts6.drop_duplicates(['fullURL','userID','timestamp_format'])
print(len(counts7))
savetoSQL(counts7,'cleaned_three')

'''
查看删除操作后表中的总记录数
'''
#查看all_gzdata表中的记录数
#python 访问数据库
engine = create_engine('mysql+pymysql://root:1234567890@127.0.0.1:3306/test?charset=utf8')
sql = pd.read_sql('all_gzdata',engine,chunksize = 10000)
lens = 0
for i in sql:
    temp = len(i)
    lens = temp + lens
print(lens)

#查看cleaned_one表中的记录数
#python 访问数据库
engine = create_engine('mysql+pymysql://root:1234567890@127.0.0.1:3306/test?charset=utf8')
sql = pd.read_sql('cleaned_one',engine,chunksize = 10000)

lens1 = 0
for i in sql:
    temp = len(i)
    lens1 = temp + lens1
print(lens1)

#查看cleaned_two表中的记录数
#python 访问数据库
engine = create_engine('mysql+pymysql://root:1234567890@127.0.0.1:3306/test?charset=utf8')
sql = pd.read_sql('cleaned_two',engine,chunksize = 10000)

lens2 = 0
for i in sql:
    temp = len(i)
    lens2 = temp + lens1
print(lens2)

#查看cleaned_three表中的记录数
#python 访问数据库
engine = create_engine('mysql+pymysql://root:1234567890@127.0.0.1:3306/test?charset=utf8')
sql = pd.read_sql('cleaned_three',engine,chunksize = 10000)

lens3 = 0
for i in sql:
    temp = len(i)
    lens3 = temp + lens1
print(lens3)