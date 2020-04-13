import os
import sqlite3
# from sqlalchemy import create_engine
# import sqlalchemy
import datetime
import time
from sqlite3 import Cursor
import tushare as ts
import pandas as pd

from time_untils import DateAddDays, now_date

pro = ts.pro_api("0da7a72463339b39f11671683c2c23a466b42c82ccae5a6aace10e6f")

# 重要常量, 最多观察的天数，包含当天
watch_days = 30

def GetProdInfos():
    # select * from prod_base
    # 连接到SQlite数据库
    conn = sqlite3.connect("data/future_data.db")
    df = pd.read_sql_query("select * from prod_base", conn, index_col="prod_code")

    # print(df)
    conn.close()
    return df

# 计算准备
def PreCalc(prod_code, start_date, end_date):
    if DateAddDays(start_date,watch_days) > now_date():
        print("日期超过了最大处理时间")
        return

    prods = GetProdInfos()

    # 连接到SQlite数据库
    conn = sqlite3.connect("data/future_data.db")
    # 创建一个cursor：
    cursor = conn.cursor()
    # 执行查询语句：

    if prod_code == "":
        cursor.execute('select * from predict_base_data where p_str_date>? and p_str_date<?', (start_date,end_date))
    else:
        cursor.execute('select * from predict_base_data where prod_code = ? and p_str_date>? and p_str_date<?', (prod_code,start_date,end_date))

    # 使用featchall获得结果集（list）
    values = cursor.fetchall()
    for v in values:
        # 为合约的每一个交易日准别数据
        vdate = v[4]
        vcode = v[1]
        main_ts = GetMainTS(vcode, vdate)
        # print(main_ts)
        quotations = GetTSQuotations(main_ts,vdate)
        # print(quotations)
        # 为合约的每一个交易日准别数据
        CalcOp(cursor, vcode, vdate, main_ts, quotations, prods)

    # 关闭cursor
    # 关闭conn
    conn.commit()
    cursor.close()
    conn.close()

    return


# 计算生成实际的操盘结果
def CalcOp(cursor, prod_code, trade_date, ts_code, quotations, prods):
    # 获取一条数据(品种、日期)
    # 得到该记录未来N个交易日的交易数据
    # 计算按照狭义赔率思维操作的结果

    # 重要常量, 通过这两个参数就能确定赔率
    lossPoint = prods.loc[prods.full_prod_code == prod_code, "loss_point"].iloc[0]  # 止损点数
    winPoint = prods.loc[prods.full_prod_code == prod_code, "win_point"].iloc[0]  # 止盈点数

    point_value = prods.loc[prods.full_prod_code == prod_code, "unit_earnings"].iloc[0] # 波动每点盈利
    min_moveup = prods.loc[prods.full_prod_code == prod_code, "min_point"].iloc[0] # 最小变动单位

    # 做多下单价（暂定比最高价格低一个价格变动单位）
    bull_order_price = quotations.iloc[0].loc["high"] - min_moveup
    # print(bull_order_price)
    # 做空下单价（暂定比最低价高一个价格变动单位）
    brear_order_price = quotations.iloc[0].loc["low"] + min_moveup

    op = "0" # 闲
    out_flag = 0
    earnings = 0
    for i in range(quotations.shape[0]):
        # print(i)

        # 先计算开多，再计算开空
        # 下单价
        if out_flag > 0:
            break

        if i > 0:
            if (quotations.iloc[i].loc["high"] - bull_order_price) / min_moveup >= winPoint:
                # 多止盈
                op = "1" # 多
                # 止盈价
                win_price = bull_order_price + winPoint * min_moveup
                print("下单价:{0},多止盈价：{1} 下单时间:{2},下单操作:{3}".format(bull_order_price, win_price, trade_date, op))
                earnings = (win_price - bull_order_price) * point_value / min_moveup
                out_flag = 1
                break

            if (brear_order_price - quotations.iloc[i].loc["low"]) / min_moveup >= winPoint:
                # 空止盈
                op = "-1" # 空
                # 止盈价
                win_price = brear_order_price - winPoint * min_moveup
                print("下单价:{0},空止盈价：{1} 下单时间:{2},下单操作:{3}".format(brear_order_price, win_price, trade_date, op))
                earnings = (brear_order_price - win_price) * point_value / min_moveup
                out_flag = 1
                break

        # print(q)

    sql = "update predict_base_data set true_op = ?, op_ts_code = ?, earnings = ? where prod_code = ? and p_str_date = ?"
    cursor.execute(sql,(op, ts_code, earnings, prod_code, trade_date))
    # update predict_base_data set true_op = '闲', op_ts_code = 'xxx', earnings = 123 where prod_code = '' and p_str_date = ''
    # select * from ts_base  where ts_code='TF1903.CFX'
    # 得到交易日期

    return

# 得到主力合约
def GetMainTS(prod_code, trade_date):
    # select * from ts_base where ts_code = ? and delist_date > ? order by delist_date limit 1,1
    # cursor.execute(r"select * from ts_base where ts_code = ? and delist_date > ? order by delist_date limit 1,1", (ts_code, delist_date))
    #one = cursor.fetchone()
    # print(one)
    df = pro.fut_mapping(ts_code = prod_code, trade_date = trade_date)
    ts_code = df["mapping_ts_code"].iloc[0]
    # print(ts_code)
    # ts_code = df
    return ts_code

def GetTSQuotations(ts_code, trade_date):
    df = pro.fut_daily(ts_code=ts_code, start_date=trade_date, end_date=DateAddDays(trade_date, watch_days)).sort_index(ascending=False)
    return df


def GetWinLossPoints():
    """

    :return:
    """
    return

if __name__ == "__main__":
    PreCalc("RB.SHF", "20191230", "20200220")
    # df = GetProdInfos()
    # print(df.loc[df.full_prod_code == "RB.SHF", "win_point"].iloc[0])

    # print(GetMainTS("MA.ZCE","20191218"))