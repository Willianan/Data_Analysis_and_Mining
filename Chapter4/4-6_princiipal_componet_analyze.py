#主成分分析降为

import pandas as pd
from sklearn.decomposition import PCA

data = pd.read_excel('data/principal_component.xls',header=None)

pca = PCA()
pca.fit(data)
print(pca.components_)#返回模型的各种特征向量
print(pca.explained_variance_ratio_)#返回各种成分各自的方差百分比

