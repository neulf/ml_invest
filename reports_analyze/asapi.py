import urllib.request as request
from bs4 import BeautifulSoup
import pandas as pd

departs = []

def statistics(url):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    headers = {'User-Agent': user_agent}
    req = request.Request(url, headers=headers)

    # chardet.detect(data1)
    html = request.urlopen(req).read()
    soup = BeautifulSoup(html,"lxml")

    '''
    import re
    for tag in soup.find_all("div", class_="temp01"):
        print(tag.name)

    print(soup.find_all("div", class_="temp01"))
    '''
    div = soup.find("div", class_="temp01")
    a_tags = div.select("ul > li > a")
    #print(a_tags)

    for tag in a_tags:
        if tag.text.find("：") > 0:
            # print(tag.text.split("：")[0])
            departs.append(tag.text.split("：")[0])

    return

def run():
    print("第1页,无id")
    statistics("http://futures.hexun.com/domestic/index.html")
    for i in range(402,353,-1):
        print("第{0}页,id={1}".format(403-i+1,i))
        statistics("http://futures.hexun.com/domestic/index-{0}.html".format(i))

    result = pd.value_counts(values=departs, sort=True, ascending=False)
    print(result)
    result.to_csv("dep_stat.csv")

    return

def test_encode():
    import chardet
    import urllib
    # 先获取网页内容
    url = "http://futures.hexun.com/domestic/index-371.html"
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    headers = {'User-Agent': user_agent}

    # data1 = urllib.urlopen("http://futures.hexun.com/domestic/index-370.html").read()
    req = request.Request(url, headers=headers)
    data1 = request.urlopen(req).read()

    # 用chardet进行内容分析
    chardit1 = chardet.detect(data1)
    print(chardit1['encoding'])  # baidu

    return

def test_encode2():
    from bs4 import BeautifulSoup

    url = "http://futures.hexun.com/domestic/index-371.html"
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    headers = {'User-Agent': user_agent}

    # data1 = urllib.urlopen("http://futures.hexun.com/domestic/index-370.html").read()
    req = request.Request(url, headers=headers)
    data1 = request.urlopen(req).read()

    soup = BeautifulSoup(data1)
    print(soup.original_encoding)  # 这里的输出就是网页的编码方式

    return

if __name__ == "__main__":
    run()
