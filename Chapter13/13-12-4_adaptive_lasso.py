import pandas as pd

inputfile = '../data/data4.csv'
data = pd.read_csv(inputfile)

from sklearn.linear_model import Lasso
model = Lasso(alpha=0.1)
model.fit(data.iloc[:,0:10],data['y'])
print(model.coef_)