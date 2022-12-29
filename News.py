# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 23:33:34 2022

@author: Robin
"""

import requests

from bs4 import BeautifulSoup

import db

from pymysql.converters import escape_string

url = "https://news.cts.com.tw/entertain/index.html"

# 爬蟲網址

data = requests.get(url) 
# 抓取資料下來為串流，它的型態為串流 stream byte
data.encoding = "utf8"
# 將資料編碼設定為:utf8
data = data.text
#抓取網路上的資料後轉換為文字

soup = BeautifulSoup(data,'html.parser')
# BeautifulSoup 解析HTML語法
news = soup.find('div',class_='newslist-container flexbox')
newsItems = news.find_all('a')
cursor = db.conn.cursor()

for row in newsItems:
    link = row.get('href')
    title = row.get('title')
    photo = row.find('img').get('data-src')
    postdate = row.find('span').text
    
    title = escape_string(title)
    #特殊符號進行轉譯
    
    #先查詢標題是否有重複的
    sql = "select * from news where title='{}'".format(title)
    cursor.execute(sql)
    db.conn.commit()
    
    if cursor.rowcount == 0:
        #查詢的比數為多少
        sql = "insert into news(title,link,photo,modate) values('{}','{}','{}','{}')".format(title,link,photo,postdate)
        
        cursor.execute(sql)
        db.conn.commit()
        
db.conn.close()
    # print(link)
    # print(title)
    # print(photo)
    # print(postdate)


