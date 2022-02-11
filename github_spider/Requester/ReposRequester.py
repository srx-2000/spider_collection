from github_spider.Requester.BaseRequester import BaseRequester
from github_spider.Parser.Parser import Parser
from github_spider.util.util import Util
from github_spider.threadpool.ThreadPool import ThreadPool
from github_spider.Entity.RepoEntity import RepoEntity
from github_spider.Requester.UserRequester import UserRequester
import requests
import os
import parsel
import time

util = Util()
thread = ThreadPool(util.get_thread_num())
repo_entity = RepoEntity()
user_requester = UserRequester()


class ReposRequester(BaseRequester):
    def __init__(self):
        BaseRequester.__init__(self)
        self.result_path = os.path.dirname(os.getcwd()) + os.sep + "result" + os.sep

    # 获取README
    def get_readme(self, username: str, repo_name: str):
        url = f"https://raw.githubusercontent.com/{username}/{repo_name}/master/README.md"
        response_text = requests.get(url, headers=self._random_header()).text
        path = self.result_path + username + os.sep + repo_name + os.sep
        if not os.path.exists(path):
            os.makedirs(path)
        with open(path + "README.md", "w", encoding="utf-8") as f:
            f.write(response_text)
        f.close()

    def get_repo_detail(self, username: str, repo_name: str):
        url = f"https://api.github.com/repos/{username}/{repo_name}/"
        self._test()
        json_result = requests.get(url, headers=self._random_header()).json()
        repos_dict = Parser.parser_repos(json_result)
        return repos_dict

    def __get_commit_num(self, username: str, repo_name: str):
        url = f"https://github.com/{username}/{repo_name}/"
        response_text = requests.get(url, headers=self._random_header()).text
        commit_num_str = parsel.Selector(response_text).xpath("//a/span['d-none d-sm-inline']/strong/text()").get()
        if commit_num_str == None:
            # 此时库为空库
            commit_num = 0
        else:
            commit_num = int(commit_num_str.replace(",", ""))
        return commit_num

    def get_repo_commit(self, username: str, repo_name: str, is_save=False):
        # 如果break_count大于20，证明一个问题的获取以超出了20秒，那么此时放弃这个问题用户的获取
        break_count = 0
        count_list = []
        commit_num = self.__get_commit_num(username, repo_name)
        if commit_num == 0:
            page = 0
        elif commit_num < 100:
            page = 1
        else:
            page = commit_num // 100 + 1
        # 用来存放所有的commit的相关信息，其中包括每次commit的sha，changed files，additions，deletions
        commit_list = []
        # 用来存放一个库所欲commit数据变化的总值，但无法精确到每次commit的sha
        repo_commit_dict = {}
        for i in range(page):
            url = f"https://api.github.com/repos/{username}/{repo_name}/commits?page={i}&per_page=100"
            self._test()
            json_result = requests.get(url, headers=self._random_header()).json()
            commit_sha_list = Parser.parser_commit(json_result, is_json=True)
            for j in range(len(commit_sha_list)):
                thread.run(func=self.__get_single_commit,
                           args=(username, repo_name, commit_sha_list[j], commit_list, count_list),
                           callback=self.callback)
            while True:
                util.process_bar(percent=len(commit_list) / commit_num,
                                 start_str=f"对库{username}/{repo_name}的commit的爬取进度：", end_str="100%",
                                 total_length=50)
                if len(commit_list) < commit_num:
                    if len(count_list) == len(commit_sha_list):
                        count_list = []
                        break
                    else:
                        # time.sleep(1)
                        last_count = len(commit_list)
                        time.sleep(1)
                        if last_count == len(commit_list):
                            break_count += 1
                        else:
                            break_count = 0
                        if break_count >= 60 and self._get_limit_count() < 4999:
                            print("\n该repo的commit的获取时间卡了超过60秒，已放弃该repo")
                            break
                else:
                    break
        if len(commit_list) == 0:
            return None
        for i in commit_list:
            if i == None:
                pass
            else:
                if not repo_commit_dict.__contains__("total"):
                    repo_commit_dict["total"] = i["total"]
                repo_commit_dict["total"] += i["total"]
                if not repo_commit_dict.__contains__("additions"):
                    repo_commit_dict["additions"] = i["total"]
                repo_commit_dict["additions"] += i["additions"]
                if not repo_commit_dict.__contains__("deletions"):
                    repo_commit_dict["deletions"] = i["total"]
                repo_commit_dict["deletions"] += i["deletions"]
        repo_commit_dict["commit_num"] = commit_num
        repo_commit_dict["repo_name"] = username + "/" + repo_name
        thread.close()
        if is_save:
            repo_entity.add_repo((repo_commit_dict, commit_list))
        return repo_commit_dict, commit_list

    def __get_single_commit(self, username, repo_name, commit_sha: str, commit_list: list, count_list: list):
        try:
            commit_dict = {}
            commit_url = f"https://github.com/{username}/{repo_name}/commit/{commit_sha}"
            response_text = requests.get(commit_url, headers=self._random_header()).text
            change_num_list = Parser.parser_commit(response_text)
            commit_dict["sha"] = commit_sha
            # 这里的total指的是修改的文件的数量，因为总代吗修改行数本身是没有的，
            # 如果想要硬算的话，其实就是把additions和deletions做了个减法，我感觉没必要，还不如总修改文件数量来的实在
            commit_dict["total"] = change_num_list[0]
            commit_dict["additions"] = change_num_list[1]
            commit_dict["deletions"] = change_num_list[2]
        except:
            commit_dict = None
        commit_list.append(commit_dict)
        count_list.append(commit_dict)

    def callback(self, status, result):
        # print(status)
        # print(result)
        pass

    def get_repos(self, user, is_save=False):
        user_repo_list = []
        # 如果传入的user是一个字符串，此时模式会切换为根据用户名，爬取该用户所有的库
        if type(user) == str:
            user_dict = user_requester.get_single_user_info(username=user)
            if user_dict == None:
                pass
            for i in range(len(user_dict["repos"])):
                repo_name = str(user_dict["repos"][i].split("/")[-1])
                result = self.get_repo_commit(user, repo_name, is_save=is_save)
                user_repo_list.append(result)
            return user_repo_list
        # 如果传入的一个list，那么证明需要大量爬取用户库了，那么此时会将传入的list进行解析，然后批量爬取
        elif type(user) == list:
            for i in range(len(user)):
                if user[i] == None:
                    pass
                else:
                    username = user[i]["login"]
                    repos = user[i]["repos"]
                    for j in range(len(repos)):
                        repo_name = str(repos[j].split("/")[-1])
                        result = self.get_repo_commit(username, repo_name, is_save=is_save)
                        user_repo_list.append(result)
            return user_repo_list
        else:
            print("请输入正确的user：1.用户名（str）\t2.用户列表(list[dict])【如没有，请使用user_requester.get_users()方法获取】")


if __name__ == '__main__':
    r = ReposRequester()
    u = UserRequester()
    # print(r.get_repos("srx-2000", is_save=True))
    user_list = u.get_users(100)
    print(r.get_repos(user_list, is_save=True))
    # print(r.get_repo_commit(username="Yatsu-domy", repo_name="whut"))
