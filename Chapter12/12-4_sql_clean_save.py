#数据清洗

from __future__ import division
import pandas as pd
import numpy as np
import re
from sqlalchemy import create_engine

'''
删除规则1：统计中间类型网页（带midques_关键字）
'''
#python 访问数据库
engine = create_engine('mysql+pymysql://root:1234567890@127.0.0.1:3306/test?charset=utf8')
sql = pd.read_sql('all_gzdata',engine,chunksize = 10000)

def countmidques(i):
    j = i[['fullURL','fullURLId','realIP']].copy()
    j['type'] = u'非中间类型网页'
    j['type'][j['fullURL'].str.contains('midques_')] = u'中间类型网页'
    return j['type'].value_counts()
counts1 = [countmidques(i) for i in sql]
counts1 = pd.concat(counts1).groupby(level = 0).sum()
print(counts1)

'''
删除规则2：主网址去掉无.html点击行为的用户记录
'''
#python 访问数据库
engine = create_engine('mysql+pymysql://root:1234567890@127.0.0.1:3306/test?charset=utf8')
sql = pd.read_sql('all_gzdata',engine,chunksize = 10000)

def counthtml(i):
    j = i[['fullURL','pageTitle','fullURLId']].copy()
    j['type'] = u'有html页面'
    j['type'][j['fullURL'].str.contains('\.html') == False] = u'无.html点击行为的用户记录'
    return j['type'].value_counts()
counts2 = [counthtml(i) for i in sql]
counts2 = pd.concat(counts2).groupby(level = 0).sum()
print(counts2)

'''
删除规则3:</strong>主网页是律师的浏览信息网页（快车-律师助手）、咨询发布成功、快搜免费发布法律
备注：此规则中要删除的记录的网址均不含有.html，所有规则3需要过滤的信息也包含咯规则2中需要过滤的
'''
#python 访问数据库
engine = create_engine('mysql+pymysql://root:1234567890@127.0.0.1:3306/test?charset=utf8')
sql = pd.read_sql('all_gzdata',engine,chunksize = 10000)

def countothers(i):
    j = i[['fullURL','pageTitle','fullURLId']].copy()
    j['type'] = u'其他'
    j['pageTitle'].fillna(u'空',inplace = True)
    j['type'][j['pageTitle'].str.contains(u'快车-法律助手')] = u'快车-法律助手'
    j['type'][j['pageTitle'].str.contains(u'咨询发布成功')] = u'咨询发布成功'
    j['type'][j['pageTitle'].str.contains(u'免费发布法律咨询') | j['pageTitle'].str.contains(u'法律快搜')] = u'快搜免费发布法律咨询'
    return j['type'].value_counts()
counts3 = [countothers(i) for i in sql]
counts3 = pd.concat(counts3).groupby(level = 0).sum()
print(counts3)

'''
删除规则4：去掉网址中问号后面的部分，截取问号前面的部分；去掉主网址不包含关键字
'''

#python 访问数据库
engine = create_engine('mysql+pymysql://root:1234567890@127.0.0.1:3306/test?charset=utf8')
sql = pd.read_sql('all_gzdata',engine,chunksize = 10000)

def deletequesafter(i):
    j = i[['fullURL']].copy()
    j['fullURL'] = j['fullURL'].str.replace('\?.*','')
    j['type'] = u'主网址不包含关键字'
    j['type'][j['fullURL'].str.contains('lawtime')] = u'主网址包含关键字'
    return j
counts4 = [deletequesafter(i) for i in sql]
counts4 = pd.concat(counts4)
print(len(counts4))
counts4['type'].value_counts()

'''
删除规则5：重复数据去除
'''
#python 访问数据库
engine = create_engine('mysql+pymysql://root:1234567890@127.0.0.1:3306/test?charset=utf8')
sql = pd.read_sql('all_gzdata',engine,chunksize = 10000)

def countduplicate(i):
    j = i[['fullURL','timestamp_format','realIP']].copy()
    return j
counts5 = [countduplicate(i) for i in sql]
counts5 = pd.concat(counts5)
print(len(counts5[counts5.duplicated() == True]))
print(len(counts5.drop_duplicates()))
counts5_a = counts5.drop_duplicates()
