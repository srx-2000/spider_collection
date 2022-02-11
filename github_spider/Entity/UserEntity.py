import threading
from github_spider.util.util import Util

util = Util()


class UserEntity:
    id_list = []
    login_list = []
    email_list = []
    location_list = []
    hireable_list = []
    public_repos_num_list = []
    followers_num_list = []
    following_num_list = []
    repos_list = []
    index = 1
    df_dict = {}
    index_list = ["login", "id", "email", "location", "hireable", "public_repos", "followers", "following", "repos"]
    times = 0

    def __init__(self):
        self.clear_list()
        self.lock = threading.RLock()
        # 单次数据库数据增量
        self.list_size = util.get_batch_num()

    # 添加一条数据，如果列表中保存的数据量超过1000就会向文件中做一次增量保存
    def __add_user(self, user_dict: dict):
        self.id_list.append(user_dict["id"])
        self.login_list.append(user_dict["login"])
        self.email_list.append(user_dict["email"])
        self.location_list.append(user_dict["location"])
        self.hireable_list.append(user_dict["hireable"])
        self.public_repos_num_list.append(user_dict["public_repos"])
        self.followers_num_list.append(user_dict["followers"])
        self.following_num_list.append(user_dict["following"])
        self.repos_list.append(user_dict["repos"])
        # print("已获取用户：{uuid}的信息".format(uuid=user_dict["login"]))

    def add_user(self, single_user_info_dict: dict):
        self.lock.acquire()
        try:
            if self.index > self.list_size:
                self.times += 1
                for i in range(0, len(self.index_list)):
                    self.df_dict[self.index_list[i]] = list(self.__dict__.values())[i]
                util.save(self.df_dict)
                log_info = '\n'+f"已进行{self.times}数据次保存，单次数据保存量为：{self.list_size}"
                print(log_info, flush=True)
                self.index = 1
                self.clear_list()
                self.__add_user(single_user_info_dict)
                # self.user_uuid_sum_num -= self.list_size
            else:
                self.__add_user(single_user_info_dict)
                self.index += 1
        finally:
            self.lock.release()

    # 清空各个列表
    def clear_list(self):
        self.login_list = []
        self.id_list = []
        self.email_list = []
        self.location_list = []
        self.hireable_list = []
        self.public_repos_num_list = []
        self.followers_num_list = []
        self.following_num_list = []
        self.repos_list = []
