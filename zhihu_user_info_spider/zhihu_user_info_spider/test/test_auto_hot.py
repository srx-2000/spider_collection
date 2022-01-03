import requests
from zhihu_user_info_spider.util import SpiderUtil
import parsel
from zhihu_user_info_spider.parser.Parser import Parser

spider_util = SpiderUtil()

# username = "13718322331"
# password = "srx62600"
headers = {
    "user-agent": spider_util.get_user_Agent(),
    "cookie": spider_util.get_cookie()
}

url = "https://www.zhihu.com/hot"

response_text = requests.get(url=url, headers=headers).text

url_list = parsel.Selector(response_text).xpath("//div[@class='HotItem-content']/a/@href").getall()

# print(response_text)
hot_list = Parser.hot_question_list_parser(response_text)
print(hot_list)
