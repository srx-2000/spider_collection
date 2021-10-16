import os
from zhihu_user_info.util.Utils import Util
import pandas as pd
import threading


# 保存方法工具类主要作用：读取json文件并按配置文件中所指定的方法进行保存
class SaveUtil(Util):
    question_list_model = 1
    # answer_list_model = 2
    user_uuid_list_model = 3
    HOT_LIST = 11
    USER_ID_LIST = 12

    def __init__(self):
        super().__init__()
        self.path = os.path.dirname(os.path.dirname(self.abs_path)) + os.sep + "result" + os.sep
        self.hot_path = self.path + "hotList" + os.sep + self.year + os.sep + self.month + os.sep + self.day + os.sep
        self.user_path = self.path + "userUUID" + os.sep + self.year + os.sep + self.month + os.sep + self.day + os.sep
        self.lock = threading.RLock()

    # 用来保存中间产物
    def middle_save(self, model: int, data: list, attach=False):
        file_name = ""
        if model == self.question_list_model:
            flag = os.path.exists(self.hot_path)
            if not flag:
                os.makedirs(self.hot_path)
            file_name = "hot_list-" + self.year + "-" + self.month + "-" + self.day + ".txt"
            f_w = open(self.hot_path + file_name, mode="w", encoding="utf-8")
            for i in data:
                f_w.write(str(i) + "\n")
            f_w.close()
        # elif model == self.answer_list_model:
        #     file_name = "answer_list-" + self.year + "-" + self.month + "-" + self.day + ".txt"
        #     f_w = open(self.path + file_name, mode="w", encoding="utf-8")
        #     for i in data:
        #         f_w.write(str(i) + "\n")
        #     f_w.close()
        elif model == self.user_uuid_list_model:
            flag = os.path.exists(self.user_path)
            if not flag:
                os.makedirs(self.user_path)
            file_name = "user_uuid-" + self.year + "-" + self.month + "-" + self.day + ".txt"

            if os.path.exists(self.user_path + file_name):
                f_w = open(self.user_path + file_name, mode="a", encoding="utf-8")
            elif attach:
                f_w = open(self.user_path + file_name, mode="a", encoding="utf-8")
            else:
                f_w = open(self.user_path + file_name, mode="w", encoding="utf-8")
            for i in data:
                f_w.write(str(i) + "\n")
            f_w.close()

    # 该方法用于恢复中间产物的数据，
    # 该方法如果是hotlist调用，那么应该每天晚上十二点之前调用一次，以免出现路劲错误
    def restore_middle_data(self, file_type: int):
        data_list = []
        if file_type == self.HOT_LIST:
            for root, dirs, files in os.walk(self.hot_path):
                for f in files:
                    with open(os.path.join(root, f), mode="r", encoding="utf-8") as f_r:
                        for i in f_r.readlines():
                            data_list.append(i.strip("\n"))
        if file_type == self.USER_ID_LIST:
            for root, dirs, files in os.walk(self.user_path):
                for f in files:
                    with open(os.path.join(root, f), mode="r", encoding="utf-8") as f_r:
                        for i in f_r.readlines():
                            data_list.append(i.strip("\n"))
        return data_list

    def save(self, data_dict):
        if "save_method" in self.json_result:
            save_method = self.json_result["save_method"]
            if save_method == "csv":
                self.__save_by_csv(data_dict)
            elif save_method == "txt":
                self.__save_by_txt(data_dict)
        else:
            print("请在util_content.json中配置save_method。")

    # 使用csv保存
    def __save_by_csv(self, data_dict):
        # data_dict = pd.DataFrame(data=data_dict, index=[0])
        df = pd.DataFrame(data_dict)
        # file_name = self.path + "user_info-" + str(int(time.time())) + ".csv"
        file_name = self.path + "user_info.csv"
        flag = os.path.exists(file_name)
        # df.to_csv(self.path + "user_info-" + str(int(time.time())) + ".csv", mode="w")
        if flag:
            df.to_csv(file_name, mode="a", header=False)
        else:
            df.to_csv(file_name, mode="w")
        # # 数据清洗
        # df_clean = pd.read_csv("user_info.csv")
        # index_list = ["index", "id", "用户token", "用户昵称", "用户等级", "用户头像url", "用户类型", "用户头文字", "个人简介", '所在行业', "关注数",
        #               "粉丝数", "回答数量", "视频数", "提问数量", "文章数", "专栏数", "收藏数", "关注的问题数量", "关注的话题数量", "关注的专栏数量", "关注的文件夹数量",
        #               "居住地", "被赞同次数"]
        # df_clean = df_clean.dropna(how="any")
        # df1 = df_clean.drop_duplicates(inplace=False)
        # df1.columns = index_list
        # del df1["index"]
        # df1.to_csv(self.path + "\\user_info_cleaned.csv", encoding='utf_8_sig', index=None)

    # 使用txt保存
    def __save_by_txt(self, dict):
        # df = pd.DataFrame(dict)
        pass
