#Apriori关联规则算法

from __future__ import print_function
import pandas as pd
from apriori import *                   #导入自行编写的高效Apriori函数
import time                             #导入时间库用来计算用时

inputfile = '../data/apriori.txt'
data = pd.read_csv(inputfile,header = None, dtype = object)

start = time.clock()                    #开始计时
print(u'\n转换原始数据到0-1矩阵~~~~~~')
ct = lambda x : pd.Series(1,index = x[pd.notnull(x)])       #转换0-1矩阵的过渡函数，即将标签数据转换为1
b = map(ct,data.values)                 #用map方式执行
b = list(b)
data = pd.DataFrame(b).fillna(0)        #实现矩阵转换，除了1外，其余为空，空值用0填充
end = time.clock()                      #计时结束
print(u'\n转换完毕，用时：%0.2f秒' %(end - start))
del b                                   #删除中间变量b，节省内存

support = 0.06                          #最小支持度
confidence = 0.75                       #最小置信度
ms = '----'                             #连接符，默认为----，用来区分不同元素

start = time.clock()
print(u'\n开始搜索关联规则.......')
find_rule(data,support,confidence,ms)
end = time.clock()
print(u'\n搜索完成，用时：%0.2f秒' %(end - start))