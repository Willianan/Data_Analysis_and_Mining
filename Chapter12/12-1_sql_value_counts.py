

from __future__ import division
import pandas as pd
from sqlalchemy import create_engine

#将表格写入数据库
def savetoSQL(DF,tablename):
    import pandas as pd
    from sqlalchemy import create_engine
    yconnect = create_engine('mysql+pymysql://root:1234567890@127.0.0.1:3306/test?charset=utf8')
    pd.io.sql.to_sql(DF, tablename, yconnect, schema = 'test', if_exists ='append')

#python 访问数据库
engine = create_engine('mysql+pymysql://root:1234567890@127.0.0.1:3306/test?charset=utf8')
sql = pd.read_sql('all_gzdata',engine,chunksize = 10000)

#分块统计
counts = [i['fullURLId'].value_counts() for i in sql]               #逐块统计
counts = pd.concat(counts).groupby(level = 0).sum()                 #合并统计结果，把相同的统计项合并（即按index分组并求和）
counts = counts.reset_index()                                       #重新设置index，将原来的index作为counts的一列

counts.columns = ['index','num']                                    #重新设置列名，主要是第二列，默认为0
counts['type'] = counts['index'].str.extract('(\d{3})')             #提取前三个数字作为类别id
print(counts)
counts_ = counts[['type','num']].groupby('type').sum()              #按类别合并
counts_.sort_values(by = 'num',ascending = False, inplace = True)   #降序排列
counts_['percentage'] = (counts_['num']/counts_['num'].sum())*100
#保存的表命名方式为“1_1_k此功能表名称”，type_counts：计算各个大类占的比例
counts_.to_excel('../tmp/1_1_1type_counts.xlsx')

#每个大类别下面小类别占比
a = counts.set_index(['type'])
b = counts.groupby('type').sum()
c = pd.merge(a,b,left_index = True, right_index = True)
c['persentage'] = (c['num_x']/c['num_y'])*100
del c['num_y']
c.rename(columns = {'num_x':'num'},inplace = True)
print(c)
c.reset_index(inplace = True)
d = c.sort_values(by = ['type','persentage'], ascending = [True,False]).reset_index()
print(d)
del d['level_0']
per_counts = d.set_index(['type','index'])
#type_counts_per:计算每个大类下各个小分支所占比例
per_counts.to_excel('../tmp/1_1_2type_counts_per.xlsx')


#统计107类别的情况
def count107(i):
    j = i[['fullURL']][i['fullURLId'].str.contains('107')].copy()       #找出类别包含107的网址
    j['type'] = None                                                    #添加空列
    j['type'][j['fullURL'].str.contains('info/.+?/')] = u'知识首页'
    j['type'][j['fullURL'].str.contains('info/.+?/.+?')] = u'知识列表页'
    j['type'][j['fullURL'].str.contains('/\d+?_*\d+?\.html')] = u'知识内容页'
    return j['type'].value_counts()

#python 访问数据库
engine = create_engine('mysql+pymysql://root:1234567890@127.0.0.1:3306/test?charset=utf8')
sql = pd.read_sql('all_gzdata',engine,chunksize = 10000)

counts2 = [count107(i) for i in sql]                                    #逐块统计
counts2 = pd.concat(counts2).groupby(level = 0).sum()                   #合并并统计结果

#计算各个部分的占比
res107 = pd.DataFrame(counts2)
res107.index.name = u'107类型'
res107.rename(columns = {'type':'num'},inplace = True)
res107[u'百分比'] = (res107['num']/res107['num'].sum())*100
res107.reset_index(inplace = True)
res107.to_excel('../tmp/1_1_3type107.xlsx')

#统计带问号网址类型统计
def countquestion(i):
    j = i[['fullURLId']][i['fullURL'].str.contains('\?')].copy()
    return j
#python 访问数据库
engine = create_engine('mysql+pymysql://root:1234567890@127.0.0.1:3306/test?charset=utf8')
sql = pd.read_sql('all_gzdata',engine,chunksize = 10000)

counts3 = [countquestion(i)['fullURLId'].value_counts() for i in sql]
counts3 = pd.concat(counts3).groupby(level = 0).sum()
print(counts3)
#求各个类型的占比并保存数据
df1 = pd.DataFrame(counts3)
df1['perc'] = (df1['fullURLId']/df1['fullURLId'].sum())*100
df1.sort_values(by = 'fullURLId', ascending = False, inplace = True)
df1.round(4).to_excel('../tmp/1_1_4questiontype.xlsx')

#求带问号的结果占所有数据的比例

allcount = counts['num'].sum()                                 #所有记录总数
questionresult = (df1['fullURLId'].sum()/allcount)*100
print(questionresult)


#统计199类型中的具体类型占比
def page199(i):
    j = i[['fullURL','pageTitle']][(i['fullURLId'].str.contains('199')) & (i['fullURL'].str.contains('\?'))]
    j['pageTitle'].fillna(u'空',inplace = True)
    j['type'] = u'其他'
    j['type'][j['pageTitle'].str.contains(u'法律快车-法律助手')] = u'法律快车-法律助手'
    j['type'][j['pageTitle'].str.contains(u'咨询发布成功')] = u'咨询发布成功'
    j['type'][j['pageTitle'].str.contains(u'免费发布法律咨询')] = u'免费发布法律咨询'
    j['type'][j['pageTitle'].str.contains(u'法律快搜')] = u'快搜'
    j['type'][j['pageTitle'].str.contains(u'法律快车法律经验')] = u'法律快车法律经验'
    j['type'][j['pageTitle'].str.contains(u'法律快车法律咨询')] = u'法律快车法律咨询'
    j['type'][j['pageTitle'].str.contains(u'_法律快车') | j['pageTitle'].str.contains(u'-法律快车')] = u'法律快车'
    j['type'][j['pageTitle'].str.contains(u'空')] = u'空'
    return j
#注意：获取一次sql对象，就需要重新访问一下数据库
#python 访问数据库
engine = create_engine('mysql+pymysql://root:1234567890@127.0.0.1:3306/test?charset=utf8')
sql = pd.read_sql('all_gzdata',engine,chunksize = 10000)

counts4 = [page199(i) for i in sql]
counts4 = pd.concat(counts4)
counts4typecounts = counts4['type'].value_counts()
print(counts4typecounts)
counts4other = counts4[counts4['type'] == u'其他']
savetoSQL(counts4other,'199elsePercentage')                                 #将199的网页中的“其他”类型的数据存入数据库中

#求各个部分的占比并保存数据
counts4typecounts_ = pd.DataFrame(counts4typecounts)
counts4typecounts_['perc'] = (counts4typecounts_['type']/counts4typecounts_['type'].sum())*100
counts4typecounts_.to_excel('../tmp/1_1_5page199.xlsx')
print(counts4typecounts_)

#统计瞎逛用户中各个类型占比
def xiaguang(i):
    j = i[['fullURL','fullURLId','pageTitle']][(i['fullURL'].str.contains('\.html')) == False]
    return j
#python 访问数据库
engine = create_engine('mysql+pymysql://root:1234567890@127.0.0.1:3306/test?charset=utf8')
sql = pd.read_sql('all_gzdata',engine,chunksize = 10000)

counts5 = [xiaguang(i) for i in sql]
counts5 = pd.concat(counts5)
savetoSQL(counts5,'xiaguang')
xg1 = counts5['fullURLId'].value_counts()
print(xg1)
#求各个部分的占比
xg_ = pd.DataFrame(xg1)
xg_.reset_index(inplace = True)
xg_.columns = ['index','num']
xg_.sort_values(by = 'num', ascending = False, inplace = True)
xg_['type'] = xg_['index'].str.extract('(d\{3})')                       #提前前三个数字作为类别id
xgs_ = xg_[['type','num']].groupby('type').sum()                        #按类别合并
xgs_.sort_values(by = 'num', ascending = False,inplace = True)          #降序排列
xgs_['percentage'] = (xgs_['num']/xgs_['num'].sum())*100
xgs_.round(4).to_excel('../tmp/1_1_6xiaguang.xlsx')
print(xgs_.round(4))