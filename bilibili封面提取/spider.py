import requests
import re
import parsel
import json
import os
import yaml
from bilibili封面提取 import ThreadPool

class cover_extraction:
    bv_av=""
    base_url = "https://www.bilibili.com/video/"
    batch_url="https://api.bilibili.com/x/web-interface/search/all/v2?page={page}&keyword={keyword}"
    key_word=""
    download_path=""
    thead_num=20

    def __init__(self,BV_AV):
        config=open(os.getcwd()+"\\config.yaml",mode="r",encoding="utf-8")
        cfg=config.read()
        yaml_line=yaml.load(stream=cfg,Loader=yaml.FullLoader)
        self.download_path=yaml_line["download_path"]
        self.thead_num=yaml_line["Thread_num"]
        self.bv_av=BV_AV
        self.base_url=self.base_url+self.bv_av

    def get_title(self,visible):
        title_response = requests.get(self.base_url).text
        title = parsel.Selector(title_response).xpath('//*[@id="viewbox_report"]/h1/span/text()').get()
        if visible:
            print("待提取的视频是：" + title+"【"+self.base_url+"】")
        return title

    def single_spider(self,download):
        title=self.get_title(False)
        response=requests.get(url=self.base_url).text
        url_json=self.__re_method(response)
        json_rsult=json.loads(url_json)
        url=json_rsult["thumbnailUrl"][0]
        if download=="1":
            self.download(url,title,self.bv_av)
        else:
            print("图片地址如下【请老爷们自取~】：")
            print(url+"\n")

    def download(self,url,title,bv_av):
        print("正在下载："+self.__word_list(title)+"___"+bv_av)
        content=requests.get(url).content
        with open(self.download_path+"\\" + self.__word_list(title)+"___"+bv_av + ".jpg", mode='wb') as w_f:
            w_f.write(content)
            print("【"+title+".jpg"+"】保存成功！")
        w_f.close()

    def __word_list(self,title):
        word_dict={}
        with open(os.getcwd()+"\\"+"word_list.txt", mode="r",encoding="utf-8") as r_f:
            for i in r_f:
                line=i.split("\n")[0]
                word_dict[line.split(" ")[0]]=line.split(" ")[1]
        r_f.close()
        for key,value in word_dict.items():
            if title.__contains__(key):
                title=str.replace(title,key,value)
        return title

    def __re_method(self,text):
        pattern = re.compile(r'>{.*}<')
        html=pattern.findall(text)[0]
        lt_html=str.replace(html, "<", "")
        rt_html=str.replace(lt_html, ">", "")
        return rt_html

    def batch_search(self,key_word):
        self.key_word=key_word
        base_url=self.batch_url.format(page=1,keyword=self.key_word)
        json_dict=json.loads(requests.get(base_url).text)
        result_num=json_dict["data"]["numResults"]
        num_ages=json_dict["data"]["numPages"]
        print("共获取到结果"+str(result_num)+"----经统计共"+str(num_ages)+"页")

    def batch_download(self,before_page):
        pic_dict={}
        print("正在获取前"+str(before_page)+"页信息")
        page_url_list=[self.batch_url.format(page=str(page),keyword=self.key_word) for page in range(1,before_page+1)]
        for i in page_url_list:
            json_dict=json.loads(requests.get(i).text)
            data_list=json_dict["data"]["result"][-1]["data"]
            for j in data_list:
                pic_dict[self.__re_sub(j["title"])+"-"+j["bvid"]]="https:"+j["pic"]
        pool=ThreadPool.ThreadPool(20)
        for key,value in pic_dict.items():
            pool.run(func=self.download,args=(value,key.split("-")[0],key.split("-")[1]))
        pool.close()

    def __re_sub(self,str1):
        re1='<em class=\"keyword\">'
        re2='</em>'
        title1=str.replace(str1,re1,"")
        title2=str.replace(title1,re2,"")
        return title2

if __name__ == '__main__':
    mode=input("请输入想要爬取的方式：\n 1.根据关键字批量爬取 \n 2.根据给出的BV好单个爬取 \n")
    if mode=="1":
        key_word=input("请输入关键字：")
        c=cover_extraction("")
        c.batch_search(key_word)
        page=input("请输入想要获取前多少页的封面：")
        c.batch_download(int(page))
    elif mode=="2":
        AV_BV=input("请输入想要提取的BV号或AV号：")
        c=cover_extraction(AV_BV)
        c.get_title(True)
        download=input("是否下载到本地？\n 1.下载本地 \n 2.显示链接\n")
        c.single_spider(download)
