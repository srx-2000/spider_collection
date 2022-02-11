from github_spider.Requester.BaseRequester import BaseRequester
from github_spider.Parser.Parser import Parser
from github_spider.util.util import Util
from github_spider.threadpool.ThreadPool import ThreadPool
from github_spider.Entity.UserEntity import UserEntity
import time
import requests
import random

# from pprint import pprint

util = Util()
thread = ThreadPool(util.get_thread_num())

user_entity = UserEntity()


class UserRequester(BaseRequester):
    def __init__(self):
        BaseRequester.__init__(self)
        self.user_max_num = 99300000

    # 通过接口获取一定数量的用户
    def __get_users(self, user_num) -> list:
        if user_num < 100:
            page_size = user_num
            page = 1
        else:
            page = user_num // 100
            page_size = 100
        user_list = []
        for i in range(page):
            since = random.randint(0, self.user_max_num)
            print(f"\r获取用户id中,共{page}页：第{i + 1}页,生成的随机种子是：{since}", end="", flush=True)
            url = f"https://api.github.com/users?repos>0&since={since}&per_page={page_size}"
            self._test()
            json_result = requests.get(url=url, headers=self._random_header()).json()
            user_list.extend(Parser.parser_user(json_result, single=False))
        return user_list

    # 对外暴露的，获取单个用户信息
    def get_single_user_info(self, username, is_save=False) -> dict:
        try:
            user_info_dict = self.__get_base_info(username)
            user_info_dict["repos"] = self.__get_user_repos(username, user_info_dict["public_repos"])
            if is_save:
                user_entity.add_user(user_info_dict)
            return user_info_dict
        except:
            return None

    # 内用方法，不对外暴露
    def __get_single_user_info(self, username, user_list: list, is_save=True):
        user_list.append(self.get_single_user_info(username, is_save=is_save))

    # 获取一个用户的所有库的连接
    def __get_user_repos(self, username, repo_num) -> list:
        if repo_num < 100:
            page = 1
            page_size = repo_num
        else:
            page = repo_num // 100
            page_size = 100
        repos = list()
        for i in range(page):
            url = f"https://api.github.com/users/{username}/repos?page={i}&per_page={page_size}"
            self._test()
            json_result = requests.get(url=url, headers=self._random_header()).json()
            repos = Parser.parser_user(json_result)
        return repos

    # 获取一个用户的基础信息
    def __get_base_info(self, username) -> dict:
        info_api = f"https://api.github.com/users/{username}"
        self._test()
        json_result = requests.get(url=info_api, headers=self._random_header()).json()
        user_info = Parser.parser_user(json_result)
        return user_info

    # 对外暴露的批量获取用户的函数
    def get_users(self, user_num, is_save=False) -> list:
        # 如果break_count大于20，证明一个问题的获取以超出了20秒，那么此时放弃这个问题用户的获取
        break_count = 0
        username_list = self.__get_users(user_num)
        user_list = list()
        for i in range(len(username_list)):
            thread.run(func=self.__get_single_user_info, args=(username_list[i]["login"], user_list, is_save,),
                       callback=self.callback)
        while True:
            util.process_bar(percent=len(user_list) / len(username_list), start_str="已获取用户进度：", end_str="100%",
                             total_length=50)
            if len(user_list) < len(username_list):
                last_count = len(user_list)
                time.sleep(1)
                if last_count == len(user_list):
                    break_count += 1
                else:
                    break_count = 0
                if break_count >= 60 and self._get_limit_count() < 4999:
                    print("\n该用户的获取时间卡了超过60秒，已放弃后续用户")
                    break
            else:
                break
        return user_list

    def callback(self, status, result):
        # print(status)
        # print(result)
        pass


if __name__ == '__main__':
    user_requester = UserRequester()
    # print(user_requester.get_single_user_info("srx-2000"))
    users = user_requester.get_users(100, is_save=True)
    thread.close()
    print("\n")
    print(users)
    # pprint(users)
