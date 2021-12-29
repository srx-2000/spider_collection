from zhihu_user_info_spider.util.SpiderUtil import SpiderUtil
from zhihu_user_info_spider.scheduler.BaseScheduler import BaseScheduler

# 爬虫配置工具
spider_util = SpiderUtil()


class ModelRequester(BaseScheduler):
    def __init__(self):
        BaseScheduler.__init__(self,name="questionLogger")

    def _random_header(self):
        headers = {
            # "x-zse-93": "101_3_2.0",
            # "x-zse-96": "2.0_aMtBgg98SR2fcTYqT9YqnqrqFwFYUCNq8_N0FDuBb7tf",
            # "x-zst-81": "3_2.0ae3TnRUTEvOOUCNMTQnTSHUZo02p-HNMZBO8YD70rTtuQ0tqK6P0Ei9y-LS9-hp1DufI-we8gGHPgJO1xuPZ0GxCTJHR7820XM20cLRGDJXfgGCBxupMuD_Ie8FL7AtqM6O1VDQyQ6nxrRPCHukMoCXBEgOsiRP0XL2ZUBXmDDV9qhnyTXFMnXcTF_ntRueThHtK3qN8EUXxaBwYMQS8Ir9_OqHXqhwypq29tJwLjJXsDBpfs8Nm3gr_jhLPv0VZpCHMkAp1iwtpswN0KLt0VrUG-qFp3hoVDJH9nCN1reHV1gLyiBwCQ7xqsqompCeLmTVq6gUKVDS8HDC8qvS1IqOGUrNs6cN12uVKshoLeJS1fJxm4qfzWG_mwDS99Dx1m8YygcpqcRtxSLoBB_2Barc_hBXfzUxKB93OhbH_ChNxP920fLL9wgV0QgtK2ioCEge8fJeB-qpMhqV8x9gKDbOOQgpY89wmuwHL2JUC",
            "user-agent": spider_util.get_user_Agent()
        }
        return headers

    def _random_cookie(self):
        header = self._random_header()
        header["cookie"] = spider_util.get_cookie()
        return header
