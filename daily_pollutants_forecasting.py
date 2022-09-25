# -*- coding: utf-8 -*-
"""Pollutants Forecasting.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qsiqz6e3T_3Ja4xval-U4ps8lKDhxNMZ
"""

from google.colab import drive
drive.mount('/content/gdrive')

"""#PM2.5"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
# %matplotlib inline
from matplotlib.pylab import rcParams
import seaborn as sns
rcParams['figure.figsize']=10,8

df = pd.read_csv('/content/gdrive/MyDrive/Covid Pollutants Analysis/Alipur.csv', parse_dates=[0])     #daily data for PM2.5, PM10, NO2
df2 = pd.read_csv('/content/gdrive/MyDrive/Covid Pollutants Analysis/Alipur_2.csv', parse_dates=[0])  #8 hrs data for CO, Ozone

"""###combining datasets"""

df2.head()

df2.tail()

#converting 8 hrs data to daily data

df['CO'] = np.NaN
df['Ozone'] = np.NaN

i=0
j=0
while (i < len(df2)):
  df['CO'][j] = (df2['CO'][i] + df2['CO'][i+1] + df2['CO'][i+2])/3
  df['Ozone'][j] = (df2['Ozone'][i] + df2['Ozone'][i+1] + df2['Ozone'][i+2])/3
  i+=3
  j+=1

"""###describe dataset"""

df.head()

df.tail()

df.shape

df.info()

df.describe()

# univariate plots
df.drop(['Date'], axis=1).hist(figsize=(25,4), layout=(1,5))
plt.show()

"""###ML models"""

import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.ensemble import AdaBoostRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor

df.columns

col_ = df.columns.tolist()[2:]
#col_.remove('PM25')

col_

#defining feature (X) and target (y)
X = df[col_]    #X-input features
y = df.iloc[:,1]  #y-input features

#Normalize Feature variable
ss = StandardScaler()
X_std = ss.fit_transform(X)     #apply stardardisation

#Train test split with test size 20% and train size as 80%
X_train, X_test, y_train, y_test = train_test_split(X_std, y, test_size=0.2, random_state=1)

print('Training data size:',X_train.shape)
print('Test data size:',X_test.shape)
print('Training data size:',y_train.shape)
print('Test data size:',y_test.shape)

names = []
r2_val = []
rmse_val = []
mae_val = []

#Linear Regression

lr = LinearRegression()
lr_model = lr.fit(X_train,y_train)          #fit the linear model on train data

#Prediction
y_pred = lr_model.predict(X_test)                   #predict using the model

r2 = r2_score(y_test,y_pred)                        #calculate r2
print('R^2 of model:',r2)
rmse = np.sqrt(mean_squared_error(y_test,y_pred))   #calculate rmse
print('RMSE of model:',rmse)
mae = mean_absolute_error(y_test,y_pred)            #calculate mae
print('MAE of model:',mae)

name = 'Linear Regression'
r2_val.append(r2)
rmse_val.append(rmse)
mae_val.append(mae)
names.append(name)

#Ada Boost Regressor

abr = AdaBoostRegressor()
abr_model = abr.fit(X_train,y_train)

y_pred = abr_model.predict(X_test)
r2 = r2_score(y_test,y_pred)
print('R^2 of model:',r2)
rmse = np.sqrt(mean_squared_error(y_test,y_pred))
print('RMSE of model:',rmse)
mae = mean_absolute_error(y_test,y_pred)
print('MAE of model:',mae)

name = 'AdaBoost'
r2_val.append(r2)
rmse_val.append(rmse)
mae_val.append(mae)
names.append(name)

#Decision Tree Regression

dt_one_reg = DecisionTreeRegressor()

dt_model = dt_one_reg.fit(X_train,y_train)
y_pred_dtone = dt_model.predict(X_test)
r2 = r2_score(y_pred_dtone,y_test)
print('R^2 of model:',r2)
rmse = np.sqrt(mean_squared_error(y_pred_dtone,y_test))
print('RMSE of model:',rmse)
mae = mean_absolute_error(y_pred_dtone,y_test)
print('MAE of model:',mae)

name = 'Decision Tree'
r2_val.append(r2)
rmse_val.append(rmse)
mae_val.append(mae)
names.append(name)

#Random Forest Regression

rf_reg=RandomForestRegressor()

#Fit the RF model and predict
rf_model = rf_reg.fit(X_train,y_train)
y_pred_rf = rf_model.predict(X_test)

r2 = r2_score(y_test,y_pred_rf)
print('R^2 of model:',r2)
rmse = np.sqrt(mean_squared_error(y_test,y_pred_rf))
print('RMSE of model:',rmse)
mae = mean_absolute_error(y_test,y_pred_rf)
print('MAE of model:',mae)

name = 'Random Forest'
r2_val.append(r2)
rmse_val.append(rmse)
mae_val.append(mae)
names.append(name)

#Support Vector Machine

sv_reg = SVR()
sv_model = sv_reg.fit(X_train,y_train)

y_pred_sv=sv_model.predict(X_test)

r2 = r2_score(y_test,y_pred_sv)
print('R^2 of model:',r2)
rmse = np.sqrt(mean_squared_error(y_test,y_pred_sv))
print('RMSE of model:',rmse)
mae = mean_absolute_error(y_test,y_pred_sv)
print('MAE of model:',mae)

name = 'Support Vector Machine'
r2_val.append(r2)
rmse_val.append(rmse)
mae_val.append(mae)
names.append(name)

#KNN REGRESSOR

knn = KNeighborsRegressor(n_neighbors=1)
knn.fit(X_train, y_train)
pred = knn.predict(X_test)

r2 = r2_score(y_test, pred)
print('R^2 of model:',r2)
rmse = np.sqrt(mean_squared_error(y_test, pred))
print('RMSE of model:',rmse)
mae = mean_absolute_error(y_test,pred)
print('MAE of model:',mae)

knn = KNeighborsRegressor(n_neighbors=7)
knn.fit(X_train, y_train)
pred = knn.predict(X_test)

r2 = r2_score(y_test, pred)
print('R^2 of model:',r2)
rmse = np.sqrt(mean_squared_error(y_test, pred))
print('RMSE of model:',rmse)
mae = mean_absolute_error(y_test,pred)
print('MAE of model:',mae)

name = 'KNN'
r2_val.append(r2)
rmse_val.append(rmse)
mae_val.append(mae)
names.append(name)

for i in range(6):
    print('%s: %f' % (names[i], r2_val[i]))

for i in range(6):
    print('%s: %f' % (names[i], rmse_val[i]))

for i in range(6):
    print('%s: %f' % (names[i], mae_val[i]))

r2_val = list(np.around(np.array(r2_val),3))
rmse_val = list(np.around(np.array(rmse_val),3))
mae_val = list(np.around(np.array(mae_val),3))

from prettytable import PrettyTable
t = PrettyTable(['Regression Model','R^2', 'RMSE', 'MAE'])
t.title = 'PM2.5'
for i in range(6):
  t.add_row([names[i], r2_val[i], rmse_val[i], mae_val[i]])
print(t)

plt.figure(figsize=(22,4))
plt.suptitle('PM2.5')

plt.subplot(1,2,1)
plt.plot(names, rmse_val, marker='o', label='rmse')
plt.plot(names, mae_val, marker='o', color='r', label='mae')
plt.legend()

plt.subplot(1,2,2)
plt.plot(names, r2_val, marker='o', color='g', label='r2')
plt.legend()
plt.show()

"""#PM10"""

df.columns

col_ = ['PM25', 'NO2', 'CO', 'Ozone']

#defining feature (X) and target (y)
X = df[col_]    #X-input features
y = df.iloc[:,2]  #y-input features

#Normalize Feature variable
ss = StandardScaler()
X_std = ss.fit_transform(X)     #apply stardardisation

#Train test split with test size 20% and train size as 80%
X_train, X_test, y_train, y_test = train_test_split(X_std, y, test_size=0.2, random_state=1)

print('Training data size:',X_train.shape)
print('Test data size:',X_test.shape)
print('Training data size:',y_train.shape)
print('Test data size:',y_test.shape)

names = []
r2_val = []
rmse_val = []
mae_val = []

#Linear Regression

lr = LinearRegression()
lr_model = lr.fit(X_train,y_train)          #fit the linear model on train data

#Prediction
y_pred = lr_model.predict(X_test)                   #predict using the model

r2 = r2_score(y_test,y_pred)                        #calculate r2
print('R^2 of model:',r2)
rmse = np.sqrt(mean_squared_error(y_test,y_pred))   #calculate rmse
print('RMSE of model:',rmse)
mae = mean_absolute_error(y_test,y_pred)            #calculate mae
print('MAE of model:',mae)

name = 'Linear Regression'
r2_val.append(r2)
rmse_val.append(rmse)
mae_val.append(mae)
names.append(name)

#Ada Boost Regressor

abr = AdaBoostRegressor()
abr_model = abr.fit(X_train,y_train)

y_pred = abr_model.predict(X_test)
r2 = r2_score(y_test,y_pred)
print('R^2 of model:',r2)
rmse = np.sqrt(mean_squared_error(y_test,y_pred))
print('RMSE of model:',rmse)
mae = mean_absolute_error(y_test,y_pred)
print('MAE of model:',mae)

name = 'AdaBoost'
r2_val.append(r2)
rmse_val.append(rmse)
mae_val.append(mae)
names.append(name)

#Decision Tree Regression

dt_one_reg = DecisionTreeRegressor()

dt_model = dt_one_reg.fit(X_train,y_train)
y_pred_dtone = dt_model.predict(X_test)
r2 = r2_score(y_pred_dtone,y_test)
print('R^2 of model:',r2)
rmse = np.sqrt(mean_squared_error(y_pred_dtone,y_test))
print('RMSE of model:',rmse)
mae = mean_absolute_error(y_pred_dtone,y_test)
print('MAE of model:',mae)

name = 'Decision Tree'
r2_val.append(r2)
rmse_val.append(rmse)
mae_val.append(mae)
names.append(name)

#Random Forest Regression

rf_reg=RandomForestRegressor()

#Fit the RF model and predict
rf_model = rf_reg.fit(X_train,y_train)
y_pred_rf = rf_model.predict(X_test)

r2 = r2_score(y_test,y_pred_rf)
print('R^2 of model:',r2)
rmse = np.sqrt(mean_squared_error(y_test,y_pred_rf))
print('RMSE of model:',rmse)
mae = mean_absolute_error(y_test,y_pred_rf)
print('MAE of model:',mae)

name = 'Random Forest'
r2_val.append(r2)
rmse_val.append(rmse)
mae_val.append(mae)
names.append(name)

#Support Vector Machine

sv_reg = SVR()
sv_model = sv_reg.fit(X_train,y_train)

y_pred_sv=sv_model.predict(X_test)

r2 = r2_score(y_test,y_pred_sv)
print('R^2 of model:',r2)
rmse = np.sqrt(mean_squared_error(y_test,y_pred_sv))
print('RMSE of model:',rmse)
mae = mean_absolute_error(y_test,y_pred_sv)
print('MAE of model:',mae)

name = 'Support Vector Machine'
r2_val.append(r2)
rmse_val.append(rmse)
mae_val.append(mae)
names.append(name)

#KNN REGRESSOR

knn = KNeighborsRegressor(n_neighbors=1)
knn.fit(X_train, y_train)
pred = knn.predict(X_test)

r2 = r2_score(y_test, pred)
print('R^2 of model:',r2)
rmse = np.sqrt(mean_squared_error(y_test, pred))
print('RMSE of model:',rmse)
mae = mean_absolute_error(y_test,pred)
print('MAE of model:',mae)

knn = KNeighborsRegressor(n_neighbors=7)
knn.fit(X_train, y_train)
pred = knn.predict(X_test)

r2 = r2_score(y_test, pred)
print('R^2 of model:',r2)
rmse = np.sqrt(mean_squared_error(y_test, pred))
print('RMSE of model:',rmse)
mae = mean_absolute_error(y_test,pred)
print('MAE of model:',mae)

name = 'KNN'
r2_val.append(r2)
rmse_val.append(rmse)
mae_val.append(mae)
names.append(name)

for i in range(6):
    print('%s: %f' % (names[i], r2_val[i]))

for i in range(6):
    print('%s: %f' % (names[i], rmse_val[i]))

for i in range(6):
    print('%s: %f' % (names[i], mae_val[i]))

r2_val = list(np.around(np.array(r2_val),3))
rmse_val = list(np.around(np.array(rmse_val),3))
mae_val = list(np.around(np.array(mae_val),3))

from prettytable import PrettyTable
t = PrettyTable(['Regression Model','R^2', 'RMSE', 'MAE'])
t.title = 'PM10'
for i in range(6):
  t.add_row([names[i], r2_val[i], rmse_val[i], mae_val[i]])
print(t)

plt.figure(figsize=(22,4))
plt.suptitle('PM10')

plt.subplot(1,2,1)
plt.plot(names, rmse_val, marker='o', label='rmse')
plt.plot(names, mae_val, marker='o', color='r', label='mae')
plt.legend()

plt.subplot(1,2,2)
plt.plot(names, r2_val, marker='o', color='g', label='r2')
plt.legend()
plt.show()

"""#NO2"""

df.columns

col_ = ['PM25', 'PM10', 'CO', 'Ozone']

col_

#defining feature (X) and target (y)
X = df[col_]    #X-input features
y = df.iloc[:,3]  #y-input features

#Normalize Feature variable
ss = StandardScaler()
X_std = ss.fit_transform(X)     #apply stardardisation

#Train test split with test size 20% and train size as 80%
X_train, X_test, y_train, y_test = train_test_split(X_std, y, test_size=0.2, random_state=1)

print('Training data size:',X_train.shape)
print('Test data size:',X_test.shape)
print('Training data size:',y_train.shape)
print('Test data size:',y_test.shape)

names = []
r2_val = []
rmse_val = []
mae_val = []

#Linear Regression

lr = LinearRegression()
lr_model = lr.fit(X_train,y_train)          #fit the linear model on train data

#Prediction
y_pred = lr_model.predict(X_test)                   #predict using the model

r2 = r2_score(y_test,y_pred)                        #calculate r2
print('R^2 of model:',r2)
rmse = np.sqrt(mean_squared_error(y_test,y_pred))   #calculate rmse
print('RMSE of model:',rmse)
mae = mean_absolute_error(y_test,y_pred)            #calculate mae
print('MAE of model:',mae)

name = 'Linear Regression'
r2_val.append(r2)
rmse_val.append(rmse)
mae_val.append(mae)
names.append(name)

#Ada Boost Regressor

abr = AdaBoostRegressor()
abr_model = abr.fit(X_train,y_train)

y_pred = abr_model.predict(X_test)
r2 = r2_score(y_test,y_pred)
print('R^2 of model:',r2)
rmse = np.sqrt(mean_squared_error(y_test,y_pred))
print('RMSE of model:',rmse)
mae = mean_absolute_error(y_test,y_pred)
print('MAE of model:',mae)

name = 'AdaBoost'
r2_val.append(r2)
rmse_val.append(rmse)
mae_val.append(mae)
names.append(name)

#Decision Tree Regression

dt_one_reg = DecisionTreeRegressor()

dt_model = dt_one_reg.fit(X_train,y_train)
y_pred_dtone = dt_model.predict(X_test)
r2 = r2_score(y_pred_dtone,y_test)
print('R^2 of model:',r2)
rmse = np.sqrt(mean_squared_error(y_pred_dtone,y_test))
print('RMSE of model:',rmse)
mae = mean_absolute_error(y_pred_dtone,y_test)
print('MAE of model:',mae)

name = 'Decision Tree'
r2_val.append(r2)
rmse_val.append(rmse)
mae_val.append(mae)
names.append(name)

#Random Forest Regression

rf_reg=RandomForestRegressor()

#Fit the RF model and predict
rf_model = rf_reg.fit(X_train,y_train)
y_pred_rf = rf_model.predict(X_test)

r2 = r2_score(y_test,y_pred_rf)
print('R^2 of model:',r2)
rmse = np.sqrt(mean_squared_error(y_test,y_pred_rf))
print('RMSE of model:',rmse)
mae = mean_absolute_error(y_test,y_pred_rf)
print('MAE of model:',mae)

name = 'Random Forest'
r2_val.append(r2)
rmse_val.append(rmse)
mae_val.append(mae)
names.append(name)

#Support Vector Machine

sv_reg = SVR()
sv_model = sv_reg.fit(X_train,y_train)

y_pred_sv=sv_model.predict(X_test)

r2 = r2_score(y_test,y_pred_sv)
print('R^2 of model:',r2)
rmse = np.sqrt(mean_squared_error(y_test,y_pred_sv))
print('RMSE of model:',rmse)
mae = mean_absolute_error(y_test,y_pred_sv)
print('MAE of model:',mae)

name = 'Support Vector Machine'
r2_val.append(r2)
rmse_val.append(rmse)
mae_val.append(mae)
names.append(name)

#KNN REGRESSOR

knn = KNeighborsRegressor(n_neighbors=1)
knn.fit(X_train, y_train)
pred = knn.predict(X_test)

r2 = r2_score(y_test, pred)
print('R^2 of model:',r2)
rmse = np.sqrt(mean_squared_error(y_test, pred))
print('RMSE of model:',rmse)
mae = mean_absolute_error(y_test,pred)
print('MAE of model:',mae)

knn = KNeighborsRegressor(n_neighbors=7)
knn.fit(X_train, y_train)
pred = knn.predict(X_test)

r2 = r2_score(y_test, pred)
print('R^2 of model:',r2)
rmse = np.sqrt(mean_squared_error(y_test, pred))
print('RMSE of model:',rmse)
mae = mean_absolute_error(y_test,pred)
print('MAE of model:',mae)

name = 'KNN'
r2_val.append(r2)
rmse_val.append(rmse)
mae_val.append(mae)
names.append(name)

for i in range(6):
    print('%s: %f' % (names[i], r2_val[i]))

for i in range(6):
    print('%s: %f' % (names[i], rmse_val[i]))

for i in range(6):
    print('%s: %f' % (names[i], mae_val[i]))

r2_val = list(np.around(np.array(r2_val),3))
rmse_val = list(np.around(np.array(rmse_val),3))
mae_val = list(np.around(np.array(mae_val),3))

from prettytable import PrettyTable
t = PrettyTable(['Regression Model','R^2', 'RMSE', 'MAE'])
t.title = 'NO2'
for i in range(6):
  t.add_row([names[i], r2_val[i], rmse_val[i], mae_val[i]])
print(t)

plt.figure(figsize=(22,4))
plt.suptitle('NO2')

plt.subplot(1,2,1)
plt.plot(names, rmse_val, marker='o', label='rmse')
plt.plot(names, mae_val, marker='o', color='r', label='mae')
plt.legend()

plt.subplot(1,2,2)
plt.plot(names, r2_val, marker='o', color='g', label='r2')
plt.legend()
plt.show()

"""#CO"""

df.columns

col_ = ['PM25', 'PM10', 'NO2', 'Ozone']

col_

#defining feature (X) and target (y)
X = df[col_]    #X-input features
y = df.iloc[:,4]  #y-input features

#Normalize Feature variable
ss = StandardScaler()
X_std = ss.fit_transform(X)     #apply stardardisation

#Train test split with test size 20% and train size as 80%
X_train, X_test, y_train, y_test = train_test_split(X_std, y, test_size=0.2, random_state=1)

print('Training data size:',X_train.shape)
print('Test data size:',X_test.shape)
print('Training data size:',y_train.shape)
print('Test data size:',y_test.shape)

names = []
r2_val = []
rmse_val = []
mae_val = []

#Linear Regression

lr = LinearRegression()
lr_model = lr.fit(X_train,y_train)          #fit the linear model on train data

#Prediction
y_pred = lr_model.predict(X_test)                   #predict using the model

r2 = r2_score(y_test,y_pred)                        #calculate r2
print('R^2 of model:',r2)
rmse = np.sqrt(mean_squared_error(y_test,y_pred))   #calculate rmse
print('RMSE of model:',rmse)
mae = mean_absolute_error(y_test,y_pred)            #calculate mae
print('MAE of model:',mae)

name = 'Linear Regression'
r2_val.append(r2)
rmse_val.append(rmse)
mae_val.append(mae)
names.append(name)

#Ada Boost Regressor

abr = AdaBoostRegressor()
abr_model = abr.fit(X_train,y_train)

y_pred = abr_model.predict(X_test)
r2 = r2_score(y_test,y_pred)
print('R^2 of model:',r2)
rmse = np.sqrt(mean_squared_error(y_test,y_pred))
print('RMSE of model:',rmse)
mae = mean_absolute_error(y_test,y_pred)
print('MAE of model:',mae)

name = 'AdaBoost'
r2_val.append(r2)
rmse_val.append(rmse)
mae_val.append(mae)
names.append(name)

#Decision Tree Regression

dt_one_reg = DecisionTreeRegressor()

dt_model = dt_one_reg.fit(X_train,y_train)
y_pred_dtone = dt_model.predict(X_test)
r2 = r2_score(y_pred_dtone,y_test)
print('R^2 of model:',r2)
rmse = np.sqrt(mean_squared_error(y_pred_dtone,y_test))
print('RMSE of model:',rmse)
mae = mean_absolute_error(y_pred_dtone,y_test)
print('MAE of model:',mae)

name = 'Decision Tree'
r2_val.append(r2)
rmse_val.append(rmse)
mae_val.append(mae)
names.append(name)

#Random Forest Regression

rf_reg=RandomForestRegressor()

#Fit the RF model and predict
rf_model = rf_reg.fit(X_train,y_train)
y_pred_rf = rf_model.predict(X_test)

r2 = r2_score(y_test,y_pred_rf)
print('R^2 of model:',r2)
rmse = np.sqrt(mean_squared_error(y_test,y_pred_rf))
print('RMSE of model:',rmse)
mae = mean_absolute_error(y_test,y_pred_rf)
print('MAE of model:',mae)

name = 'Random Forest'
r2_val.append(r2)
rmse_val.append(rmse)
mae_val.append(mae)
names.append(name)

#Support Vector Machine

sv_reg = SVR()
sv_model = sv_reg.fit(X_train,y_train)

y_pred_sv=sv_model.predict(X_test)

r2 = r2_score(y_test,y_pred_sv)
print('R^2 of model:',r2)
rmse = np.sqrt(mean_squared_error(y_test,y_pred_sv))
print('RMSE of model:',rmse)
mae = mean_absolute_error(y_test,y_pred_sv)
print('MAE of model:',mae)

name = 'Support Vector Machine'
r2_val.append(r2)
rmse_val.append(rmse)
mae_val.append(mae)
names.append(name)

#KNN REGRESSOR

knn = KNeighborsRegressor(n_neighbors=1)
knn.fit(X_train, y_train)
pred = knn.predict(X_test)

r2 = r2_score(y_test, pred)
print('R^2 of model:',r2)
rmse = np.sqrt(mean_squared_error(y_test, pred))
print('RMSE of model:',rmse)
mae = mean_absolute_error(y_test,pred)
print('MAE of model:',mae)

knn = KNeighborsRegressor(n_neighbors=7)
knn.fit(X_train, y_train)
pred = knn.predict(X_test)

r2 = r2_score(y_test, pred)
print('R^2 of model:',r2)
rmse = np.sqrt(mean_squared_error(y_test, pred))
print('RMSE of model:',rmse)
mae = mean_absolute_error(y_test,pred)
print('MAE of model:',mae)

name = 'KNN'
r2_val.append(r2)
rmse_val.append(rmse)
mae_val.append(mae)
names.append(name)

for i in range(6):
    print('%s: %f' % (names[i], r2_val[i]))

for i in range(6):
    print('%s: %f' % (names[i], rmse_val[i]))

for i in range(6):
    print('%s: %f' % (names[i], mae_val[i]))

r2_val = list(np.around(np.array(r2_val),3))
rmse_val = list(np.around(np.array(rmse_val),3))
mae_val = list(np.around(np.array(mae_val),3))

from prettytable import PrettyTable
t = PrettyTable(['Regression Model','R^2', 'RMSE', 'MAE'])
t.title = 'CO'
for i in range(6):
  t.add_row([names[i], r2_val[i], rmse_val[i], mae_val[i]])
print(t)

plt.figure(figsize=(22,4))
plt.suptitle('CO')

plt.subplot(1,2,1)
plt.plot(names, rmse_val, marker='o', label='rmse')
plt.plot(names, mae_val, marker='o', color='r', label='mae')
plt.legend()

plt.subplot(1,2,2)
plt.plot(names, r2_val, marker='o', color='g', label='r2')
plt.legend()
plt.show()

"""#Ozone"""

df.columns

col_ = ['PM25', 'PM10', 'NO2', 'CO']

col_

#defining feature (X) and target (y)
X = df[col_]    #X-input features
y = df.iloc[:,5]  #y-input features

#Normalize Feature variable
ss = StandardScaler()
X_std = ss.fit_transform(X)     #apply stardardisation

#Train test split with test size 20% and train size as 80%
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

print('Training data size:',X_train.shape)
print('Test data size:',X_test.shape)
print('Training data size:',y_train.shape)
print('Test data size:',y_test.shape)

names = []
r2_val = []
rmse_val = []
mae_val = []

#Linear Regression

lr = LinearRegression()
lr_model = lr.fit(X_train,y_train)          #fit the linear model on train data

LinearRegression(normalize=False)

#Prediction
y_pred = lr_model.predict(X_test)                   #predict using the model

r2 = r2_score(y_test,y_pred)                        #calculate r2
print('R^2 of model:',r2)
rmse = np.sqrt(mean_squared_error(y_test,y_pred))   #calculate rmse
print('RMSE of model:',rmse)
mae = mean_absolute_error(y_test,y_pred)            #calculate mae
print('MAE of model:',mae)

name = 'Linear Regression'
r2_val.append(r2)
rmse_val.append(rmse)
mae_val.append(mae)
names.append(name)

#Ada Boost Regressor

abr = AdaBoostRegressor()
abr_model = abr.fit(X_train,y_train)

y_pred = abr_model.predict(X_test)
r2 = r2_score(y_test,y_pred)
print('R^2 of model:',r2)
rmse = np.sqrt(mean_squared_error(y_test,y_pred))
print('RMSE of model:',rmse)
mae = mean_absolute_error(y_test,y_pred)
print('MAE of model:',mae)

name = 'AdaBoost'
r2_val.append(r2)
rmse_val.append(rmse)
mae_val.append(mae)
names.append(name)

#Decision Tree Regression

dt_one_reg = DecisionTreeRegressor()

dt_model = dt_one_reg.fit(X_train,y_train)
y_pred_dtone = dt_model.predict(X_test)
r2 = r2_score(y_test,y_pred_dtone)
print('R^2 of model:',r2)
rmse = np.sqrt(mean_squared_error(y_test,y_pred_dtone))
print('RMSE of model:',rmse)
mae = mean_absolute_error(y_test,y_pred_dtone)
print('MAE of model:',mae)

name = 'Decision Tree'
r2_val.append(r2)
rmse_val.append(rmse)
mae_val.append(mae)
names.append(name)

#Random Forest Regression

rf_reg=RandomForestRegressor()

#Fit the RF model and predict
rf_model = rf_reg.fit(X_train,y_train)
y_pred_rf = rf_model.predict(X_test)

r2 = r2_score(y_test,y_pred_rf)
print('R^2 of model:',r2)
rmse = np.sqrt(mean_squared_error(y_test,y_pred_rf))
print('RMSE of model:',rmse)
mae = mean_absolute_error(y_test,y_pred_rf)
print('MAE of model:',mae)

name = 'Random Forest'
r2_val.append(r2)
rmse_val.append(rmse)
mae_val.append(mae)
names.append(name)

#Support Vector Machine

sv_reg = SVR()
sv_model = sv_reg.fit(X_train,y_train)

y_pred_sv=sv_model.predict(X_test)

r2 = r2_score(y_test,y_pred_sv)
print('R^2 of model:',r2)
rmse = np.sqrt(mean_squared_error(y_test,y_pred_sv))
print('RMSE of model:',rmse)
mae = mean_absolute_error(y_test,y_pred_sv)
print('MAE of model:',mae)

name = 'Support Vector Machine'
r2_val.append(r2)
rmse_val.append(rmse)
mae_val.append(mae)
names.append(name)

#KNN REGRESSOR

knn = KNeighborsRegressor(n_neighbors=1)
knn.fit(X_train, y_train)
pred = knn.predict(X_test)

r2 = r2_score(y_test, pred)
print('R^2 of model:',r2)
rmse = np.sqrt(mean_squared_error(y_test, pred))
print('RMSE of model:',rmse)
mae = mean_absolute_error(y_test,pred)
print('MAE of model:',mae)

knn = KNeighborsRegressor(n_neighbors=7)
knn.fit(X_train, y_train)
pred = knn.predict(X_test)

r2 = r2_score(y_test, pred)
print('R^2 of model:',r2)
rmse = np.sqrt(mean_squared_error(y_test, pred))
print('RMSE of model:',rmse)
mae = mean_absolute_error(y_test,pred)
print('MAE of model:',mae)

name = 'KNN'
r2_val.append(r2)
rmse_val.append(rmse)
mae_val.append(mae)
names.append(name)

for i in range(6):
    print('%s: %f' % (names[i], r2_val[i]))

for i in range(6):
    print('%s: %f' % (names[i], rmse_val[i]))

for i in range(6):
    print('%s: %f' % (names[i], mae_val[i]))

r2_val = list(np.around(np.array(r2_val),3))
rmse_val = list(np.around(np.array(rmse_val),3))
mae_val = list(np.around(np.array(mae_val),3))

from prettytable import PrettyTable
t = PrettyTable(['Regression Model','R^2', 'RMSE', 'MAE'])
t.title = 'Ozone'
for i in range(6):
  t.add_row([names[i], r2_val[i], rmse_val[i], mae_val[i]])
print(t)

plt.figure(figsize=(22,4))
plt.suptitle('Ozone')

plt.subplot(1,2,1)
plt.plot(names, rmse_val, marker='o', label='rmse')
plt.plot(names, mae_val, marker='o', color='r', label='mae')
plt.legend()

plt.subplot(1,2,2)
plt.plot(names, r2_val, marker='o', color='g', label='r2')
plt.legend()
plt.show()