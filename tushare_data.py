import tushare as ts
import pandas as pd
from sqlalchemy import create_engine
import sqlalchemy

# df = ts.get_gdp_quarter()
# print(df)

pro = ts.pro_api("0da7a72463339b39f11671683c2c23a466b42c82ccae5a6aace10e6f")


# df = pro.trade_cal(exchange='', start_date='20180901', end_date='20181001', fields='exchange,cal_date,is_open,pretrade_date', is_open='0')
# print(df)

# df = pro.new_share(start_date='20191201', end_date='20200101')
# df = pro.fut_daily(trade_date='20200103', exchange='DCE', fields='ts_code,trade_date,pre_close,pre_settle,open,high,low,close,settle,vol')

# df = pro.fut_basic(exchange='DCE', fut_type='1', fields='ts_code,symbol,name,list_date,delist_date')
# df.to_csv("fu.csv")

# df = pro.fut_mapping(ts_code='BB.DCE',trade_date="20200102")
# print(df)

def all_ts_to_db(exg, ifExists):
    df = pro.fut_basic(exchange=exg, fut_type='1', fields='ts_code,symbol,name,list_date,delist_date')

    engine = create_engine("sqlite:///data/future_data.db")
    df.to_sql('ts_base', engine, if_exists=ifExists)
    return


if __name__ == "__main__":
    """
    all_ts_to_db("DCE", "replace")
    all_ts_to_db("SHFE", "append")
    all_ts_to_db("CZCE", "append")
    all_ts_to_db("CFFEX", "append")
    all_ts_to_db("INE", "append")
    """


    # 获取主力合约TF.CFX每日对应的月合约
    # df = pro.fut_mapping(ts_code='TF.CFX', trade_date="20190123")
    # print(df)

    # df = pro.fut_basic(exchange="CFX", fut_type='1', fields='ts_code,symbol,name,list_date,delist_date')
    # print(df)

    df = pro.fut_holding(trade_date='20181113', symbol='MA', exchange='CZCE')
    print(df)

    print(df.size)

    print("ok")