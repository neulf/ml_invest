import os
import sqlite3
# from sqlalchemy import create_engine
# import sqlalchemy
import datetime
import time
from sqlite3 import Cursor

"""
计算生成实际的操盘结果
"""
def calc_op(prodCode, tradeDate):
    # 获取一条数据(品种、日期)
    # 得到该记录未来N个交易日的交易数据
    # 计算按照狭义赔率思维操作的结果
    # 注意需要判断是否即将换月，如果14个交易日即将换月，则使用下一个主力合约

    # 重要参数, 通过这两个参数就能确定赔率
    lossPoint = 100  # 止损点数
    winPoint = 200  # 止盈点数

    # 重要参数, 最多观察的天数，包含当天
    watchDays = 14
    # 重要参数， 交割前多少天采用次主力合约
    moveupDays = 60

    # select * from ts_base  where ts_code='TF1903.CFX'
    # 得到交易日期


    return