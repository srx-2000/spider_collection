import threading
from github_spider.util.util import Util

util = Util()


class RepoEntity:
    repo_name_list = []
    commit_num_list = []
    total_list = []
    additions_list = []
    deletions_list = []
    commit_list_list = []
    index = 1
    df_dict = {}
    index_list = ["repo_name", "commit_num", "total", "additions", "deletions", "commit_list"]
    times = 0

    def __init__(self):
        self.clear_list()
        self.lock = threading.RLock()
        # 单次数据库数据增量
        self.list_size = util.get_batch_num(is_repo=True)

    # 添加一条数据，如果列表中保存的数据量超过1000就会向文件中做一次增量保存
    def __add_repo(self, user_tuple: tuple):
        self.repo_name_list.append(user_tuple[0]["repo_name"])
        self.commit_num_list.append(user_tuple[0]["commit_num"])
        self.total_list.append(user_tuple[0]["total"])
        self.additions_list.append(user_tuple[0]["additions"])
        self.deletions_list.append(user_tuple[0]["deletions"])
        self.commit_list_list.append(user_tuple[-1])
        # print("已获取用户：{uuid}的信息".format(uuid=user_dict["login"]))

    def add_repo(self, repo_tuple: tuple):
        self.lock.acquire()
        try:
            if self.index > self.list_size:
                self.times += 1
                for i in range(0, len(self.index_list)):
                    self.df_dict[self.index_list[i]] = list(self.__dict__.values())[i]
                util.save(self.df_dict, is_repo=True)
                log_info = '\n' + f"已进行{self.times}数据次保存，单次数据保存量为：{self.list_size}"
                print(log_info, flush=True)
                self.index = 1
                self.clear_list()
                self.__add_repo(repo_tuple)
            else:
                self.__add_repo(repo_tuple)
                self.index += 1
        finally:
            self.lock.release()

    # 清空各个列表
    def clear_list(self):
        self.repo_name_list = []
        self.commit_num_list = []
        self.total_list = []
        self.additions_list = []
        self.deletions_list = []
        self.commit_list_list = []
