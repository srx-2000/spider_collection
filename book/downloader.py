import time

import requests
import parsel
import re
import os

from ThreadPool import ThreadPool


class Downloader(object):

    base_url="https://www.ishuyin.com/"

    def __init__(self, id):
        self.search_url="https://www.ishuyin.com/show-{id}.html".format(id=id)
        self.mp3_url_list=[]
        self.chapter_list=[]
        self.book_name=""
        self.base_path=""
        self.count=0
        self.dict={}

    def init(self):
        response = requests.get(url=self.search_url).text
        self.chapter_list = parsel.Selector(response).xpath("//div[@class='box' and position()<3]/a/@href").getall()
        self.book_name = parsel.Selector(response).xpath("//h1/text()").get()
        self.base_path = os.getcwd() + "\\mp3\\" + self.book_name + "\\"
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

    def parse(self,i,count):
        response_text=requests.get(self.base_url+i).text
        unicode=re.search(r'(\*\d+)*\*',response_text).group()
        unicode_list=unicode.split("*")
        mp3_url=""
        for j in range(1, len(unicode_list)-1):
            mp3_url+=chr(int(unicode_list[j]))
        print("已成功解析："+mp3_url)
        self.dict[count]=mp3_url
        if count == (len(self.chapter_list)-1):
            return True
        else:
            return False

    def download(self,i,count):
        print("开始下载:"+self.book_name+"第"+str(count+1)+"章")
        content=requests.get(url=i)
        with open(self.base_path+"\\"+str(count+1)+".mp3",mode="wb") as f:
            f.write(content.content)
            print(self.book_name+"第"+str(count+1)+"章保存成功！")
        f.close()


    def parse_all(self):
        if len(self.chapter_list) != 0:
            pool = ThreadPool(100)
            print("开始解析并下载有声书："+self.book_name)
            for i in range(0,len(self.chapter_list)):
                # print(self.chapter_list[i])
                pool.run(func=self.parse,args=(self.chapter_list[i],i,),callback=self.callback)
            pool.close()

        else:
            print("下载器未数初始化")

    def callback(self,status,pool,num,result):
        self.count+=1
        if self.count== len(self.chapter_list):
            for i in sorted(self.dict):
                self.mp3_url_list.append(self.dict[i])
            with open(self.base_path + "\\" + "mp3_url.txt", mode="w") as f:
                for i in self.mp3_url_list:
                    f.write(i + "\n")
                f.close()

    def download_batch(self):
        if not os.path.exists(self.base_path+"\\"+"mp3_url.txt"):
            self.parse_all()
        else:
            with open(self.base_path+"\\"+"mp3_url.txt",mode="r") as f:
                for line in f:
                    self.mp3_url_list.append(line.strip('\n'))
        pool = ThreadPool(50)
        for i in self.mp3_url_list:
            pool.run(func=self.download,args=(i,self.mp3_url_list.index(i)))
        pool.close()

if __name__ == '__main__':
    book=Downloader(23736)
    book.init()
    book.download_batch()



