from http import cookiejar
import requests
import json
import os
import parsel


class xhub():
    login_email = ''
    login_password = ''
    url_list = []
    cookies=""
    headers = {"Accept": "application/json, text/javascript, */*; q=0.01",
               "Connection": "keep-alive",
               "Cookie": cookies,
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
                "signin-form[post_referer]":"https://www.xvideos.com/account",
                "signin-form[csrf_token]":token,
                "signin-form[login]":self.login_email,
                "signin-form[password]":self.login_password}
        # 使用session发起post请求来获取登录后的cookie,cookie已经存在session中
        response = self.session.post(url=url, data=data)
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

    def parse_url(self):
        id_list=[]
        title_list=[]
        with open(r'../video/video_url.txt', encoding='utf-8') as f:
            for i in f:
                self.url_list.append(i.strip("\n"))
        f.close()
        for i in self.url_list:
            html=requests.get(url=i,headers=self.headers).text
            id_list.extend(parsel.Selector(html).xpath("//div[@id='content']/div[@class='mozaique']/div/@data-id").getall())
            title_list.extend(parsel.Selector(html).xpath("//div[@id='content']/div[@class='mozaique']/div['@class=thumb-under']/div/p/a/text()").getall())
            print("已解析完页面："+i)
        with open(r'../video/video_id.txt', mode="w",encoding='utf-8') as f:
            for i in range(0,len(id_list)):
                f.write(id_list[i]+"-"+title_list[i]+"\n")
                print(id_list[i]+"-"+title_list[i])
        f.close()
        os.remove("../video/video_url.txt")



    def download(self):
        with open(r'../video/video_id.txt',encoding='utf-8') as f:
            for i in f:
                url="https://www.xvideos.com/video-download/{video_id}/".format(video_id=i.strip("\n").split("-")[0])
                single_response = requests.post(url=url,data=self.data,headers=self.headers)
                json_result=json.loads(single_response.content)
                file_name=i.strip("\n").split("-")[1]
                print("开始下载:"+file_name)
                video=requests.get(url=json_result["URL"])
                with open(r'../video/' + file_name+".mp4", mode='wb') as f:
                    f.write(video.content)
                    print("保存成功："+file_name)

if __name__ == '__main__':
    email=input("邮箱：")
    password=input("密码：")
    xhub=xhub(email,password)
    xhub.login_save_cookie()
    xhub.read_cookie()
    xhub.parse_url()
    xhub.download()
    os.remove("../video/video_id.txt")
    print("*"*50+"全部下载完毕了！"+"*"*50)