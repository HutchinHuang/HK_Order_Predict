# Select The Best Linear Regression Model with the Smallest MSE Via Cross-Validation.
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
with open("./HK_data_test.csv") as file:
    file.readline()  # skip the header
    data = np.loadtxt(file, delimiter=",")
# print(type(data)) 类型是np.ndarray

X = data[:, 1:-1]  # select columns 2 through -1
# X = data[:, [2,3,4,-2,-1]] In Order to Get Certain Columns.
y = data[:, -1]   # select column -1, the order num
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=24)
'''
# Check The Data Imported From Csv.
print(len(X_test))
print("===========")
print(len(X_train))
print("***********")
print(y_test)
print("===========")
print(y_train)
'''
# Linear Regression And Then Prediction.
lr = LinearRegression()
lr.fit(X_train, y_train)
y_predict_lr = lr.predict(X_test)
print(y_predict_lr)
print(lr.score(X_test, y_test))
print(r2_score(y_test, y_predict_lr))
print(mean_squared_error(y_test, y_predict_lr))
