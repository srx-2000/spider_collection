import time

import requests
import parsel
import re
import os
import json
from ThreadPool import ThreadPool


class Downloader(object):

    base_url="https://www.ishuyin.com"
    php_url="https://www.ishuyin.com/e/extend/url.php?code="

    def __init__(self, cl,id):
        self.search_url="https://www.ishuyin.com/{cl}/{id}/0.html".format(cl=cl,id=id)
        self.book_name=""
        self.base_path=""
        self.count=0
        self.chapters = []

    def init(self):
        response = requests.get(url=self.search_url).text
        for chapter in parsel.Selector(response).xpath("//div[@class='bd cl']/section/ul/li/a").extract():
            self.chapters.append( {
            'name':parsel.Selector(chapter).xpath("//a/text()").getall()[0],
            'link':parsel.Selector(chapter).xpath("//a/@href").getall()[0],
            'audio_url':'' }
            )
        #print(self.chapters)
        self.book_name = parsel.Selector(response).xpath("//h1/text()").get()
        self.base_path = os.getcwd() + "\\mp3\\" + self.book_name + "\\"
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

    def parse(self,chapter):
        response_text=requests.get(self.base_url+chapter['link']).text
        data_code = parsel.Selector(response_text).xpath("//div[@class='jp-playlist']/ul/li/@data-code").getall()
        #print(data_code)
        if len(data_code) == 0:
            return
        headers= {
            'referer':self.base_url+chapter['link'],
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
            'accept':'application/json, text/javascript, */*; q=0.01',
            'x-requested-with': 'XMLHttpRequest',
        }
        response_text=requests.get(self.php_url+data_code[0],headers=headers).text
        audio_link = json.loads(response_text)['url']
        #print(audio_link)
        chapter['audio_url'] = audio_link
        #print(self.chapters[count])
        print("开始下载:"+ chapter['name'])
        content=requests.get(url=chapter['audio_url'])
        with open(self.base_path+"\\"+ chapter['name']+".mp3",mode="wb") as f:
            f.write(content.content)
            print(chapter['name']+ " 保存成功！")
        f.close()

    def download_batch(self):
        total = len(self.chapters)
        if  total!= 0:
            pool = ThreadPool(50)
            print(f"开始解析并下载有声书：{total}"+self.book_name)
            for i in range(0,total):
                pool.run(func=self.parse,args=(self.chapters[i],))
            pool.close()
        else:
            print("下载器未数初始化")

if __name__ == '__main__':
    #book=Downloader(38,22977)  #https://www.ishuyin.com/38/22977/0.html
    book=Downloader(38,15626)  #https://www.ishuyin.com/album-38-15626.html
    book.init()
    book.download_batch()
