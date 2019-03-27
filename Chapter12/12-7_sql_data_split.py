"""
网址正确分类
"""
from __future__ import division
import pandas as pd
import numpy as np
import re
from sqlalchemy import create_engine

#将表格写入数据库
def savetoSQL(DF,tablename):
    import pandas as pd
    from sqlalchemy import create_engine
    yconnect = create_engine('mysql+pymysql://root:1234567890@127.0.0.1:3306/test?charset=utf8')
    pd.io.sql.to_sql(DF, tablename, yconnect, schema = 'test', if_exists ='append')

#手动分析咨询类别和知识类别的网址
engine = create_engine('mysql+pymysql://root:1234567890@127.0.0.1:3306/test?charset=utf8')
sql = pd.read_sql('cleaned_one',engine,chunksize = 10000)

def countknowledge(i):
    j = i[['fullURL']].copy()
    j['type'] = 'else'
    j['type'][j['fullURL'].str.contains('(info)|(faguizt)')] = 'zhishi'
    j['type'][j['fullURL'].str.contains('(ask)|(askzt)')] = 'zixun'
    return j
counts2 = [countknowledge(i) for i in sql]
counts2 = pd.concat(counts2)
counts2['type'].value_counts()
#统计各个类型的占比
counts2_a = counts2['type'].value_counts()
counts2_b = pd.DataFrame(counts2_a)
counts2_b.columns = ['num']
counts2_b.index.name = 'type'
counts2_b['percent'] = (counts2_b['num']/counts2_b['num'].sum())*100
print(counts2_b)

'''
手动分析知识类别的网址，得出知识类别下的二级类别
'''
knowledge = counts2[counts2['type'] == 'zhishi']
knowledge_info = knowledge[knowledge['fullURL'].str.contains('info')]
print(len(knowledge_info))
knowledge_info['iszsk'] = 'else'
knowledge_info['iszsk'][knowledge_info['fullURL'].str.contains('info')] = 'infoelsezsk'
knowledge_info['iszsk'][knowledge_info['fullURL'].str.contains('zhishiku')] = 'zsk'
knowledge_info['iszsk'].value_counts()

'''
用正则表达式匹配出网址中二级类别
'''
pattern = re.compile('/info/(.*?)/',re.S)
knowledge_info_e = knowledge_info[knowledge_info['iszsk'] == 'infoelsezsk']
for i in range(len(knowledge_info_e)):
    knowledge_info_e.iloc[i,2] = re.findall(pattern,knowledge_info_e.iloc[i,0]).copy()[0]
print(knowledge_info_e.head())

pattern1 = re.compile('zhishiku/(.*?)/',re.S)
knowledge_info_f = knowledge_info[knowledge_info['iszsk'] == 'zsk']
for i in range(len(knowledge_info_f)):
    knowledge_info_f.iloc[i,2] = re.findall(pattern1,knowledge_info_f.iloc[i,0]).copy()[0]
print(knowledge_info_f.head())

'''
列名重命名
'''
knowledge_info_e.columns = ['fullURL','type1','type2']
print(knowledge_info_e.head())
knowledge_info_f.columns = ['fullURL','type1','type2']
print(knowledge_info_f.head())

#将两类处理过二级类别的记录合并
knowledge_info_g = pd.concat(knowledge_info_e,knowledge_info_f)
knowledge_info_h = knowledge_info_g['type2'].value_counts()
print(len(knowledge_info_e['type2'].value_counts()))
print(len(knowledge_info_f['type2'].value_counts()))
print(len(knowledge_info_h['type2'].value_counts()))
print(knowledge_info_h.head())
print(knowledge_info_h.index)

'''
将二级类别分别存储到数据库中
'''
detailtypes = knowledge_info_h.index
for i in range(len(detailtypes)):
    x = knowledge_info_g[knowledge_info_g['type2'] == knowledge_info_h.index[i]]
    savetoSQL(x,knowledge_info_h.index)

'''
用正则表达式匹配出网址中三级类别
'''
knowledge_info_q = knowledge_info_e.copy()
knowledge_info_q['type3'] = np.nan
resulttype3 = pd.DataFrame([],columns = knowledge_info_q.columns)
for i in range(len(knowledge_info_h.index)):
    pattern2 = re.compile('/info/'+knowledge_info_h.index[i]+'/(.*?)/',re.S)
    current = knowledge_info_q[knowledge_info_q['type2'] == knowledge_info_h.index[i]]
    print(current.head())
    for j in range(len(current)):
        findresult = re.findall(pattern2,current.iloc[j,0])
        if findresult == []:
            current.iloc[j,3] = np.nan
        else:
            current.iloc[j,3] = findresult[0]
    resulttype3 = pd.concat(resulttype3,current)                    #将处理后的数据拼接
resulttype3.head()
resulttype3.set_index('fullURL',inplace = True)
print(resulttype3.head(10))

#统计婚姻类下面的三级类别的数目
j = resulttype3[resulttype3['type2'] == 'hunyin']['type3'].value_counts()
print(len(j))
print(j.head())

'''
目标：将类别三按照每类降序排列，然后保存
'''
Type3nums = resulttype3.pivot_table(index = ['type2','type3'],aggfunc = 'count')
#Type3nums = resulttype3.groupby([resulttype3['type2'],resulttype3['type3']].count())
r = Type3nums.reset_index().sort_values(by=['type2','type1'],ascending=[True,False])
r.set_index(['type2','type3'],inplace = True)
r.to_excel('../tmp/2_2_3Type3nums.xlsx')
print(r)

engine = create_engine('mysql+pymysql://root:1234567890@127.0.0.1:3306/test?charset=utf8')
sql = pd.read_sql('cleaned_one',engine,chunksize = 10000)
l1 = 0
l2 = 0
for i in sql:
    zixun = i[['userID','fullURL']][i['fullURL'].str.contains('(ask)|(askzt)')].copy()
    l1 = len(zixun) + l1
    hunyin = i[['userID','fullURL']][i['fullURL'].str.contains('hunyin')].copy()
    l2 = len(hunyin) + l2
    zixun.to_sql('zixunformodel',engine,index=False,if_exists='append')
    hunyin.to_sql('hunyinformodel',engine,index=False,if_exists='append')
print(l1,l2)