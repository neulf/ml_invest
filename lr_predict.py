def classify(features_train, labels_train):
    import numpy as np
    from sklearn.linear_model import LogisticRegression
    X = features_train
    Y = labels_train
    clf = LogisticRegression()
    clf.fit(X, Y)
    return clf


def LR_Accuracy(features_train, labels_train, features_test, labels_test):
    """ 计算分类器的准确率"""
    ### 导入sklearn模块的LogisticRegression
    from sklearn.linear_model import LogisticRegression

    ### 创建分类器
    clf = LogisticRegression()

    ### 训练分类器
    X = features_train
    Y = labels_train
    clf.fit(X, Y)

    ### 用训练好的分类器去预测测试集的标签值
    pred = clf.predict(features_test)

    ### 计算并返回在测试集上的准确率
    from sklearn.metrics import accuracy_score
    y_pred = pred
    y_true = labels_test
    accuracy_score(y_true, y_pred)

    return accuracy_score(y_true, y_pred, normalize=False)