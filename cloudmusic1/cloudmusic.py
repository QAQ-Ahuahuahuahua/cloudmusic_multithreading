# coding : UFT-8
import requests
import threading
import time
import os
import random
import time
import csv
import re
import pymysql
from bs4 import BeautifulSoup

Base_URL = 'http://music.163.com'

Base_Headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'Host': 'music.163.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'
}

_session = requests.session()

def Turn_Page(pageIndex):
    Page_Url = 'http://music.163.com/discover/playlist/?order=hot&cat=全部&limit=35&offset=' + str(pageIndex * 35)
    rep = _session.get(Page_Url,headers = Base_Headers)
    Get_PlayList(rep.text)

def Get_PlayList(content):
    bs4 = BeautifulSoup(content,"html.parser").body.find_all('a',class_='msk')
    for content in bs4:
        playList = []
        playList_title = content.get('title')
        playList_url = content.get('href')
        playList.append(playList_title)
        playList.append(playList_url)
        print(playList)

class MyThread(threading.Thread):
    def __init__(self, tid, monitor):
        self.tid = tid
        self.monitor = monitor
        threading.Thread.__init__(self)

    def run(self):
        while True:
            monitor['lock'].acquire()  # 调用lock.acquire()   加锁
            if monitor['page'] != 43:
                Turn_Page(monitor['page'])
                monitor['page'] = monitor['page'] + 1  # 增加页面
                print('线程：',self.tid, '下一页:', monitor['page'])  # 还未爬的页面数
                time.sleep(0.5)
            else:
                print("Thread_id", self.tid, " 最后一页")
                end = time.time()
                print("运行时间：", end - start, "s")
                os._exit(0)  # 退出程序
            monitor['lock'].release()  # 释放锁
            time.sleep(0.5)


monitor = {'page': 1, 'lock': threading.Lock()}  # 初始化页面

if __name__ == '__main__':
    start = time.time()
    for k in range(10):
        new_thread = MyThread(k,monitor)  # 创建线程; Python使用threading.Thread对象来代表线程    类BoothThread继承自thread.Threading类
        new_thread.start()  # 调用start()方法启动线程

    end = time.time()
    print("运行时间：", end - start, "s")
