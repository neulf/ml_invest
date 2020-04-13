import datetime


def DateAddDays(strDate, days):
    tdate = datetime.datetime.strptime(strDate, "%Y%m%d") + datetime.timedelta(days=days)

    return tdate.strftime("%Y%m%d")

def now_date():
    now_date = datetime.datetime.now().strftime("%Y%m%d")
    return now_date

def now_datetime():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return now

if __name__ == "__main__":
    print(DateAddDays("20200126", -10))
    print(DateAddDays("20200126", 10))
