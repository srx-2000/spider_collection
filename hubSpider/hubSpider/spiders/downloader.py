import threading
from http import cookiejar
import requests
import json
import os
import parsel
import time

from hubSpider.spiders.ThreadPool import ThreadPool


class xhub():
    login_email = ''
    login_password = ''
    url_list = []
    cookies="wpn_ad_cookie=b3b198eb84dbb54fef98d71de062b333; cit=e7d4ed6dd2da5267ggyAzW0mGbedh9MedmXHrg%3D%3D; undefined=0; hexavid_static=hw; intr-3959997=1; xv_nbview=-1; html5_networkspeed=2468; html5_pref=%7B%22SQ%22%3Afalse%2C%22MUTE%22%3Afalse%2C%22VOLUME%22%3A0.10000000000000014%2C%22FORCENOPICTURE%22%3Afalse%2C%22FORCENOAUTOBUFFER%22%3Afalse%2C%22FORCENATIVEHLS%22%3Afalse%2C%22PLAUTOPLAY%22%3Atrue%2C%22CHROMECAST%22%3Afalse%2C%22EXPANDED%22%3Afalse%2C%22FORCENOLOOP%22%3Afalse%7D; thumbloadstats_vthumbs=%7B%222%22%3A%5B%7B%22s%22%3A2%2C%22d%22%3A501%7D%2C%7B%22s%22%3A2%2C%22d%22%3A2987%7D%2C%7B%22s%22%3A1%2C%22d%22%3A1857%7D%5D%2C%223%22%3A%5B%7B%22s%22%3A1%2C%22d%22%3A642%7D%2C%7B%22s%22%3A2%2C%22d%22%3A1509%7D%2C%7B%22s%22%3A1%2C%22d%22%3A1359%7D%5D%2C%2210%22%3A%5B%7B%22s%22%3A2%2C%22d%22%3A741%7D%2C%7B%22s%22%3A2%2C%22d%22%3A3166%7D%2C%7B%22s%22%3A1%2C%22d%22%3A1474%7D%5D%2C%22last%22%3A%7B%22s%22%3A1%2C%22v%22%3A%5B1857%2C1359%2C1474%5D%7D%7D; hexavid_lastsubscheck=1; chat_deco=1; X-Backend=11|X/suQ|X/qsG; last_views=%5B%2252896695-1608801164%22%2C%2256348837-1608802353%22%2C%2228748735-1609031620%22%2C%2219986471-1609031692%22%2C%2218478139-1609031730%22%2C%2238229833-1609994974%22%2C%2232427813-1609995517%22%2C%2258323997-1610006390%22%2C%2228679013-1610263582%22%2C%2257049173-1610279228%22%2C%224634956-1610283966%22%2C%2219097603-1610283991%22%2C%2219097707-1610284160%22%2C%2248197237-1610284391%22%2C%2225813895-1610296893%22%5D; chat_data_c=; session_token=c1e51e6be07d7967eQcyyscgCEAtKpn44h4ZE7E-KUwj_8EzX4QqQt3FxCi8S9uUQqeh8SN0LAqfz_sQFtiXtUpMDzg73tu5YWdmLqZmSb9m8ZwETz9P8eiYn5ZueDDE0tsQn_s9VsHXqQRCmukK13JGsqrsJK4mLv2_8hPVLvGoQ9SVWB8sCvxLMeJVBnclLHpvLGy5JBngE01emi5KZJTgoGgLZPDlynKwn5pY_DLG3oKyw0YH07uCRV-D3PvU6l1dJCOhXBAGsvjNBi8BH1dylBof-hlxth5FJRT5Ndx4L35weUlp8MFDrGDKicSqlbphEbWTHrAtgh7Vh9iqLJN6rb7n2M8rOgP1qe1s_5cgR_6CBwwXWZafVDvnp9G56Ct76yJNYkJo4xkawqJqcIJjtnKwShxW7qepYvdC7l71ragudQz7hf3uj_woyA04fGi6IW15c-JBll6y"
    headers = {"Accept": "application/json, text/javascript, */*; q=0.01",
               "Connection": "keep-alive",
               "Cookie":cookies,
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
               }
    session = requests.session()

    session.cookies = cookiejar.LWPCookieJar(filename="cookies.txt")

    try:
        session.cookies.load(ignore_discard=True)
    except:
        pass
    def __init__(self,email,password):
        self.login_email=email
        self.login_password=password


    def login_save_cookie(self):
        """
        登录并保存cookie到本地
        :return:
        """
        login_page = "https://www.xvideos.com/account"

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://www.xvideos.com",
            "Referer": "https://www.xvideos.com/account",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "Accept-Language": "zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6",
            "Accept-Encoding": "gzip, deflate, br"
            }

        login_page_response = requests.get(url=login_page, headers=headers)
        token = parsel.Selector(login_page_response.text).xpath("//input[@name='signin-form[csrf_token]']/@value").getall()
        url = 'https://www.xvideos.com/account'
        data = {"signin-form[votes]":"",
                "signin-form[subs]":"",
                "signin-form[post_referer]":login_page,
                "signin-form[csrf_token]":token,
                "signin-form[login]":self.login_email,
                "signin-form[password]":self.login_password}
        # 使用session发起post请求来获取登录后的cookie,cookie已经存在session中
        response = self.session.post(url=url, data=data)
        print(response.text)
        # 把cookie保存到文件中
        self.session.cookies.save()
        print(self.session.cookies)

    def read_cookie(self):
        """
        读取cookie进入登录后的页面
        :return:
        """
        list=[]
        with open(file="cookies.txt",encoding="utf-8") as f:
            for i in f:
                list.append(i.strip("\n"))
        f.close()
        self.cookies=list[-1].split(": ")[-1]
        self.headers["Cookie"]=self.cookies

    def login_y_n(self):
        """
        判断用户是否已经登录，我们这里使用的方法是：随便找一个登陆后页面的url，如果我们访问它时不发生重定向，我们就可以
        判断该用户应经登录了
        :return:
        """
        url = 'https://www.xvideos.com/video-download/57628185'
        response = self.session.get(url = url,allow_redirects=False) # allow_redirects =False不允许重定向到登录页面
        if response != 200:
            return False
        else:
            return True

    def parse_url(self,url):
        id_list=[]
        title_list=[]
        html=requests.get(url=url,headers=self.headers).text
        id_list.extend(parsel.Selector(html).xpath("//div[@id='content']/div[@class='mozaique']/div/@data-id").getall())
        title_list.extend(parsel.Selector(html).xpath("//div[@id='content']/div[@class='mozaique']/div['@class=thumb-under']/div/p/a/text()").getall())
        print("已解析完页面："+url)
        with open(r'../video/video_id.txt', mode="a",encoding='utf-8') as f:
            for i in range(0,len(id_list)):
                f.write(id_list[i]+"-"+title_list[i]+"\n")
                print(id_list[i]+"-"+title_list[i])
        f.close()


    def download(self,id_string):
        url="https://www.xvideos.com/video-download/{video_id}/".format(video_id=id_string.split("-")[0])
        single_response = requests.post(url=url,headers=self.headers)
        json_result=json.loads(single_response.content)
        file_name=id_string.split("-")[1]
        print("开始下载:"+file_name)
        video=requests.get(url=json_result["URL"])
        with open(r'../video/' + file_name+".mp4", mode='wb') as w_f:
            w_f.write(video.content)
            print("保存成功："+file_name)
        w_f.close()

    def parse_all(self,thread_num):
        pool=ThreadPool(thread_num)
        f=open("../video/video_url.txt",mode="r",encoding="utf-8")
        lines=f.readlines()
        total_num=len(lines)
        for i in lines:
            pool.run(func=self.parse_url,args=(i.strip("\n"),))
        pool.close()
        print(total_num)
        if total_num==pool.run_sum_time:
            print("待解析页面个数：："+str(pool.run_sum_time))
        # return True
    def download_all(self,thread_num):
        pool = ThreadPool(thread_num)
        f = open("../video/video_id.txt", mode="r", encoding="utf-8")
        for i in f:
            pool.run(func=self.download, args=(i.strip("\n"),))
            # print(i)
        pool.close()

if __name__ == '__main__':
    email=input("邮箱：")
    password=input("密码：")
    xhub=xhub(email,password)
    # 如果被Google的recaptcha给探测到了，那么这些就都没用了，直接在上面的cookies后面添加登录后的cookies即可
    # f=open("cookies.txt",mode="r")
    # if len(f.readlines()) == 0:
    #     xhub.login_save_cookie()
    # xhub.read_cookie()
    xhub.parse_all(20)
    os.remove("../video/video_url.txt")
    time.sleep(2)
    print("所有页面已经解析完毕，即将进入下载.........")
    time.sleep(3)
    xhub.download_all(20)
