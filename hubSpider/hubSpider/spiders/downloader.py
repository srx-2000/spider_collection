import requests
import json
import parsel
import time
import os
from hubSpider.spiders.ThreadPool import ThreadPool


class xhub():
    parse_count=0
    url_list = []
    cookies="html5_pref=%7B%22SQ%22%3Afalse%2C%22MUTE%22%3Afalse%2C%22VOLUME%22%3A0.14814814814814814%2C%22FORCENOPICTURE%22%3Afalse%2C%22FORCENOAUTOBUFFER%22%3Afalse%2C%22FORCENATIVEHLS%22%3Afalse%2C%22PLAUTOPLAY%22%3Atrue%2C%22CHROMECAST%22%3Afalse%2C%22EXPANDED%22%3Afalse%2C%22FORCENOLOOP%22%3Afalse%7D; wpn_ad_cookie=844f777cc0605f3817f54d75af61201d; html5_networkspeed=1898; session_ath=light; last_views=%5B%2253852345-1620103005%22%2C%2248308125-1620103030%22%2C%2250198419-1620103048%22%2C%2250195611-1620104267%22%2C%2249103779-1620104271%22%2C%2262344381-1621327559%22%2C%2262320519-1622283383%22%2C%2263312887-1622888247%22%2C%2227495597-1623578627%22%2C%2221738443-1623578645%22%2C%2234615431-1623578681%22%2C%2213596507-1623578812%22%2C%227803869-1623743475%22%2C%2260235255-1626420331%22%2C%2225006697-1626659785%22%2C%2223093369-1626659874%22%2C%2223093373-1626659917%22%2C%2223092473-1626660258%22%2C%2223093435-1626660443%22%2C%223554254-1626743341%22%2C%2258324077-1626918228%22%2C%229008195-1626918243%22%2C%228233984-1627120116%22%2C%2255229829-1628060293%22%2C%2213247727-1628738890%22%2C%2222837435-1628738906%22%2C%221911474-1628738976%22%2C%229242034-1628739051%22%2C%2211154523-1628739122%22%2C%2215071445-1628739178%22%2C%2220509683-1628739177%22%2C%22261140-1628739397%22%2C%2222575635-1628739403%22%2C%2258709721-1628739406%22%2C%2233517373-1628739472%22%2C%22259434-1628739568%22%2C%22260465-1628739710%22%2C%2230081125-1628739779%22%2C%22260469-1628739780%22%2C%2225127631-1628740446%22%2C%2227707541-1628740465%22%2C%2210820539-1628740480%22%2C%229473165-1628740513%22%2C%2210820479-1628740689%22%2C%2262205689-1629000254%22%5D; session_token=1b9bd7cf559a478fQJsUNtH6oScs17pyecyYSEI6Ju8nF0ouIgdJNfC0C2a34Osm3IUzD8rjTFOkKvVYK-q3OU9Evbr958auaO9z0Jtd5-0WULzOcEP7sYNhmtv9SsfZ4uvBl2q52jPB4MbU7Cos9v0f4bI68xkZMP8SNxXUuFX9Coqh9NWx3mSK7jUeRO6CC2CcOYOi-rxAVNSOCGrJq6243cUes4_HXUCsRSQ-K7RBwXGvUa90N-JGHsfeber7LMew9BN2EnLoAWqdjHbX5I-8BAZ0_SBjmCJoCS9TwN_oABTGsYjRmLg0RGfBgDXRHhO5OPlTAunOYIzLa5BEwzkXQYGLzGgkhu-IF5HwMG0gAXXJG-fovy8r7wBY6MgpCPIJGDfMAzABmCsLtufTaBaEoyo8DoohuYL7QY_lSwxuJ2toXxNojF5_2Fq1U0Gn3eIe9Sn5JCXyUZvUonK7EqXBXoatLnfDTfQeQQ%3D%3D; pending_thumb=%7B%22t%22%3A%5B%5D%2C%22s%22%3A%5B%5D%2C%22p%22%3A%5B%5D%2C%22r%22%3A%5B%5D%7D"
    headers = {
               "Cookie":cookies,
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
               }
    # def login_save_cookie(self):
    #     """
    #     登录并保存cookie到本地
    #     :return:
    #     """
    #     login_page = "https://www.xvideos.com/account"
    #
    #     headers = {
    #         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    #         "Connection": "keep-alive",
    #         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
    #         "Content-Type": "application/x-www-form-urlencoded",
    #         "Origin": "https://www.xvideos.com",
    #         "Referer": "https://www.xvideos.com/account",
    #         "Sec-Fetch-Dest": "document",
    #         "Sec-Fetch-Mode": "navigate",
    #         "Sec-Fetch-Site": "same-origin",
    #         "Sec-Fetch-User": "?1",
    #         "Upgrade-Insecure-Requests": "1",
    #         "Accept-Language": "zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6",
    #         "Accept-Encoding": "gzip, deflate, br"
    #         }
    #
    #     login_page_response = requests.get(url=login_page, headers=headers)
    #     token = parsel.Selector(login_page_response.text).xpath("//input[@name='signin-form[csrf_token]']/@value").getall()
    #     url = 'https://www.xvideos.com/account'
    #     data = {"signin-form[votes]":"",
    #             "signin-form[subs]":"",
    #             "signin-form[post_referer]":login_page,
    #             "signin-form[csrf_token]":token,
    #             "signin-form[login]":self.login_email,
    #             "signin-form[password]":self.login_password}
    #     # 使用session发起post请求来获取登录后的cookie,cookie已经存在session中
    #     response = self.session.post(url=url, data=data)
    #     # 把cookie保存到文件中
    #     self.session.cookies.save()
    #     print(self.session.cookies)

    # def read_cookie(self):
    #     """
    #     读取cookie进入登录后的页面
    #     :return:
    #     """
    #     list=[]
    #     with open(file="cookies.txt",encoding="utf-8") as f:
    #         for i in f:
    #             list.append(i.strip("\n"))
    #     f.close()
    #     self.cookies=list[-1].split(": ")[-1]
    #     self.headers["Cookie"]=self.cookies

    def login_y_n(self):
        """
        判断用户是否已经登录，我们这里使用的方法是：找一个视频id，然后尝试下载这个视频，如果返回的结果是可以下载，那么就是登录了
        :return:
        """
        home_url="https://www.xvideos.com/"
        response_text=requests.get(url=home_url).text
        id=parsel.Selector(response_text).xpath("//div/@data-id").get()
        print("测试视频id【用于测试是否登录成功】："+id)
        url = 'https://www.xvideos.com/video-download/'+id
        response = requests.get(url = url,headers=self.headers,allow_redirects=False) # allow_redirects =False不允许重定向到登录页面
        if not response.text.__contains__("true"):
            return False
        else:
            print("登录成功！")
            return True

    def parse_url(self,url):
        id_list=[]
        title_list=[]
        html=requests.get(url=url,headers=self.headers).text
        id_list.extend(parsel.Selector(html).xpath("//div/@data-id").getall())
        title_list.extend(parsel.Selector(html).xpath("//div/p/a/@title").getall())
        print("已解析完页面："+url)
        self.parse_count+=1
        with open("../video/video_id.txt", mode="w",encoding='utf-8') as f:
            for i in range(0,len(id_list)):
                f.write(id_list[i]+"-"+title_list[i]+"\n")
                # print(id_list[i]+"-"+title_list[i])
        f.close()

    def download(self,id_string):
        url="https://www.xvideos.com/video-download/{video_id}/".format(video_id=id_string.split("-")[0])
        single_response = requests.get(url=url,headers=self.headers)
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
        if total_num==pool.run_sum_time:
            print("待解析页面个数："+str(pool.run_sum_time))
        return total_num
        # return True

    def download_all(self,thread_num):
        pool = ThreadPool(thread_num)
        f = open("../video/video_id.txt", mode="r", encoding="utf-8")
        for i in f:
            pool.run(func=self.download, args=(i.strip("\n"),))
            # print(i)
        pool.close()

if __name__ == '__main__':
    xhub=xhub()
    f_r = open("../video/video_id.txt",mode="r",encoding="utf-8")
    f_len =len(f_r.readline())
    f_r.close()
    if f_len == 0:
        total_num=xhub.parse_all(20)
        print("."*30+"正在请求解析"+"."*30)
        while True:
            if total_num==xhub.parse_count:
                break
            else:
                time.sleep(1)
    if xhub.login_y_n():
        xhub.download_all(20)
    else:
        print("登录失败，请自己准备cookie并填在10行处")


