"""
将按日期的数据进入数据库
"""
import os
import sqlite3
# from sqlalchemy import create_engine
# import sqlalchemy
import datetime
import time
from sqlite3 import Cursor
import tushare as ts
from string import digits
import re
import pandas as pd

from calc_labels import GetProdInfos

pro = ts.pro_api("0da7a72463339b39f11671683c2c23a466b42c82ccae5a6aace10e6f")

def getcellbyname(headers, rows, colName):
    for i in range(0, len(headers)):
        # print(headers[i])
        # print(colName == headers[i])
        if headers[i] == colName:
            return rows[i]

    return 0


def getprodcodebyname(name):
    code = "-"
    return code

def fill_db(start_date="", end_date="", exchange="", ts_code=""):
    prods = GetProdInfos()

    df = pro.fut_daily(start_date=start_date, end_date = end_date, exchange=exchange, ts_code=ts_code,
                       fields="ts_code,trade_date,pre_close,pre_settle,open,high,low,close,settle,vol")

    conn = sqlite3.connect('data/future_data.db')
    # 创建一个Cursor:
    cursor: Cursor = conn.cursor()

    # print(df)
    for i in range(df.shape[0]):
        # print(df.iloc[i].loc["trade_date"])
        sql = "insert into predict_base_data(prod_code, prod_name_cn, p_date, p_str_date,op_ts_code) values (?,?,?,?,?)"
        pstr_date = df.iloc[i].loc["trade_date"]
        p_date = datetime.datetime.strptime(pstr_date, "%Y%m%d").strftime("%Y-%m-%d")
        ts_code = df.iloc[i].loc["ts_code"]
        # print(ts_code)

        # prod_code= ""
        if bool(re.search(r'\d{4}', ts_code)) :
            continue

        prod_code = ts_code

        if prods.loc[prods.full_prod_code == ts_code,"prod_name"].size == 0:
            continue

        prod_name_cn = prods.loc[prods.full_prod_code == prod_code, "prod_name"].iloc[0]
        # print(prod_name_cn)

        cursor.execute(sql,(prod_code,prod_name_cn,p_date,pstr_date,ts_code))

    conn.commit()
    cursor.close()
    conn.close()
    return

def data_to_db(filepath):
    # 青松,黑金期货,试错交易,灰天鹅,未来航情,晨先财经,云数据,逍遥论期,立鹤论期
    # 青松,黑金期货,微语解期,灰天鹅,未来航情,抓牛在手,云数据,逍遥论期,青石
    # 青松,黑金期货,微语解期,灰天鹅,未来航情,抓牛在手,云数据,逍遥论期,青石
    # 青松,黑金期货,试错交易,微语解期,灰天鹅,未来航情,晨先财经,抓牛在手,云数据,逍遥论期,立鹤论期,青石

    # 获取基础信息，建议放入数据库
    # http://www.khqihuo.com/spqh/560.html

    predict_mapping = dict(p1="青松讲盘", p2="黑金期货", p3="试错交易", p4="微语解期", p5="灰天鹅", p6="未来航情", p7="晨先财经", p8="抓牛在手",
                           p9="云数据",
                           p10="逍遥论期", p11="立鹤论期", p12="青石看盘", p13="国投安信", p14="乡村牛童", p15="相遇点评", p16="", p17="", p18="", p19="",
                           p20="李昉")
    # print(predict_mapping.get("p2"))

    import csv
    filename = os.path.basename(filepath)
    strdate = filename.replace("future", "").replace(".csv", "")
    tdate = time.strptime(strdate, "%Y%m%d")

    # print(time.strftime(r"%Y/%m/%d",tdate))

    # engine = create_engine("sqlite:///data/future_data.db")
    # 连接到SQLite数据库
    # 数据库文件是test.db
    # 如果文件不存在，会自动在当前目录创建:
    conn = sqlite3.connect('data/future_data.db')
    # 创建一个Cursor:
    cursor: Cursor = conn.cursor()

    with open(filepath, encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        for i, rows in enumerate(reader):
            if i == 0:
                theader = rows

            if i > 0:
                # 创建一个Cursor:
                # cursor: Cursor = conn.cursor()

                # print(len(theader))
                # print(getcellbyname(theader, rows, "商品名称"))
                # 继续执行一条SQL语句，插入一条记录:

                cursor.execute(
                    r"insert into predict_base_data (prod_code, prod_name_cn, p_date, p_str_date, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16, p17, p18, p19, p20) values ("
                    r"'{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', "
                    r"'{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}') "
                        .format(getcellbyname(theader, rows, "商品代码"), getcellbyname(theader, rows, "商品名称"), time.strftime(r"%Y-%m-%d", tdate), strdate,
                                getcellbyname(theader, rows, predict_mapping["p1"]),
                                getcellbyname(theader, rows, predict_mapping["p2"]),
                                getcellbyname(theader, rows, predict_mapping["p3"]),
                                getcellbyname(theader, rows, predict_mapping["p4"]),
                                getcellbyname(theader, rows, predict_mapping["p5"]),
                                getcellbyname(theader, rows, predict_mapping["p6"]),
                                getcellbyname(theader, rows, predict_mapping["p7"]),
                                getcellbyname(theader, rows, predict_mapping["p8"]),
                                getcellbyname(theader, rows, predict_mapping["p9"]),
                                getcellbyname(theader, rows, predict_mapping["p10"]),
                                getcellbyname(theader, rows, predict_mapping["p11"]),
                                getcellbyname(theader, rows, predict_mapping["p12"]),
                                getcellbyname(theader, rows, predict_mapping["p13"]),
                                getcellbyname(theader, rows, predict_mapping["p14"]),
                                getcellbyname(theader, rows, predict_mapping["p15"]),
                                getcellbyname(theader, rows, predict_mapping["p16"]),
                                getcellbyname(theader, rows, predict_mapping["p17"]),
                                getcellbyname(theader, rows, predict_mapping["p18"]),
                                getcellbyname(theader, rows, predict_mapping["p19"]),
                                getcellbyname(theader, rows, predict_mapping["p20"])))

                # 通过rowcount获得插入的行数:
                # cursor.rowcount
    # 关闭Cursor:
    cursor.close()
    # 提交事务:
    conn.commit()

    # 关闭Connection:
    conn.close()
    return


def find_daily_record(begin_date):
    import glob

    folder = begin_date.strftime("%Y/%m")

    listglob = []
    listglob = glob.glob(r"data/{0}/future*.csv".format(folder))
    listglob.sort()
    # print(listglob)
    # return

    str_date = begin_date.strftime("%Y%m%d")


    for filepath in listglob:
        filename = os.path.basename(filepath)
        if filename >= "future{}.csv".format(str_date):
            data_to_db("data/{0}/{1}".format(folder, filename))

    return

def xxx():
    # 连接到SQlite数据库
    conn = sqlite3.connect("data/future_data.db")
    # 创建一个cursor：
    cursor = conn.cursor()
    # 执行查询语句：

    if prod_code == "":
        df = pd.read_sql_query("select full_prod_code from prod_base where p_str_date>=:dstart and p_str_date<=:dfinish",
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
    return

def test():
    df = pro.fut_daily(start_date="20190101", end_date = "20191231", ts_code="RB.SHF",
                       fields="ts_code,trade_date,pre_close,pre_settle,open,high,low,close,settle,vol")

    print(df)

    print(bool(re.search(r'\d{4}', "RB2051.SHF")))
    return

if __name__ == "__main__":
    # data_to_db("data/future20191231.csv")
    # find_daily_record(datetime.datetime.strptime("20200101","%Y%m%d"))
    fill_db(start_date="20180101", end_date="20181231", ts_code="RB.SHF")
    # test()
