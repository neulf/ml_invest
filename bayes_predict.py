from sklearn.metrics import confusion_matrix
from confusion import plot_confusion_matrix


def classify(features_train, labels_train):
    import numpy as np
    from sklearn.naive_bayes import GaussianNB
    X = features_train
    Y = labels_train
    clf = GaussianNB()
    clf.fit(X, Y)
    return clf


def NB_Accuracy(features_train, labels_train, features_test, labels_test):
    """ 计算分类器的准确率"""
    ### 导入sklearn模块的GaussianNB
    from sklearn.naive_bayes import GaussianNB

    ### 创建分类器
    clf = GaussianNB()

    ### 训练分类器
    X = features_train
    Y = labels_train
    clf.fit(X, Y)

    ### 用训练好的分类器去预测测试集的标签值
    pred = clf.predict(features_test)

    print("预测值:")
    print(pred)

    ### 计算并返回在测试集上的准确率
    from sklearn.metrics import accuracy_score
    y_pred = pred
    y_true = labels_test
    accuracy_score(y_true, y_pred)

    cm = confusion_matrix(y_true, y_pred)
    import matplotlib.pyplot as plt

    class_names = [0, 1]
    plt.figure()
    plot_confusion_matrix(cm, classes=class_names, title='Confusion matrix')
    plt.show()

    return accuracy_score(y_true, y_pred, normalize=False)
    #return plt