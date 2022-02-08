from zhihu_user_info_spider.util.SpiderUtil import SpiderUtil
from zhihu_user_info_spider.scheduler.BaseScheduler import BaseScheduler
from zhihu_user_info_spider.parser.Parser import Parser

# 爬虫配置工具
spider_util = SpiderUtil()
# 解析器
parser = Parser()


class ModelRequester(BaseScheduler):
    def __init__(self):
        BaseScheduler.__init__(self, name="questionLogger")

    def _random_header(self):
        headers = {
            "user-agent": spider_util.get_user_Agent()
        }
        return headers

    def _random_cookie(self):
        header = self._random_header()
        header["cookie"] = spider_util.get_cookie()
        return header

    def _header_with_zse_96(self, api_url: str):
        header = self._random_cookie()
        header["x-app-za"] = 'OS=Web'
        header["x-zse-93"] = "101_3_2.0"
        header["x-zse-96"] = Parser.get_x_zse_96(api_url)
        return header

    # 暂时没能破解成功，且可以通过别的途径绕过，所以本方法暂时无用
    def _header_with_zst_81(self, api_url: str):
        header = self._header_with_zse_96()
        header["x-zst-81"] = Parser.get_x_zst_81(api_url)
        return header
