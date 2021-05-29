import requests
import parsel
import pandas as pd


class wh_housing_crawler:
    def get_crawler_infomation(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }
        cookie = {
            'cookie': "aQQ_ajkguid=FF462255-2FF1-C6BF-3906-DDEEBF767C20; id58=e87rkF/8ZJpnP8sbCbc+Ag==; _ga=GA1.2.549045430.1610376346; 58tj_uuid=59c2003e-db6c-4e78-a620-e34a0c278e53; als=0; ctid=22; cmctid=158; wmda_new_uuid=1; wmda_uuid=0d98fab728ee4813c9e00dbe1ac9b7e3; wmda_visited_projects=%3B6289197098934; lps=https%3A%2F%2Fwh.zu.anjuke.com%2Ffangyuan%2Fjiangxiat%2F%3Fpi%3Dbaidu-cpchz-wh-qybk2%26kwid%3D80374578249%7Chttps%3A%2F%2Fwww.baidu.com%2Fbaidu.php%3Fsc.a00000KEJeCxDFezEWFQDN6NutZpjfypcYH82cu5GOB0spYD_wzixT3Cxm4bPxQAFRpn-fUgIpfG_--PfQYqFGNTOFjNC4tQeSeg1Kh6wxKtGFlnVW72R-BAI0ipgkBHgiKl78eoQ-ZjwiYDe_g-QQLITAFLhfaNhk1YYQGmaj-SQoBxssYDLVb2aJDEATwPp5n-y6P1TB2SiyKe-WyKNeZ_7yOT.7R_NR2Ar5Od6632EQ9sXHnygKvGwKou1pnjnRANerUCX1f6e3L_g_3_AXZZjNs4Sao5eP7OUblqEKBmvyTxZ_LXr1FvUd2s1f_U85WkL20.U1Y10ZDq18il8ovV1tHg3oXOdqrv3nMuklei8eWvdnc0TA-W5HD0TZPGuv3qPANWnhnsuH-BnjIBn1wWmhf3PvPbPAfYnW0duARLrjD0IjLr4QJlEpL5kPxBVet0pyYqnWcd0ATqTZnz0ZNG5yF9pywd0ZKGujYk0APGujY1rHD0UgfqnH0krNtknjDLg1csPWFxrHDsP7t1PW0k0AVG5H00TMfqrHDz0AFG5HDdPNtkPH9xnW0Yg1ckPsKVm1Yknj0kg1D3P1c1nHRsPjIxnNtkPHuxn0KkTA-b5HDv0Z7Wpyfqn1Tk0ZFMIA7M5HD0mycqn7ts0ANzu1Ys0ZKs5HbdPWnkPjRknfK8IM0qna3snj0snj0sn0KVIZ0qn0KbuAqs5H00ThCqn0KbugmqTAn0uMfqn0KspjYs0Aq15H00mMTqnH00UMfqn0K1XWY0mgPxpywW5gK1QyFbuZ60pywW5R9affKYmgFMugfqn17xn1Dkg160IZN15HD3nWfzPjf4nWckPjTYnjfznj6Y0ZF-TgfqnHmknH0dPWmkn1bLr0K1pyfqmvn1PyubPH0snj0sn1nsnfKWTvYqfYN7PHm4wW0vwj6znYDdrfK9m1Yk0ZK85H00TydY5H00Tyd15H00XMfqn0KVmdqhThqV5HKxn7tsg1Kxn0Kbmy4dmhNxTAk9Uh-bT1Ysg1Kxn7tsg100TA7Ygvu_myTqn0Kbmv-b5HDsP1nLPjD3nWf0ugwGujYVnfK9TLKWm1Ys0ZNspy4Wm1Ys0Z7VuWYs0AuWIgfqn0KGTvP_5H00XMK_Ignqn0K9uAu_myTqnfK_uhnqn0KbmvPb5fKYTh7buHYdrH0znHf0mhwGujYvfbRdfWFanYDkrj04PY7DwW0LrDfsnHIanjR1fRcYn0KBIjYs0Aq9IZTqn0KEIjYs0AqzTZfqnanscznsc10WnansQW0snj0snanscznsczYWna3snj0snj0Wni3snj0snj00TNqv5H08rjIxna3sn7tsQW0sg108nW-xna3zn-tsQWnY0AF1gLKzUvwGujYs0APzm1YYPWDzns%26word%3D%26ck%3D7083.11.217.341.367.374.154.553%26shh%3Dwww.baidu.com%26sht%3Dbaidu%26us%3D1.0.1.0.2.762.0%26wd%3D%26bc%3D110101; wmda_session_id_6289197098934=1611056620435-980e79a9-9585-6f13; sessid=C9C889BE-C839-E049-0014-C7EE95F16367; twe=2; init_refer=https%253A%252F%252Fwww.baidu.com%252Flink%253Furl%253DV3XjRzifgSVzhRmUVntzChfF0wS74ot15t2nvNxLn-lDKXL9aZatt_rRIQhbZyCR214AcnES9dskz70CYF3Cta%2526wd%253D%2526eqid%253Dad8d2a580000ba21000000036006c6f1; new_uv=4; new_session=0; ajk_member_verify=3H6KccZh0z%2B4hRPYm7sL%2BjZ2yEWLuIZNWfk0vSfchLg%3D; ajk_member_verify2=MjExMTQ1ODExfEtSY0VqR0d8MQ%3D%3D; __xsptplusUT_8=1; _gid=GA1.2.1187123473.1611058329; _gat=1; __xsptplus8=8.1.1611056888.1611058350.12%232%7Cwww.baidu.com%7C%7C%7C%7C%23%23JHNcBDsgwotEvfYPwiizqkOB2S1TqVo2%23; xzfzqtoken=wop1wEZHqQXmexxfbieiZXDx9WsJANKztN5K6c836ErKUn3lwqVSV%2F1SYU3Oi9TAin35brBb%2F%2FeSODvMgkQULA%3D%3D; ajkAuthTicket=TT=c2935eb841bf224288206e676d482d6b&TS=1611058359542&PBODY=iSLnTdBpNWWveJZqZ21KIx9ZcM0zd9zBH6KEr0RU0jS7ovrND9KrdBf45Lm-qj6zYCdwoRShiqGbBRIAVkpAVz-difT9dqB7PQfyfjL_ECg1msueQhMQ-npqJ1ZsZwt9w-Glo0dmeErrgFdH1qPSmiubecHHA908ks9sqIEdO4A&VER=2; obtain_by=1; xxzl_cid=92c48cfa13664d818cf67864db3ccd81; xzuid=7a4085ab-9277-4eba-99f5-c374feaf96cf"
        }
        resp = requests.get(url=url, cookies=cookie, headers=headers)

        '''这里我暂时使用parsel来解析html了，并会对增加的代码进行一定的注释'''
        # 获取文本形式的html
        resp_text=resp.text
        # 这里使用xpath对html进行筛选，xpath具体语法可以参见：https://www.w3school.com.cn/xpath/index.asp

        # 获取房屋连接的列表
        zoom_link_list=parsel.Selector(resp_text).xpath("//div[@class='zu-info']/h3/a/@href").getall()
        # 获取房屋描述列表
        zoom_describe_list=parsel.Selector(resp_text).xpath("//div[@class='zu-info']/h3/a/b/text()").getall()
        # 获取房屋地址列表
        '''首先获取写有地址的节点，因为这个节点的文本数据被分别放到了a和address两个不同的标签中，所以这里要与上面的直接取文本稍有不同，是没有使用getall()函数获取数据的，
        而是使其继续保持为一个选择题的状态，这样返回的就是一个选择器列表，其中的每个选择器里面放的都是一个房屋的地址节点'''
        zoom_address_selector=parsel.Selector(resp_text).xpath("//div[@class='zu-info']/address")
        '''定义一个空列表用于接收最终数据'''
        zoom_address_list=[]
        '''遍历选择器列表'''
        for i in zoom_address_selector:
            '''这里继续使用xpath函数对遍历到的选择器进行进一步筛选，筛选所使用的函数是string()这个函数的作用是  获取该节点以及其子节点下所有的文本。  所以这样a标签和
            address标签中的文本都取下来了，然后使用get()函数挨个进行数据清洗，去掉多余的空格'''
            address=i.xpath("string(.)").get().strip().replace(" ", "").replace("\n","")
            '''加入到空列表中'''
            zoom_address_list.append(address)
        # 获取房屋价格列表
        zoom_price_list=parsel.Selector(resp_text).xpath("//div[@class='zu-side']/p/strong/b/text()").getall()
        # 获取房屋详情列表
        '''处理方法与上面地址的处理方法类似'''
        zoom_detail_selector=parsel.Selector(resp_text).xpath("//div[@class='zu-info']/p[1]")
        zoom_detail_list=[]
        for i in zoom_detail_selector:
            '''这里的字是html中的那个icon图标被强转为string时的结果，只需要使用空格替换掉即可'''
            detail=i.xpath("string(.)").get().strip().replace(" ", "").replace(""," ")
            zoom_detail_list.append(detail)

        print(zoom_link_list)
        print(zoom_describe_list)
        print(zoom_address_list)
        print(zoom_detail_list)
        print(zoom_price_list)
        '''以元组的形式返回给主函数，用以添加到总列表中'''
        return zoom_link_list,zoom_describe_list,zoom_address_list,zoom_detail_list,zoom_price_list


        # resp.encoding = resp.apparent_encoding
        #
        # soup = bs4.BeautifulSoup(resp.text, "html.parser")
        # print(resp.text)
        #
        # zoom_info = soup.find_all(name="div", class_="zu-itemmod")
        # print(zoom_info)
        # for item in zoom_info:
        #
        #     zoom_describe = item.a["title"]
        #     zoom_link = item.a["href"]
        #     zoom_details_find = item.p.text.strip()
        #     pat = re.compile(r'[\u4e00-\u9fa50-9]+')
        #     zoom_details_find_list = pat.findall(zoom_details_find)
        #     zoom_details_final_result = '-'.join(zoom_details_find_list)
        #     zoom_address_find = item.find_all(name="address", class_="details-item")[0].text.strip()
        #     zoom_address_result_list = pat.findall(zoom_address_find)
        #     zoom_address_final_result = "-".join(zoom_address_result_list)
        #     zoom_price = item.find_all(name="strong")[0].text
        #     print( zoom_link, zoom_details_final_result, zoom_address_final_result, zoom_price)
        #     time.sleep(0.2)
        #     pass
if __name__ == '__main__':
    '''这里因为要爬取1-50页的数据，所以使用for循环创建一个url列表，用来给下面不断请求'''
    url_list=[f"https://wh.zu.anjuke.com/fangyuan/p{page}/" for page in range(1,51)]
    # url = "https://wh.zu.anjuke.com/fangyuan/p1/"
    # 各个信息的总列表
    all_link_list=[]
    all_describe_list=[]
    all_address_list=[]
    all_detail_list=[]
    all_price_list=[]
    for url in url_list:
        # 每次调用get_crawler_infomation()函数都是获取一个页面上的所有信息，所以这里需要用list中的extend方法将每次爬取下来的结果合并到总列表中
        single_result=wh_housing_crawler().get_crawler_infomation(url)
        all_link_list.extend(single_result[0])
        all_describe_list.extend(single_result[1])
        all_address_list.extend(single_result[2])
        all_detail_list.extend(single_result[3])
        all_price_list.extend(single_result[4])

    # 建立字典，用来初始化DataFrame
    dict = {'房屋租住链接': all_link_list, '房屋描述': all_describe_list, "房屋地址": all_address_list, "房屋详情（户型）以及经纪人": all_detail_list,"房屋价格":all_price_list}
    df = pd.DataFrame(dict)
    # 将DataFrame以csv的形式写入“武汉出租房源情况.csv”文件中
    df.to_csv(r"C:\Users\16016\Desktop\武汉出租房源情况.csv",encoding='utf_8_sig')