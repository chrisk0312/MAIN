#https://dacon.io/competitions/open/235610/data

import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import OneHotEncoder
from keras.callbacks import EarlyStopping
import time
from sklearn.svm import LinearSVR
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier
from xgboost import XGBClassifier



#1. 데이터
path = "C:\\_data\\daicon\\wine\\"



train_csv = pd.read_csv(path + 'train.csv', index_col= 0)
print(train_csv)
test_csv = pd.read_csv(path + 'test.csv', index_col= 0)
print(test_csv)
submission_csv = pd.read_csv(path + "sample_submission.csv")
print(submission_csv)

print(train_csv.shape) #(5497, 13)
print(test_csv.shape) #(1000, 12)
print(submission_csv.shape) #(1000, 2)


print(train_csv.columns) #'quality', 'fixed acidity', 'volatile acidity', 'citric acid',
    #    'residual sugar', 'chlorides', 'free sulfur dioxide',
    #    'total sulfur dioxide', 'density', 'pH', 'sulphates', 'alcohol',
    #    'type'],
    
x = train_csv.drop(['quality'], axis= 1)
print(x)
y = train_csv['quality']-3



x.loc[x['type'] == 'red', 'type'] = 1
x.loc[x['type'] == 'white', 'type'] = 0
print(x)

test_csv.loc[test_csv['type'] == 'red', 'type'] = 1
test_csv.loc[test_csv['type'] == 'white', 'type'] = 0

print(test_csv)



#print(x.shape,y.shape) #(5497, 12) (5497, 7)




x_train, x_test, y_train, y_test = train_test_split(x, y, train_size= 0.8, shuffle= True, random_state=364, stratify= y)

from sklearn.preprocessing import MinMaxScaler, MaxAbsScaler
from sklearn.preprocessing import StandardScaler, RobustScaler

#mms = MinMaxScaler()
#mms = StandardScaler()
#mms = MaxAbsScaler()
mms = RobustScaler()

mms.fit(x_train)
x_train= mms.transform(x_train)
x_test= mms.transform(x_test)


#2. 모델구성
models = [DecisionTreeClassifier(), RandomForestClassifier(), GradientBoostingClassifier(), XGBClassifier()]

for model in models:
    model.fit(x_train, y_train)
    results = model.score(x_test,y_test) #분류에서는 (디폴트값)acc 빼줌 회귀는 r2
    y_predict = model.predict(x_test)
    acc = accuracy_score(y_predict, y_test)
    print(type(model).__name__, "acc :", acc)
    print(type(model).__name__, ':', model.feature_importances_)
        

test_csv = (test_csv)

y_submit = model.predict(test_csv)


y_submit = (y_submit)+3
submission_csv['quality'] = y_submit
#acc = accuracy_score(y_predict, y_test)
ltm = time.localtime(time.time())
#print("acc :", acc)
print("로스 :", results)
save_time = f"{ltm.tm_year}{ltm.tm_mon}{ltm.tm_mday}{ltm.tm_hour}{ltm.tm_min}{ltm.tm_sec}" 
submission_csv.to_csv(path+f"submission_{save_time}e.csv", index=False)




print("걸린 시간 :", round(end_time - start_time, 2), "초" )

#minmax
#acc : 0.5581818181818182
#로스 : 1.0659217834472656

#StandardScaler
#acc : 0.5681818181818182
#로스 : 1.0569180250167847

#MaxAbsScaler()
#acc : 0.5709090909090909
#로스 : 1.0683833360671997

#mms = RobustScaler()
#acc : 0.5609090909090909
#로스 : 1.0590828657150269

#LinearSVR()
# model.score: 0.2888460317435524
# 로스 : 0.2888460317435524

# DecisionTreeClassifier acc : 0.5745454545454546
# DecisionTreeClassifier : [0.06461628 0.11042118 0.06893686 0.08386408 0.0954351  0.08462122
#  0.08668209 0.08438739 0.08273942 0.09039276 0.14600391 0.00189971]
# RandomForestClassifier acc : 0.6727272727272727
# RandomForestClassifier : [0.07385647 0.1002922  0.08077489 0.08490105 0.086459   0.08501067
#  0.09118079 0.10090457 0.08263846 0.0868306  0.12354298 0.00360833]
# GradientBoostingClassifier acc : 0.6018181818181818
# GradientBoostingClassifier : [0.04195664 0.15335656 0.04734851 0.07652747 0.06093943 0.05854147
#  0.06190635 0.06334744 0.04640791 0.06877852 0.31516637 0.00572331]
# XGBClassifier acc : 0.6627272727272727
# XGBClassifier : [0.0657826  0.09354989 0.06135033 0.06598268 0.06206436 0.07210352
#  0.06398375 0.05954533 0.05898329 0.07156365 0.17753017 0.14756043]