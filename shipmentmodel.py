 
import pandas as pd
import numpy as np

ship= pd.read_csv("/Users/shaguftajahan/Downloads/shipments.csv")
ship1 = ship.copy()
ship1=ship1.drop(['ID'],axis=1)
ship1.drop(ship1[(ship1['Prior_purchases'] >5)].index, inplace=True)

#saving dataset with new indexing
ship1.to_csv("ship1_new.csv", index = False)
ship1_new = pd.read_csv("ship1_new.csv")
ship1_new

#creating dummy variables to convert categorical data into numerical data
#using one hot encoder
ship1_new = pd.get_dummies(ship1_new, columns = ['Warehouse_block','Mode_of_Shipment','Product_importance'])

from sklearn import preprocessing
label_encoder = preprocessing.LabelEncoder()
ship1_new['Gender']= label_encoder.fit_transform(ship1_new['Gender'])

# imputation of outlier values in discount offered column
from sklearn.linear_model import LinearRegression
lr = LinearRegression()
 
# dividing the data into train and test
#test part is outlier values
#train part is rest data
testdf = ship1_new[ship1_new['Discount_offered']>20]
traindf = ship1_new[ship1_new['Discount_offered']<=20]

traindf1 = traindf.copy()
y = traindf1['Discount_offered'] 
traindf2 = traindf1.drop("Discount_offered",axis=1)

#fit the train part of the data into model
lr.fit(traindf2,y)

testdf1 = testdf.copy() 
testdf1

testdf2 = testdf1.drop('Discount_offered', 1)
testdf2

#predicting the value of test data
pred = lr.predict(testdf2)
pred

y_test = testdf1['Discount_offered']

#putting the value of predicted value for model formation
testdf1['Discount_offered']= pred
traindf1['Discount_offered']=y


y = traindf1['Reached.on.Time_Y.N']
traindf1.drop("Reached.on.Time_Y.N",axis=1,inplace=True)
from sklearn.linear_model import LogisticRegression
logr = LogisticRegression()
logr.fit(traindf1,y)
LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
                   intercept_scaling=1, l1_ratio=None, max_iter=100,
                   multi_class='auto', n_jobs=None, penalty='l2',
                   random_state=None, solver='lbfgs', tol=0.0001, verbose=0,
                   warm_start=False)
y_test = testdf1['Reached.on.Time_Y.N']
testdf1.drop("Reached.on.Time_Y.N",axis=1,inplace=True)
pred = logr.predict(testdf1)

from sklearn import metrics
print(metrics.accuracy_score(pred,y_test))

import pickle
pickle_out = open('new_model.pkl','wb')
pickle.dump(logr,pickle_out)#saving our model in .pkl file 
pickle_out.close()


