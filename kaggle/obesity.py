import numpy as np
import pandas as pd
from keras.models import Sequential, load_model
from keras.layers import Dense,Dropout,BatchNormalization, AveragePooling1D, Flatten, Conv2D, LSTM, Bidirectional,Conv1D,MaxPooling1D
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler, MinMaxScaler, Normalizer, RobustScaler
from sklearn.metrics import accuracy_score, f1_score
from lightgbm import LGBMClassifier

path= "c:/_data/kaggle/obesity/"
train=pd.read_csv(path+"train.csv",index_col=0)
test=pd.read_csv(path+"test.csv",index_col=0)
sample=pd.read_csv(path+"sample_submission.csv")
x= train.drop(['NObeyesdad'],axis=1)
y= train['NObeyesdad']

lb = LabelEncoder()

# 라벨 인코딩할 열 목록
columns_to_encode = ['Gender','family_history_with_overweight','FAVC','CAEC','SMOKE','SCC','CALC','MTRANS']

# 데이터프레임 x의 열에 대해 라벨 인코딩 수행
for column in columns_to_encode:
    lb.fit(x[column])
    x[column] = lb.transform(x[column])

# 데이터프레임 test_csv의 열에 대해 라벨 인코딩 수행
for column in columns_to_encode:
    lb.fit(test[column])
    test[column] = lb.transform(test[column])
    
# print(x['Gender'])
# print(test['CALC'])
x_train,x_test,y_train,y_test=train_test_split(x,y,train_size=0.90,random_state=777777,stratify=y)

# print(x_train.shape,y_train.shape)  #(18682, 16) (18682,)
# print(x_test.shape,y_test.shape)    #(2076, 16) (2076,)

random_state = 277
lgbm_params = {"objective": "multiclass",
               "metric": "multi_logloss",
               "verbosity": -1,
               "boosting_type": "gbdt",
               "random_state": random_state,
               "num_class": 7,
               "learning_rate" :  0.01386432121252535,
               'n_estimators': 494,         #에포
               'feature_pre_filter': False,
               'lambda_l1': 1.2149501037669967e-07,
               'lambda_l2': 0.9230890143196759,
               'num_leaves': 31,
               'feature_fraction': 0.5,
               'bagging_fraction': 0.5523862448863431,
               'bagging_freq': 4,
               'min_child_samples': 20}

model = LGBMClassifier(**lgbm_params)

# 모델 학습
model.fit(x_train, y_train)

# 테스트 데이터에 대한 예측
y_pred = model.predict(x_test)
y_submit = model.predict(test)
sample['NObeyesdad']=y_submit

sample.to_csv(path + "obesity25.csv", index=False)
# 정확도 평가
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
'''


from sklearn.model_selection import GridSearchCV

# Define the parameter grid
param_grid = {
    'n_estimators': [100, 200, 300, 400, 500],
    'learning_rate': [0.01, 0.05, 0.1],
    'num_leaves': [20, 30, 40],
    # Add more parameters here
}

# Create a GridSearchCV object
grid = GridSearchCV(LGBMClassifier(objective='multiclass', metric='multi_logloss', verbosity=-1, boosting_type='gbdt', random_state=277, num_class=7), param_grid, cv=5)

# Fit the GridSearchCV object to the data
grid.fit(x_train, y_train)

# Print the best parameters
print(grid.best_params_)

# Use the best model
model = grid.best_estimator_

# Make predictions on the test data
y_pred = model.predict(x_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Make predictions on the test data
y_submit = model.predict(test)

# Create a submission DataFrame and save it to a CSV file
sample['NObeyesdad'] = y_submit
sample.to_csv(path + "obesity22.csv", index=False)
'''