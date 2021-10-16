from zhihu_user_info.proxypool.ProxyPool import Proxy_pool
from zhihu_user_info.entities.UserEntity import UserEntityList
from zhihu_user_info.parser.Parser import Parser
from zhihu_user_info.util.SaveUtil import SaveUtil
from zhihu_user_info.util.SpiderUtil import SpiderUtil
from zhihu_user_info.threadpool.ThreadPool import ThreadPool
from zhihu_user_info.requester.ModeRequester import ModelRequester

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
        json_result = proxy_pool.get_response(url=url, headers=self._random_header()).json()
        # print(json_result)
        return json_result

    # 解析用户数据并保存
    def __parse_single_info(self, json_data: dict):
        Parser.user_info_parser(json=json_data)

    # single_user commander
    def __get_single_user(self, uuid):
        json_data = self.__get_single_info(uuid)
        self.__parse_single_info(json_data=json_data)

    def get_users(self):
        restore_list = save_util.restore_middle_data(save_util.USER_ID_LIST)
        for i in restore_list:
            thread_pool.run(func=self.__get_single_user, args=(i,))
            # print(i)
        self.__close_thread_pool()

    def __close_thread_pool(self):
        thread_pool.close()


# if __name__ == '__main__':
#     user = UserRequester()
#     user.get_users()
