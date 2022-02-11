import json
import parsel


# login【用户名（srx-2000）】,id【id（54949399）】,email【邮箱】,location【地址（北京）】,hireable【招聘状态】,public_repos【公开库数量】,followers【粉丝数量】,following【关注数量】,
# html_url【仓库地址（https://github.com/srx-2000/spider_collection）】,description【仓库描述】,fork【仓库fork数量】,total【库的总代码修改行数】,additions【库的总代码增加行数】,deletions【库的总代码减少行数】
# files【提交次数】
class Parser(object):
    # 这里的single参数是用来区分是要解析单个用户，还是解析得到所有用户
    # 如果置为True那么此时函数就会将传入的result_json当做单个用户的信息进行解析
    # 如果置为False那么此时函数就会将传入的result_json当做一个user列表进行解析
    # 同时该方法还会解析传入的用户的库，返回一个列表
    @staticmethod
    def parser_user(result_json, single=True):
        single_user_info_dict = {}
        all_user_list = []
        user_repos_list = []
        if type(result_json) == list:
            if single:
                for i in result_json:
                    user_repos_list.append(i["html_url"])
                return user_repos_list
            else:
                for i in result_json:
                    single_user = dict()
                    single_user["login"] = i["login"]
                    single_user["id"] = i["id"]
                    all_user_list.append(single_user)
                return all_user_list
        else:
            single_user_info_dict["login"] = result_json["login"]
            single_user_info_dict["id"] = result_json["id"]
            single_user_info_dict["email"] = result_json["email"]
            single_user_info_dict["location"] = result_json["location"]
            single_user_info_dict["hireable"] = result_json["hireable"]
            single_user_info_dict["public_repos"] = result_json["public_repos"]
            single_user_info_dict["followers"] = result_json["followers"]
            single_user_info_dict["following"] = result_json["following"]
            return single_user_info_dict

    @staticmethod
    def parser_repos(json_result):
        repos_dict = dict()
        repos_dict["fork"] = json_result["network_count"]
        repos_dict["description"] = json_result["description"]
        return repos_dict

    @staticmethod
    def parser_commit(result, is_json=False):
        if is_json:
            commit_list_sha = list()
            for i in result:
                commit_list_sha.append(i["sha"])
            return commit_list_sha
        else:
            num_list = parsel.Selector(result).xpath('//*[@id="toc"]/div[2]//*/text()').getall()
            # print(num_list)
            change_num_list = []
            for i in num_list:
                if str(i).strip() != "":
                    change_num_list.append(int(str(i).strip().split(" ")[0].replace(",", "")))
            # print(change_num_list)
            return change_num_list
