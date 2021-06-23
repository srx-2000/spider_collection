# ！/usr/bin/env python
# -*-coding:utf-8-*-
import os
import you_get
import threading

from bilibiliSP.spiders.ThreadPool import ThreadPool

url_list=[]

def read_file():
    with open(r'..\..\bilbili_Output.txt', encoding='utf-8') as f:
        for line in f:
            # print(line)
            url_list.append(line.strip('\n'))

def download(url):
    os.system(r"you-get -o D:/sp "+url)
    you_get.main()
    # pass

def downloadAll(thread_num):
    pool = ThreadPool(thread_num)
    for i in url_list:
        # print(i)
        pool.run(func=download, args=(i,))
    pool.close()
if __name__ == '__main__':
    read_file()
    downloadAll(10)