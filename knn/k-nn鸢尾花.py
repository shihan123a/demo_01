#!/usr/bin/python
# -*- coding: utf-8 -*-
# KNN调用
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn import datasets
# 导入鸢尾花数据并查看数据特征
iris = datasets.load_iris()
print('数据量',iris.data.shape)
# 拆分属性数据
iris_X = iris.data
# 拆分类别数据
iris_y = iris.target
# 方法一：拆分测试集和训练集,并进行预测
iris_train_X , iris_test_X, iris_train_y ,iris_test_y = train_test_split(iris_X, iris_y, test_size=0.2,random_state=0)
# knn = KNeighborsClassifier(n_neighbors=3)
# knn.fit(iris_train_X, iris_train_y)
# knn.predict(iris_test_X)
# 方法二：拆分测试集和训练集
np.random.seed(0)
# permutation随机生成0-150的系列
indices = np.random.permutation(len(iris_y))
iris_X_train = iris_X[indices[:-30]]
iris_y_train = iris_y[indices[:-30]]
iris_X_test = iris_X[indices[-30:]]
iris_y_test = iris_y[indices[-30:]]
knn = KNeighborsClassifier()
# 提供训练集进行顺利
knn.fit(iris_X_train, iris_y_train)
# 预测测试集鸢尾花类型
predict_result = knn.predict(iris_X_test)
print('预测结果',predict_result)
# 计算预测的准确率
print('预测准确率',knn.score(iris_X_test, iris_y_test))