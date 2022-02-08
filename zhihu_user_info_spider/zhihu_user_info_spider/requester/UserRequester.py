from zhihu_user_info_spider.proxypool.ProxyPool import Proxy_pool
from zhihu_user_info_spider.entities.UserEntity import UserEntityList
from zhihu_user_info_spider.parser.Parser import Parser
from zhihu_user_info_spider.util.SaveUtil import SaveUtil
from zhihu_user_info_spider.util.SpiderUtil import SpiderUtil
from zhihu_user_info_spider.threadpool.ThreadPool import ThreadPool
from zhihu_user_info_spider.requester.ModeRequester import ModelRequester
from zhihu_user_info_spider.Exception.SpiderException import SpiderException

# ip池
proxy_pool = Proxy_pool()
# 保存配置工具
save_util = SaveUtil()
# 爬虫配置工具
spider_util = SpiderUtil()
# 用户model
user_entity = UserEntityList()
# 开启线程池
thread_pool = ThreadPool(spider_util.get_thread_num())


class UserRequester(ModelRequester):
    # 通过接口获取单个用户的数据
    def __get_single_info(self, uuid):
        url = "https://api.zhihu.com/people/{uuid}".format(uuid=uuid)
        # 如果使用可匿名代理可能爬取速度会下降的比较多，但如果不使用匿名代理，那么极有可能爬到一定数量之后，偶然间暴露本机ip导致本机ip被封
        json_result = proxy_pool.get(url=url, headers=ModelRequester._random_cookie(self), anonymity=False).json()
        return json_result

    # 解析用户数据并保存
    def __parse_single_info(self, json_data: dict):
        Parser.user_info_parser(json=json_data)

    # single_user commander
    def __get_single_user(self, uuid):
        # print("用户："+uuid)
        json_data = self.__get_single_info(uuid)
        self.__parse_single_info(json_data=json_data)

    def get_users(self):
        restore_list = save_util.restore_middle_data(save_util.USER_ID_LIST)
        for i in restore_list:
            thread_pool.run(func=self.__get_single_user, args=(i,), callback=self.callback_fun)
            # print(i)
            # self.__get_single_user(i)
        self.__close_thread_pool()

    def __close_thread_pool(self):
        thread_pool.close()

    def callback_fun(self, status, result):
        if not status:
            raise SpiderException(result)


if __name__ == '__main__':
    user = UserRequester()
    user.get_users()
