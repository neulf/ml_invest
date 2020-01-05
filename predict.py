import numpy as np

import confusion
from sklearn.metrics import confusion_matrix

from bayes_predict import NB_Accuracy, classify
from lr_predict import LR_Accuracy

X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
Y = np.array([1, 2, 1, 3, 1, 4])

#features_test = np.array([[-0.8, -1],[-0.7,-2]])
#labels_test = np.array([1,1])

features_test = np.array([[-0.8, -1],[-0.7,-2]])
labels_test = np.array([1,2])

score = NB_Accuracy(X, Y, features_test, labels_test)
print('GaussianNB %s' % score)

X_train = X
y_train = Y
X_test = features_test
y_test = labels_test
cls = classify(X,Y)
print('Traing score : %.2f' % cls.score(X_train, y_train))
print('Testing score : %.2f' % cls.score(X_test, y_test))
