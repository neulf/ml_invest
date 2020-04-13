#!/usr/bin/env python3
import okex.account_api as account
import okex.futures_api as future
import okex.lever_api as lever
import okex.spot_api as spot
import okex.swap_api as swap
import okex.index_api as index
import okex.option_api as option
import json
import logging
import datetime

from time_untils import now_datetime

api_key = "2cef398f-e86a-4ba8-a665-68535660f5bd"
secret_key = "5D2BE14F30AD59CE0B7F6D5E828CF334"
passphrase = "lf790211"

host = "192.168.68.12"
username = "neulf"
password = "lf790211"
database = "future_data"

log_format = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(filename='mylog-rest.json', filemode='a', format=log_format, level=logging.INFO)

def get_timestamp():
    now = datetime.datetime.now()
    t = now.isoformat("T", "milliseconds")
    return t + "Z"


time = get_timestamp()


def update_info():
    accountAPI = account.AccountAPI(api_key, secret_key, passphrase, False)

    # 获取账户资产估值 （1次/20s）
    result = accountAPI.get_asset_valuation(valuation_currency="USD")

    print(time + json.dumps(result))
    logging.info("result:" + json.dumps(result))
    print("账户资产估值：" + str(round(result["balance"],2)))
    print("每份资产估值：" + str(round(result["balance"]/28, 2)))

    import pymysql

    # 打开数据库连接
    db = pymysql.connect(host, username, password, database)

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # 使用 execute()  方法执行 SQL 查询
    cursor.execute("update fundinfo_summaryinfo set all_amount = {}, one_part_amount = {}, update_time='{}' where fund_name_en = '{}'"
                   .format(round(result["balance"],2), round(result["balance"]/28, 2), now_datetime(), "000001"))

    # 使用 fetchone() 方法获取单条数据.
    # data = cursor.fetchone()

    db.commit()
    # print("更新 %s 条数据" % data)

    # 关闭数据库连接
    db.close()

    return


if __name__ == "__main__":
    update_info()