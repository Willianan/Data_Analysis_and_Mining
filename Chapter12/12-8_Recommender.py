"""
协同过滤算法
"""

import numpy as np
import pandas as pd
import time

engine = create_engine('mysql+pymysql://root:1234567890@127.0.0.1:3306/test?charset=utf8')
data = pd.read_sql('hunyinformodel',engine,chunksize = 10000)
data.head()

'''
基于物品的协同过滤推荐
'''
#1、定义协同推荐函数

def jaccard(a,b):                                       #自定义杰卡德相似系数函数，仅对0-1矩阵有效
    return 1.0*(a*b).sum()/(a+b-a*b).sum()

class Recommender():
    sim = None                                          #相似度矩阵
    def similarity(self,x,distance):                    #计算相似度矩阵的函数
        y = np.ones((len(x),len(x)))
        for i in range(len(x)):
            for j in range(len(x)):
                y[i,j] = distance(x[i],x[j])
        return y

    def fit(self,x,distance = jaccard) :                #训练函数
        self.sim = self.similarity(x,distance)

    def recommend(self,a) :                             #推荐函数
        return np.dot(self.sim,a)*(1-a)

len(data['fullURL'].value_counts())
len(data['realIP'].value_counts())

#2、将所有数据转换成0-1矩阵
start0 = time.clock()
data.sort_values(by=['realIP','fullURL'],ascending=[True,True],inplace=True)
realIP = data['realIP'].value_counts().index
realIP = np.sort(realIP)
fullURL = data['fullURL'].value_counts().index
fullURL = np.sort(fullURL)
D = pd.DataFrame([],index=realIP,columns=fullURL)

for i in range(len(data)):
    a = data.iloc[i,0]
    b = data.iloc[i,1]
    D.iloc[a,b] = 1
D.fillna(0,inplace=True)
end0 = time.clock()
usetime0 = end0 - start0
print(u'转成0、1矩阵所花费的时间为'+ str(usetime0) + 's!')

#3、交叉验证方法验证推荐
df = D.copy()

simpler = np.random.permutation(len(df))
df = df.take(simpler)                                       #打乱数据

train = df.iloc[:int(len(df)*0.8),:]
test = df.iloc[int(len(df)*0.8):,:]

df = df.values

df_train = df[:int(len(df)*0.8),:]
df_test = df[int(len(df)*0.8):,:]
#由于基于物品的推荐，对于矩阵，根据上面的推荐函数，index为网址，因此需要进行转置
df_train = df_train.T
df_test = df_test.T

print(df_train.shape)
print(df_test.shape)

#4、建立相似矩阵，训练模型
start1 = time.clock()
r = Recommender()
sim = r.fit(df_train)                               #计算物品的相似度矩阵
end1 = time.clock()

a = pd.DataFrame(sim)                               #保存相似度矩阵
usetime1 = end1 - start1
print(u'建立相似矩阵耗时'+str(usetime1)+'s!')
print(a.shape)

#将所有数据保存
a.index = train.columns
a.columns = train.columns
a.to_csv('../tmp/3_1_2similarityMatrix.csv')
print(a.head(20))

#使用测试集进行预测
print(df_test.shape)
start2 = time.clock()
result = r.recommend(df_test)
end2 = time.clock()

result1 = pd.DataFrame(result)
usetime2 = end2 - start2
print(u'推荐函数耗时'+str(usetime2)+'s!')
#将推荐结果表格中的对应的网址和用户名对上
result1.index = test.columns
result1.columns = test.index
result1.to_csv('../tmp/3_1_3recommendresult.csv')

#5、协同推荐结果展现
#定义展现具体协同推荐结果的函数，k为推荐的个数，recomMatrix为协同过滤算法算出的推荐矩阵的表格化

def xietong_result(K,recomMatrix):
    recomMatrix.fillna(0.0,inplace = True)
    n = range(1,K+1)
    recommends = ['xietong'+str(y) for y in n]
    currentemp = pd.DataFrame([],index=recomMatrix.columns,columns=recommends)
    for i in range(len(recomMatrix.columns)):
        temp = recomMatrix.sort_values(by=recomMatrix.columns[i],ascending=False)
        K = 0
        while K < K:
            currentemp.iloc[i,K] = temp.index[K]
            if temp.iloc[K,i] == 0.0:
                currentemp.iloc[i,K:K] = np.nan
                break
            K += 1
    return currentemp
start3 = time.clock()
xietong_result = xietong_result(3,result1)
end3 = time.clock()
print(u'按照协同过滤推荐方法为用户推荐3个未浏览的网址耗时为'+str(end3 - start3)+'s!')
xietong_result.to_csv('../tmp/3_1_4xietong_result.csv')

'''
随机推荐
'''
randata = 1 - df_test
randmatrix = pd.DataFrame(randata,index=test.columns,columns=test.index)
#定义随机推荐函数
def rand_recommend(K,recomMatrix):
    import random
    recomMatrix.fillna(0.0,inplace = True)
    recommends = ['recommend'+str(y) for y in range(1,K+1)]
    currentemp = pd.DataFrame([],index=recomMatrix.columns,columns=recommends)
    for i in range(len(recomMatrix.columns)):
        curentcol = recomMatrix.columns[i]
        temp = recomMatrix[curentcol][recomMatrix[curentcol] != 0]
        if len(temp) == 0:
            currentemp.iloc[i,:] = np.nan
        elif len(temp) < K:
            r = temp.index.take(np.random.permutation(len(temp)))
            currentemp.iloc[i,len(r)] = r
        else:
            r = random.sample(temp.index,K)
            currentemp.iloc[i,:] = r
    return currentemp
start4 = time.clock()
random_result = rand_recommend(3,randmatrix)
end4 = time.clock()
print(u'随机为用户推荐3个未浏览过的网址耗时为'+str(end4 - start4)+'s!')
random_result.to_csv('../tmp/random_result.csv')

'''
按照流行度推荐
'''
#1、定义按照流行度推荐函数
def popular_recommend(K,recomMatrix):
    recomMatrix.fillna(0.0,inplace=True)
    recommends = ['recommend'+str(y) for y in range(1,K+1)]
    currentemp = pd.DataFrame([],index=recomMatrix.columns,columns=recommends)
    for i in range(len(recomMatrix.columns)):
        curentcol = recomMatrix.columns[i]
        temp = recomMatrix[curentcol][recomMatrix[curentcol] != 0]
        if len(temp) == 0:
            currentemp.iloc[i,:] = np.nan
        elif len(temp) < K:
            r = temp.index
            currentemp.iloc[i,len(r)] = r
        else:
            r = temp.index[:K]
            currentemp.iloc[i,:] = r
    return currentemp
#确定用户未浏览的网页
TEST = 1 - df_test
test2 = pd.DataFrame(TEST,index=test.columns,columns=test.index)
print(test2.head())
print(test2.shape)

#确定网页浏览热度排名
hotPopular = data['fullURL'].value_counts()
hotPopular = pd.DataFrame(hotPopular)
print(hotPopular.head())
print(hotPopular.shape)

#按照流行度对可推荐的所有网址排序
test3 = test2.reset_index()
list_custom = list(hotPopular.index)
test3['index'] = test3['index'].astype('category')
test3['index'].cat.reorder_categories(list_custom,inplace=True)
test3.sort_values(by='index',inplace=True)
test3.set_index('index',inplace=True)
print(test3.head())
print(test3.shape)

#按照流行度为用户推荐3个未浏览过的网址
recomMatrix = test3
start5 = time.clock()
popular_result = popular_recommend(3,recomMatrix)
end5 = time.clock()
print(u'按照流行度为用户推荐3个未浏览过的网址耗时为'+str(end5 - start5)+'s!')
popular_result.to_csv('../tmp/popular_result.csv')