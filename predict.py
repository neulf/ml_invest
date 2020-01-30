import numpy as np
import sqlite3
import pandas as pd

import confusion
from sklearn.metrics import confusion_matrix

from bayes_predict import NB_Accuracy, classify
from lr_predict import LR_Accuracy

def get_input_data(prod_code, start_date, end_date):
    # 连接到SQlite数据库
    conn = sqlite3.connect("data/future_data.db")
    # 创建一个cursor：
    cursor = conn.cursor()
    # 执行查询语句：

    if prod_code == "":
        df = pd.read_sql_query("select prod_code,p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,p15,p16,p17,p18,p19,p20 from predict_base_data where p_str_date>=:dstart and p_str_date<=:dfinish",
                               conn,
                               params={"dstart":start_date,"dfinish":end_date},
                               index_col="prod_code")

        df_label = pd.read_sql_query("select true_op from predict_base_data where p_str_date>=:dstart and p_str_date<=:dfinish",
                               conn,
                               params={"dstart":start_date,"dfinish":end_date})
    else:
        df = pd.read_sql_query("select p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,p15,p16,p17,p18,p19,p20 from predict_base_data where prod_code = :prod_code and p_str_date>=:dstart and p_str_date<=:dfinish",
                               conn,
                               params={"prod_code":prod_code,"dstart":start_date,"dfinish":end_date})

        df_label = pd.read_sql_query("select true_op from predict_base_data where prod_code = :prod_code and p_str_date>=:dstart and p_str_date<=:dfinish",
                               conn,
                               params={"prod_code":prod_code,"dstart":start_date,"dfinish":end_date})

    # params={"dstart":datetime(2014,6,24,16,0),"dfinish":datetime(2014,6,24,17,0)}
    print(df.values)
    arr_label = [i for item in df_label.values for i in item]
    print(arr_label)

    return (df.values, arr_label)


# 通过训练集进行训练，并用测试集进行测试
def valid(prod_code, start_date, end_date, test_start_date, test_end_date):
    train_data = get_input_data(prod_code, start_date, end_date)

    features_train = train_data[0]
    labels_train = train_data[1]

    test_data = get_input_data(prod_code, test_start_date, test_end_date)

    features_test = test_data[0]
    labels_test = test_data[1]

    score = NB_Accuracy(features_train, labels_train, features_test, labels_test)
    print('GaussianNB %s' % score)

    X_train = features_train
    y_train = labels_train
    X_test = features_test
    y_test = labels_test
    cls = classify(features_train, labels_train)
    print('Traing score : %.2f' % cls.score(X_train, y_train))
    print('Testing score : %.2f' % cls.score(X_test, y_test))
    return

def predict(prod_code, start_date, end_date, pred_start_date, pred_end_date):
    train_data = get_input_data(prod_code, start_date, end_date)

    features_train = train_data[0]
    labels_train = train_data[1]

    pred_data = get_input_data(prod_code, pred_start_date, pred_end_date)

    print(pred_data[0])

    clf = classify(features_train,labels_train)
    op = clf.predict(pred_data[0])

    if type(op) is np.ndarray:
        print("推荐操作:操作集合")
    else:
        if op == 0:
            op_display="空"
        elif op == 1:
            op_display = "闲"
        elif op == 2:
            op_display = "多"
        else:
            op_display = "未知"
        print("推荐操作:{0}".format(op_display))

    return op

if __name__ == "__main__":
    # predict()
    predict("RB.SHF","20191231","20200103","20200102","20200110")