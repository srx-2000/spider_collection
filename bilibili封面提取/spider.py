import requests
import re
import parsel
import json
import os

class cover_extraction:
    bv_av=""
    base_url = "https://www.bilibili.com/video/"

    def __init__(self,BV_AV):
        self.bv_av=BV_AV
        self.base_url=self.base_url+self.bv_av

    def get_title(self,visible):
        title_response = requests.get(self.base_url).text
        title = parsel.Selector(title_response).xpath('//*[@id="viewbox_report"]/h1/span/text()').get()
        if visible:
            print("待提取的视频是：" + title+"【"+self.base_url+"】")
        return str.replace(title,"/","-")

    def spider(self,download):
        title=self.get_title(False)
        response=requests.get(url=self.base_url).text
        url_json=self.__re_method(response)
        json_rsult=json.loads(url_json)
        url_list=json_rsult["thumbnailUrl"]
        if download=="1":
            self.download(url_list,title)
        else:
            print("图片地址如下【请老爷们自取~】：")
            for i in url_list:
                print(i+"\n")

    def download(self,url_list,title):
        dir=os.getcwd()
        for i in range(0,len(url_list)):
            content=requests.get(url_list[i]).content
            with open(dir+"\\"+ title+"("+str(i)+")"+".jpg", mode='wb') as w_f:
                w_f.write(content)
                print("【"+title+"("+str(i)+")"+".jpg"+"】保存成功！")
            w_f.close()

    def __re_method(self,text):
        pattern = re.compile(r'>{.*}<')
        html=pattern.findall(text)[0]
        lt_html=str.replace(html, "<", "")
        rt_html=str.replace(lt_html, ">", "")
        return rt_html


if __name__ == '__main__':
    AV_BV=input("请输入想要提取的BV号或AV号：")
    c=cover_extraction(AV_BV)
    c.get_title(True)
    download=input("是否下载到本地？\n 1.下载本地 \n 2.显示链接\n")
    c.spider(download)