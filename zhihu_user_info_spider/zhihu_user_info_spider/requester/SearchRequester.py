from zhihu_user_info_spider.proxypool.ProxyPool import Proxy_pool
from zhihu_user_info_spider.requester.ModeRequester import ModelRequester
from zhihu_user_info_spider.parser.Parser import Parser

# ip池
proxy_pool = Proxy_pool()


# # 保存配置工具
# save_util = SaveUtil()
# # 爬虫配置工具
# spider_util = SpiderUtil()
# # 用户model
# user_entity = UserEntityList()
# # 开启线程池
# thread_pool = ThreadPool(spider_util.get_thread_num())


class SearchRequester(ModelRequester):
    def __init__(self):
        super().__init__()

    def __get_user(self, uuid):
        url = "https://api.zhihu.com/people/{uuid}".format(uuid=uuid)
        json_result = proxy_pool.get_response(url=url, headers=self._random_header()).json()
        return json_result

    def __parser_user(self, json_data: dict):
        data = Parser.user_info_parser(json=json_data, is_add=False)
        # print(data)
        return data

    def get_user_info(self, uuid):
        json_dict = self.__get_user(uuid=uuid)
        return self.__parser_user(json_dict)


if __name__ == '__main__':
    sq = SearchRequester()
    json = sq.get_user_info("680bb09a357c9b943bfdea48d6c008ab")
    print(Parser.user_info_parser(json=json, database=True, is_add=False))
