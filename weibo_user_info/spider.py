# import requests
import json
import parsel
import pandas as pd
import re
import time
import random
import os

# from .ThreadPool import ThreadPool
from weibo_user_info.ThreadPool import ThreadPool
from weibo_user_info.ProxyPool import Proxy_pool

# 获取项目根路径
dir = os.getcwd()

proxy_pool = Proxy_pool()


# 工具类
class util(object):
    # 获取代理池
    @staticmethod
    def get_user_agent():
        MY_USER_AGENT = []
        with open(dir + "\\user_agent.txt", encoding="utf-8", mode="r") as f:
            for line in f:
                # print(line.strip('\n'))
                MY_USER_AGENT.append(line.strip('\n'))
        return MY_USER_AGENT

    '''这里区分新旧cookie池的依据是二者的UI设计新旧，weibo.cn看起来就很古老的那种ui，所以这里就称其为旧cookie池了'''

    # 获取weibo.com的cookie池（新cookie池）
    @staticmethod
    def get_new_cookies():
        MY_COOKIES = []
        with open(dir + "\\new_cookies.txt", encoding="utf-8", mode="r") as f:
            for line in f:
                # print(line.strip('\n'))
                MY_COOKIES.append(line.strip('\n'))
        return MY_COOKIES

    # 获取weibo.cn的cookie池（旧cookie池）
    @staticmethod
    def get_old_cookies():
        MY_COOKIES = []
        with open(dir + "\\old_cookies.txt", encoding="utf-8", mode="r") as f:
            for line in f:
                # print(line.strip('\n'))
                MY_COOKIES.append(line.strip('\n'))
        return MY_COOKIES

    # 随机从旧cookie池中选择一个cookie
    @staticmethod
    def get_cookie():
        cookie = {
            'cookie': random.choice(util.get_old_cookies())
        }
        return cookie

    # 随机从新cookie池中选择一个cookie
    @staticmethod
    def get_cookie1():
        cookie1 = {
            'cookie': random.choice(util.get_new_cookies())
        }
        return cookie1

    # 获取请求头
    @staticmethod
    def get_header():
        headers = {
            'User-Agent': random.choice(util.get_user_agent()),
            # 'DOWNLOAD_DELAY': 3,  ## 下载延时
        }
        return headers

    # 字符串转数字
    @staticmethod
    def to_num(string):
        pre = re.compile('\d')
        # for i in content_list:
        text = ''.join(pre.findall(string))
        # print(string)3
        if text == "":
            return 0
        else:
            return int(text)

    # 判断输入的三个数最小的
    @staticmethod
    def min(num1, num2, num3):
        min = num1
        if min > num2:
            min = num2
        if min > num3:
            min = num3
        return min


# 爬虫类
class Spider:
    user_url = ""
    fans_page_url_list = []

    # 对用户地址，以及粉丝数量初始化
    def __init__(self, user_id, num):
        self.user_url = "https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{user_id}&since_id=".format(
            user_id=user_id)
        self.fans_page_url_list = [self.user_url + f"{begin}" for begin in range(num) if begin % 20 == 0]

    # 获取用户的粉丝的id列表
    def get_fans_id(self):
        fans_id_list = []
        print("正在获取粉丝id.....具体完成时间根据要爬取的粉丝数量而定")
        for i in range(len(self.fans_page_url_list)):
            response = proxy_pool.get(url=self.fans_page_url_list[i], headers=util.get_header())
            json_result = json.loads(response.content)
            if "cardlist_head_cards" in json_result["data"]["cardlistInfo"]:
                for i in json_result["data"]["cards"]:
                    if "title" in i:
                        all_fans_list = i["card_group"]
                        for j in all_fans_list:
                            fans_id = j["user"]["id"]
                            fans_id_list.append(fans_id)
            else:
                for i in json_result["data"]["cards"]:
                    all_fans_list = i["card_group"]
                    for j in all_fans_list:
                        fans_id = j["user"]["id"]
                        fans_id_list.append(fans_id)
        print(len(fans_id_list))
        print(fans_id_list)
        with open("id.txt", encoding="utf-8", mode="w") as f:
            for i in fans_id_list:
                f.write(str(i) + "\n")
        f.close()

    # 调用所有具体方法，获取用户所有信息，并将其存储而一个csv文件
    def get_info(self, id):
        user_home_page_url = "https://weibo.cn/u/{id}".format(id=id)
        all_fans_num_list = []
        all_follow_num_list = []
        all_all_blog_num_list = []
        all_like_list = []
        all_comment_list = []
        all_name_list = []
        all_forward_list = []
        all_create_time_list = []
        all_credit_list = []
        all_prove_list = []
        all_member_level_list = []
        all_place_list = []
        all_education_list = []
        all_signature_list = []
        all_constellation_list = []
        print(user_home_page_url)
        time.sleep(4)
        response = proxy_pool.get(url=user_home_page_url, headers=util.get_header(), cookies=util.get_cookie())
        response_text = response.text
        if response_text.__contains__("用户状态异常，暂时无法访问。"):
            all_fans_num_list.append("用户状态异常，暂时无法访问。")
            all_follow_num_list.append("用户状态异常，暂时无法访问。")
            all_all_blog_num_list.append("用户状态异常，暂时无法访问。")
            all_like_list.append("用户状态异常，暂时无法访问。")
            all_comment_list.append("用户状态异常，暂时无法访问。")
            all_name_list.append("用户状态异常，暂时无法访问。")
            all_forward_list.append("用户状态异常，暂时无法访问。")
            all_create_time_list.append("用户状态异常，暂时无法访问。")
            all_credit_list.append("用户状态异常，暂时无法访问。")
            all_prove_list.append("用户状态异常，暂时无法访问。")
            all_member_level_list.append("用户状态异常，暂时无法访问。")
            all_education_list.append("用户状态异常，暂时无法访问。")
            all_place_list.append("用户状态异常，暂时无法访问。")
            all_signature_list.append("用户状态异常，暂时无法访问。")
            all_constellation_list.append("用户状态异常，暂时无法访问。")
        else:
            fans_follow_blog_result = self.get_num(response_text)
            other = self.get_other(id)
            like_comment_num = self.get_blog_atr_num(id)
            all_fans_num_list.append(fans_follow_blog_result[0][0])
            all_follow_num_list.append(fans_follow_blog_result[1][0])
            all_all_blog_num_list.append(fans_follow_blog_result[2][0])
            all_like_list.append(like_comment_num[0])
            all_comment_list.append(like_comment_num[1])
            all_forward_list.append(like_comment_num[0])
            all_name_list.append(fans_follow_blog_result[3])
            all_member_level_list.append(other[0])
            all_create_time_list.append(other[1])
            all_credit_list.append(other[2])
            all_prove_list.append(other[3])
            all_place_list.append(other[4])
            all_education_list.append(other[5])
            all_signature_list.append(other[6])
            all_constellation_list.append(other[7])
        dict = {"关注数": all_follow_num_list, "粉丝数": all_fans_num_list, "vip等级": all_member_level_list,
                "阳光信用": all_credit_list, "点赞数": all_like_list, "评论数": all_comment_list, "转发数": all_forward_list,
                "注册时间": all_create_time_list, "微博总数": all_all_blog_num_list, "用户名称": all_name_list,
                "微博认证": all_prove_list, "位置信息": all_place_list, "教育信息": all_education_list, "个性签名": all_signature_list,
                "生日星座": all_constellation_list}
        df = pd.DataFrame(dict)
        print(dict)
        flag = os.path.exists(dir + "\\微博粉丝信息.csv")
        if not flag:
            df.to_csv("微博粉丝信息.csv", mode="w")
        else:
            df.to_csv("微博粉丝信息.csv", mode="a", header=False)
        return all_follow_num_list, all_fans_num_list, all_member_level_list, all_credit_list, all_like_list, all_comment_list, \
               all_forward_list, all_create_time_list, all_all_blog_num_list, all_name_list, all_prove_list, all_place_list, \
               all_education_list, all_signature_list, all_constellation_list

    # 获取用户所有微博的点赞数，转发数，评论数
    def get_blog_atr_num(self, id):
        comment_num = 0
        like_num = 0
        forward_num = 0
        base_url = "https://weibo.cn/u/" + str(id)
        time.sleep(4)
        response = proxy_pool.get(url=base_url, headers=util.get_header(), cookies=util.get_cookie())
        response_text = response.text
        single_page_comment = parsel.Selector(response_text).xpath(
            "//div[@class='c']/div[last()]/a[@class='cc']/text()").getall()
        single_page_like = parsel.Selector(response_text).xpath("//div[@class='c']/div/a[last()-3]/text()").getall()
        single_page_forward = parsel.Selector(response_text).xpath("//div[@class='c']/div/a[last()-2]/text()").getall()

        for i in range(len(single_page_comment)):
            comment_num += util.to_num(single_page_comment[i])
            like_num += util.to_num(single_page_like[i])
            forward_num += util.to_num(single_page_forward[i])
        all_page_num = parsel.Selector(response_text).xpath("//input[@name='mp']/@value").get()
        print("所有微博页数:" + all_page_num)
        if all_page_num != None:
            if int(all_page_num) >= 20:
                page_url_list = [base_url + f"?page={page}" for page in range(2, 20 + 1)]
                print("由于该用户发的微博数量过多，为了尽可能节省资源与时间，此处仅取前20页进行数据爬取")
            else:
                page_url_list = [base_url + f"?page={page}" for page in range(2, int(all_page_num) + 1)]
            print(page_url_list)
            for i in page_url_list:
                print(i)
                time.sleep(4)
                response = proxy_pool.get(url=i, headers=util.get_header(), cookies=util.get_cookie())
                page_response_text = response.text
                single_page_comment = parsel.Selector(page_response_text).xpath(
                    "//div[@class='c']/div[last()]/a[@class='cc']/text()").getall()
                single_page_like = parsel.Selector(page_response_text).xpath(
                    "//div[@class='c']/div[last()]/a[last()-3]/text()").getall()
                single_page_forward = parsel.Selector(response_text).xpath(
                    "//div[@class='c']/div/a[last()-2]/text()").getall()
                min_len = min(len(single_page_comment), len(single_page_like), len(single_page_forward))
                for i in range(min_len):
                    comment_num += util.to_num(single_page_comment[i])
                    like_num += util.to_num(single_page_like[i])
                    forward_num += util.to_num(single_page_forward[i])
        print(like_num)
        print(comment_num)
        return like_num, comment_num, forward_num

    # 用旧的地址获取用户的基础信息（粉丝数，关注数，微博总数）。其实可以使用微博移动端的接口，获取信息会更方便。
    def get_num(self, response_text):
        try:
            fans_num_list = []
            follow_num_list = []
            all_blog_num_list = []
            all_blog_num = parsel.Selector(response_text).xpath("//div[@class='tip2']/span/text()").get()
            num = parsel.Selector(response_text).xpath("//div[@class='tip2']/a/text()").getall()
            name = parsel.Selector(response_text).xpath("//div[@class='ut']/span[@class='ctt'][1]/text()").get()
            follow_num = num[0]
            fans_num = num[1]
            all_blog_num_list.append(util.to_num(all_blog_num))
            follow_num_list.append(util.to_num(follow_num))
            fans_num_list.append(util.to_num(fans_num))
            print(all_blog_num)
            print(follow_num)
            print(fans_num)
            return fans_num_list, follow_num_list, all_blog_num_list, name
        except IndexError:
            raise Exception("cookie已过期，请及时更换old_cookies和new_cookies中的数据")

    # 获取用户的其余信息（阳光信用，注册时间，会员等级，微博认证，位置，教育，个性签名，星座）
    def get_other(self, id):
        new_info_url = "https://weibo.com/u/{id}".format(id=id)
        old_info_url = "https://weibo.cn/{id}/info".format(id=id)
        time.sleep(4)
        response = proxy_pool.get(url=old_info_url, headers=util.get_header(), cookies=util.get_cookie())
        old_info_response_text = response.text
        time.sleep(4)
        # 这里使用selenium来对抗微博的动态渲染，直接从新的微博网页处获取用户的所有基本信息
        from selenium.webdriver.chrome.options import Options
        from selenium import webdriver
        # 获取用户header中的icon的class 用来判断从用户header中提取到的信息都属于什么种类。
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        # 这行代码非常关键，去掉之后无头模式是无法正确点击icon图标的
        chrome_options.add_argument('--window-size=1920,1080')
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(new_info_url)
        while True:
            try:
                base_class = driver.find_element_by_xpath("//*[@id='app']").get_attribute("class")
                if base_class is not None:
                    time.sleep(1)
                    break
            except:
                pass
        driver.find_element_by_xpath("//i[@class='woo-font woo-font--angleDown']").click()
        time.sleep(1)
        icon_list = driver.find_elements_by_xpath(
            "//div[@class='woo-box-flex woo-box-alignCenter ProfileHeader_icon3_3Ppd6']/i")
        info_list = driver.find_elements_by_xpath("//div[@class='woo-box-item-flex ProfileHeader_con3_Bg19p']")
        middle_info_dict = {}
        for i in range(0, len(icon_list)):
            middle_info_dict[icon_list[i].get_attribute("class")] = re.sub('<[^<]+?>', '', info_list[i].get_attribute(
                "innerHTML")).replace('\n', '').strip()
        member_level = parsel.Selector(old_info_response_text).xpath("//div[@class='c'][2]/text()").get()
        index_list = ["woo-font woo-font--proV",
                      "woo-font woo-font--proBintro",
                      "woo-font woo-font--proIntro",
                      "woo-font woo-font--proPlace",
                      "woo-font woo-font--proEdu",
                      "woo-font woo-font--proTime",
                      "woo-font woo-font--proCredit"]
        for j in index_list:
            if not middle_info_dict.keys().__contains__(j):
                middle_info_dict[j] = "未知"
        create_time = middle_info_dict["woo-font woo-font--proTime"]
        credit = middle_info_dict["woo-font woo-font--proCredit"]
        prove = middle_info_dict["woo-font woo-font--proV"]
        place = middle_info_dict["woo-font woo-font--proPlace"]
        education = middle_info_dict["woo-font woo-font--proEdu"]
        signature = middle_info_dict["woo-font woo-font--proBintro"]
        constellation = middle_info_dict["woo-font woo-font--proIntro"]
        print("微博创建日期：" + create_time)
        print("阳光信誉：" + credit)
        print("微博认证：" + prove)
        print("所在地区：" + place)
        print("教育经历：" + education)
        print("个性签名：" + signature)
        print("生日星座：" + constellation)
        return member_level, create_time, credit, prove, place, education, signature, constellation


if __name__ == '__main__':
    with open(dir + "\\logo.txt", encoding="utf-8", mode="r") as f:
        for i in f:
            print(i.strip("\n"))
    print("~" * 50 + "该爬虫仅用于交流学习，如果需要大量快速爬取请自行加入减少time.sleep时间" + "~" * 50)
    print("~" * 31 + "如果想要爬取多个人的信息，只需在目录中的id.txt填入id列表（一行一个）然后选择第三个模式即可开始爬取" + "~" * 31)
    a = input("请输入1或2或3选择要进行步骤：\n1.爬取输入用户信息\n2.爬取粉丝id\n3.爬取粉丝（多人）信息\n")
    if a == "1":
        user_id = input("请输入用户的id：")
        spider = Spider(int(user_id), 0)
        spider.get_info(int(user_id))
    elif a == "2":
        user_id = input("请输入用户的id：")
        fans_num = input("请输入想要获取的粉丝信息的数量：")
        spider = Spider(int(user_id), int(fans_num))
        spider.get_fans_id()
    elif a == "3":
        spider = Spider(0, 0)
        id_list = []
        try:
            with open(dir + "\\id.txt", encoding="utf-8", mode="r") as f:
                for line in f:
                    id_list.append(line.strip('\n'))
            f.close()
            pool = ThreadPool(20)
            for i in range(0, len(id_list)):
                pool.run(func=spider.get_info, args=(id_list[i],))
            pool.close()
        except:
            print("未找到id.txt文件，请先提供id列表，或选择2模式获取id列表")
    else:
        print("请输入1或2或3")
