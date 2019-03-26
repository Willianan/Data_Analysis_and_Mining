#属性变换

import pandas as pd

#参数初始化
discfile = '../data/discdata.xls'
transformaddata = '../tmp/discdata_processed.xls'

data = pd.read_excel(discfile)
data = data[data['TARGET_ID'] == 184].copy()        #保留TARGET_ID为184的数据

data_group = data.groupby('COLLECTTIME')            #以时间分组

def attr_trans(x):                                  #定义属性变换函数
    result = pd.Series(index = ['SYS_NAME','CWXT_DB:184:C:\\', 'CWXT_DB:184:D:\\', 'COLLECTTIME'])
    result['SYS_NAME'] = x['SYS_NAME'].iloc[0]
    result['COLLECTTIME'] = x['COLLECTTIME'].iloc[0]
    result['CWXT_DB:184:C:\\'] = x['VALUE'].iloc[0]
    result['CWXT_DB:184:D:\\'] = x['VALUE'].iloc[1]
    return result
data_processed = data_group.apply(attr_trans)       #逐组处理
data_processed.to_excel(transformaddata,index = False)