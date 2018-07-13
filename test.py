# coding=utf-8  
# 搜狗微信专用
import requests
from bs4 import BeautifulSoup
import time
import pymysql
from pyquery import PyQuery as pq
from selenium import webdriver
import re

# 获取html文档 i 页数
def get_html(i):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Host': 'weixin.sogou.com',
        'Cookie':'SUID=1014F0B73220910A0000000058953131; SUV=00BA7A57B7F0141058A2777CEB32C842; usid=hO4Qk4dUo3_-fzjq; IPLOC=CN4401; SNUID=F94299CFB3B1D955FDA06BEDB4288752; ABTEST=8|1528189335|v1; weixinIndexVisited=1; ppinf=5|1528189402|1529399002|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTo0NTolRTYlODklOTMlRTklODUlQjElRTYlQjIlQjklRTglODAlOEMlRTUlQjclQjJ8Y3J0OjEwOjE1MjgxODk0MDJ8cmVmbmljazo0NTolRTYlODklOTMlRTklODUlQjElRTYlQjIlQjklRTglODAlOEMlRTUlQjclQjJ8dXNlcmlkOjQ0Om85dDJsdURBckNUcmVNRGFBeHJIS045QXVLSTBAd2VpeGluLnNvaHUuY29tfA; pprdig=fNdH47QdMS9mHevgIj8U61SDJZdGXu_E0yWGNlgEdcTF3Wn76UbxIevs8V8WD4K97o9gy7F-AthAixwicCjVOMo5N0pJWD6nQlG7eoYWBq36l-MbSWqGidtPKon2QcgJ6avWdMSa3VBY9olBn2oabtv0kkNat-yioQQ6RjufzPQ; sgid=22-35360397-AVsWUdqLTnuK0xsERfYERoc; ppmdig=1528189403000000501c62164c753a033b138fbba5f10ec4; JSESSIONID=aaa-PcUHE05c47GUhVknw',
        'Referer': 'http://weixin.sogou.com/weixin?query=%E9%BA%A6%E5%8D%A2%E5%8D%A1&_sug_type_=&s_from=input&_sug_=y&type=2&page=14&ie=utf8',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4620.400 QQBrowser/9.7.13014.400'
    }
    response = requests.get("http://weixin.sogou.com/weixin?query=%E9%BA%A6%E5%8D%A2%E5%8D%A1&_sug_type_=&s_from=input&_sug_=n&type=2&page=" + i + "&ie=utf8",headers=headers)
    response.encoding = 'utf-8'
    return response.text


# 获取页面url
def get_certain_joke(html,num):
    """get the joke of the html"""
    soup = BeautifulSoup(html, 'html.parser')
    tds = soup.find_all('div', class_="txt-box")

    for td in tds:
        zzr = td.find_all('a')
        content = parse_wx_articles_by_html(zzr[0]["href"])
        insert_table(parse_content_html(content),parse_title_html(content),zzr[0]["href"],num)

# 循环搜狗微信链接
def get_while_html(i, start):
    num = start
    while num <= i:
        print('-----------正在抓取第' + str(num) + '页--------------')
        content = get_html(str(num))
        get_certain_joke(content,num)
        print('-----------第' + str(num) + '页抓取完成--------------')
        num = num + 1


# 获取公众号文章内容
def parse_wx_articles_by_html(selenium_html):
    # 渲染js，微信部分内容是由js生成
    browser = webdriver.PhantomJS(executable_path=r'E:\phantomjs.exe')
    browser.get(selenium_html)
    time.sleep(3)
    html = browser.execute_script("return document.documentElement.outerHTML")
    browser.close()
    return html

# 获取文章内容
def parse_content_html(html):
    return pq(html)('#js_content')

# 获取文章标题
def parse_title_html(html):
    return pq(html)('#activity-name')

def connect_db():
    host = "192.168.1.1"
    name = "python"
    user = "mmcp"
    password = "admin"
    db = pymysql.connect(host, user, password, name, charset='utf8')
    return db

def insert_table(content,title, url ,page):
    sql = "INSERT INTO wc_article(title,content,url,page)VALUES(%s,%s,%s,%s)"
    db_insert = connect_db()
    cursor_insert = db_insert.cursor()
    n = re.sub('<script[\s\S]*</script>', '', str(title))
    y = re.sub('<h2[^>]*>', '', n)
    x = re.sub('</h2>', '', y)
    cursor_insert.execute(sql, (x.replace(" ","").replace("\n",""), str(content).replace('display:none', 'display:block')
                                .replace('data-src', 'src'), str(url), page))
    db_insert.commit()
    db_insert.close()


get_while_html(40,31)
