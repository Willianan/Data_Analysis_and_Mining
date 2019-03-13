#使用神经网络算法预测销量高低

import pandas as pd

#参数初始化
data = pd.read_excel('data/sales_data.xls',index_col=u'序号')

#数据转换
data[data == u'好'] = 1
data[data == u'是'] = 1
data[data == u'高'] = 1
data[data != 1] = 1
x = data.iloc[:,:3].values.astype(int)
y = data.iloc[:,3].values.astype(int)

from keras.models import Sequential
from keras.layers.core import Dense,Activation

model = Sequential()    #建立模型
model.add(Dense(input_dim = 3,units = 10))
model.add(Activation('relu'))   #用relu函数作为激活函数，能够大幅度提供准确度
model.add(Dense(input_dim = 10,units = 1))
model.add(Activation('sigmoid'))    #由于是0~1输出，用sigmoid函数作为激活函数

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])      #编译模型

model.fit(x,y,epochs = 1000,batch_size=10)  #训练模型，学习一千次
yp = model.predict_classes(x).reshape(len(y))       #分类预测


def cm_plot(y, yp):
    from sklearn.metrics import confusion_matrix
    cm = confusion_matrix(y, yp)
    import matplotlib.pyplot as plt
    plt.matshow(cm, cmap=plt.cm.Greens)
    plt.colorbar()
    
    for x in range(len(cm)):
        for y in range(len(cm)):
            plt.annotate(cm[x, y], xy=(x, y), horizontalalignment='center', verticalalignment='center')
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    return plt
cm_plot(y,yp).show()    #显示混淆矩阵可视化结果