import parsel
import pandas as pd
from anjuke_room_rent_info import Proxy_pool
import os

class wh_housing_crawler:
    proxy_pool=Proxy_pool.Proxy_pool()
    def get_crawler_infomation(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }

        '''这里不建议使用cookie了，容易被锁，反正不用cookie也一样爬'''
        # cookie = {
        #     'cookie': 'aQQ_ajkguid=F0FD99AE-6908-73F8-737F-FE0EE73B201F; 58tj_uuid=2f56b069-a674-4b4a-baf3-02aec6082a39; _ga=GA1.2.49098926.1622276564; id58=e87rkGCx+dJ+Dk2LWD05Ag==; als=0; sessid=2F0970ED-925C-270A-01EC-E8C046035340; ctid=549; twe=2; _gid=GA1.2.490847335.1625984404; obtain_by=2; new_session=1; init_refer=https%253A%252F%252Fwww.baidu.com%252Fother.php%253Fsc.0f0000KnL8OYnGM8b_aM6W5fkJ15FoWBY0s0P2a6kdRIAXUWyavGaTmBjr2q44KTTzM9bUWofUXV6Suo_c9mKA4Q830jR0fhRkmUd-4oahfXXd0_0snFKYChZPYGk17Nc_zcE9TecUuQBA1efX1jhw82WiCnrd0ZdtSG24LaI-ligCGmcCWdHk1Drt-SRVKOnSC4ufvyazIl7YeV2S1V1DWPggjD.DY_NR2Ar5Od663rj6thm_8jViBjEWXkSUSwMEukmnSrZr1wC4eL_8C5RojPak3S5Zm0.TLFWgv-b5HDkrfK1ThPGujYknHb0THY0IAYq_Q2SYeOP0ZN1ugFxIZ-suHYs0A7bgLw4TARqnsKLULFb5UazEVrO1fKzmLmqnfKdThkxpyfqnHRzrjD1Pjbsn6KVINqGujYkPjnLn1m4PfKVgv-b5HDknjfkPj6d0AdYTAkxpyfqnHczP1n0TZuxpyfqn0KGuAnqiD4a0ZKGujY1PsKWpyfqn0KWThnqnWnLPHc%2526dt%253D1625984396%2526wd%253D%2525E5%2525AE%252589%2525E5%2525B1%252585%2525E5%2525AE%2525A2%2526tpl%253Dtpl_12273_25609_21806%2526l%253D1528134902; new_uv=2; lps=https%3A%2F%2Frcheng.zu.anjuke.com%2F%3Ffrom%3Dnavigation%7Chttps%3A%2F%2Frongchengshi.anjuke.com%2F; cmctid=522; wmda_uuid=1b37a947daea0242d94083cb95843922; wmda_new_uuid=1; wmda_session_id_6289197098934=1625984421370-3493f67e-7167-f700; wmda_visited_projects=%3B6289197098934; ajkAuthTicket="TT=5b34c0e4bc87c768a988c8a0a69d2ab0&TS=1625984486646&PBODY=i1AQZ_dCwBl-uS8FB8pZtkOlrZKCN4RC3Lo1DttpsvzklXph5lH2JS-1oN-5DS2WTIqRWnYj6da3ms_gIac4kWOCeQ6QJhYUY9gMPMfF1iJqkb-eoNOyXdGlv6qgR_uCPVIWbaQK3J3TAiZkMXxKTHYyVSmMyWnlR3jvxFaeO2U&VER=2"; xxzl_cid=92c48cfa13664d818cf67864db3ccd81; xzuid=7a4085ab-9277-4eba-99f5-c374feaf96cf'
        # }

        '''这里不建议使用https代理，因为代理源的https代理过少，很容易出现多个https代理被重复使用，导致ip被封，这样代理池就没有意义了
        使用http代理依旧可以访问，所以不到非不得已不要还是用https代理'''
        # 使用代理池访问网页
        resp=self.proxy_pool.get_response(url=url,headers=headers,https=False)

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

if __name__ == '__main__':
    crawler=wh_housing_crawler()
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
        single_result=crawler.get_crawler_infomation(url)
        all_link_list.extend(single_result[0])
        all_describe_list.extend(single_result[1])
        all_address_list.extend(single_result[2])
        all_detail_list.extend(single_result[3])
        all_price_list.extend(single_result[4])

    # 建立字典，用来初始化DataFrame
    dict = {'房屋租住链接': all_link_list, '房屋描述': all_describe_list, "房屋地址": all_address_list, "房屋详情（户型）以及经纪人": all_detail_list,"房屋价格":all_price_list}
    df = pd.DataFrame(dict)
    # 将DataFrame以csv的形式写入“武汉出租房源情况.csv”文件中
    df.to_csv(os.getcwd()+"//result//武汉出租房源情况.csv",encoding='utf_8_sig')