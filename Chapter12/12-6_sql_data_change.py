"""
数据变换
"""

from __future__ import division
import pandas as pd
from sqlalchemy import create_engine

#将表格写入数据库
def savetoSQL(DF,tablename):
    import pandas as pd
    from sqlalchemy import create_engine
    yconnect = create_engine('mysql+pymysql://root:1234567890@127.0.0.1:3306/test?charset=utf8')
    pd.io.sql.to_sql(DF, tablename, yconnect, schema = 'test', if_exists ='append')

'''
识别翻页的网址并删除重复的记录
'''
#python 访问数据库
engine = create_engine('mysql+pymysql://root:1234567890@127.0.0.1:3306/test?charset=utf8')
sql = pd.read_sql('cleaned_one',engine,chunksize = 10000)

L0 = 0
L1 = 0
L2 = 0
for i in sql:
    d = i.copy()
    temp0 = len(d)
    L0 = temp0 + L0

    #获取类似于http://www.lawtime.cn***/2007020619634_2.html格式的记录的个数
    x1 = d[d['fullURL'].str.contains('_\d{0,2}.html')]
    temp1 = len(x1)
    L1 = L1 + temp1

    #获取类似于http://www.lawtime.cn***/29_1_p3.html格式的记录的个数
    x2 = d[d['fullURL'].str.contains('_\d{0,2}_\w{0,2}.html')]
    temp2 = len(x2)
    L2 = temp2 + L2

    x1.to_sql('l1', engine, index = False, if_exists = 'append')
    x2.to_sql('l2', engine, index = False, if_exists = 'append')
print(L0,L1,L2)

'''
#注意：在内部循环中，容易删除不完整，所有需要进行全部二次筛选删除
#初步筛选
'''
engine = create_engine('mysql+pymysql://root:1234567890@127.0.0.1:3306/test?charset=utf8')
sql = pd.read_sql('cleaned_one',engine,chunksize = 10000)
l4 = 0
for i in sql:
    d = i.copy()
    d['fullURL'] = d[d['fullURL'].str.replace('_\d{0,2}.html','.html')]
    d['fullURL'] = d[d['fullURL'].str.replace('_\d{0,2}_\w{0,2}.html')]

    d = d.drop_duplicates()
    temp = len(d)
    l4 = l4 + temp
    d.to_sql('changed_1', engine, index = False, if_exists = 'append')
print(l4)
#二次筛选
engine = create_engine('mysql+pymysql://root:1234567890@127.0.0.1:3306/test?charset=utf8')
sql = pd.read_sql('changed_1',engine,chunksize = 10000)

def dropduplicate(i):
    j = i[['realIP','fullURL','pageTitle','userID','timestamp_format']].copy()
    return j
counts1 = [dropduplicate(i) for i in sql]
counts1 = pd.concat(counts1)
print(len(counts1))
a = counts1.droplicates(['fullURL','userID'])
print(len(a))
savetoSQL(a,'changed_2')

"""
查看经过数据变换替换后的数据是否替换干净
"""
engine = create_engine('mysql+pymysql://root:1234567890@127.0.0.1:3306/test?charset=utf8')
sql = pd.read_sql('changed_2',engine,chunksize = 10000)
l0 = 0
l1 = 0
l2 = 0
for i in sql:
    d = i.copy()
    temp0 = len(d)
    l0 = temp0 + l0

    x1 = d[d['fullURL'].str.contains('_\d{0,2}.html')]
    temp1 = len(x1)
    l1 = l1 + temp1

    x2 = d[d['fullURL'].str.contains('_\d{0,2}_\w{0,2}.html')]
    temp2 = len(x2)
    l2 = temp2 + l2
print(l0,l1,l2)
