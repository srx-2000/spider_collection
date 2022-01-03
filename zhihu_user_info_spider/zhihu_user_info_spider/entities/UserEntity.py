from zhihu_user_info_spider.util.SaveUtil import SaveUtil
from zhihu_user_info_spider.util.SpiderUtil import SpiderUtil
import threading
import logging
import os
from zhihu_user_info_spider.scheduler.BaseScheduler import BaseScheduler

# 批量爬取用户数据时，将会保存以下信息：
# id【每个用户的唯一标识】（id）  用户token【可以用来访问用户空间】（url_token）  用户昵称（name）  用户性别（gender）  用户等级（level_info.level）  用户头像url（avatar_url）  用户类型（type）  用户头文字【用户昵称后面跟的那个东西】（headline）
# 个人简介（description）  所在行业（business.name）  关注数（following_count）  粉丝数（follower_count）  回答数量（answer_count）  视频数（zvideo_count）  提问数量（question_count） 文章数（articles_count）
# 专栏数（columns_count） 收藏数（favorite_count）  关注的问题数量（following_question_count）  关注的话题数量（following_topic_count）  关注的专栏数量（following_columns_count）
# 关注的文件夹数量（following_favlists_count）  居住地（location.name【注意这里是个list，详情见刘看山的数据】）  被赞同次数（voteup_count）

save_util = SaveUtil()
spider_util = SpiderUtil()


# job_logger = logging.getLogger("UserInfoLog")
# logging.basicConfig(format="%(asctime)s - %(levelname)s: %(message)s",
#                     datefmt='%Y-%m-%d %H:%M:%S',
#                     level=logging.INFO,
#                     filemode='a',
#                     filename=os.path.dirname(
#                         os.getcwd()) + os.sep + "scheduler" + os.sep + "log" + os.sep + "UserInfoLog.log")


class UserEntityList(BaseScheduler):
    id_list = []
    user_token_list = []
    user_name_list = []
    user_gender_list = []
    user_level_list = []
    avatar_url_list = []
    user_type_list = []
    user_headline_list = []
    user_description_list = []
    user_business_list = []
    user_following_count_list = []
    user_follower_count_list = []
    user_answer_count_list = []
    user_zvideo_count_list = []
    user_question_count_list = []
    user_articles_count_list = []
    user_columns_count_list = []
    user_favorite_count_list = []
    user_following_question_count_list = []
    user_following_topic_count_list = []
    user_following_columns_count_list = []
    user_following_favlists_count_list = []
    user_location_list = []
    user_voteup_count_list = []
    index = 1
    df_dict = {}
    index_list = ["id", "用户token", "用户昵称", "用户性别", "用户等级", "用户头像url", "用户类型", "用户头文字", "个人简介", '所在行业', "关注数",
                  "粉丝数", "回答数量", "视频数", "提问数量", "文章数", "专栏数", "收藏数", "关注的问题数量", "关注的话题数量", "关注的专栏数量", "关注的文件夹数量",
                  "居住地", "被赞同次数"]
    times = 0

    def __init__(self):
        BaseScheduler.__init__(self, name="UserInfoLog")
        self.clear_list()
        self.lock = threading.RLock()
        self.user_uuid_sum_num = len(save_util.restore_middle_data(save_util.USER_ID_LIST))
        # 单次数据库数据增量
        self.list_size = spider_util.get_batch_num()

    # 添加一条数据，如果列表中保存的数据量超过1000就会向文件中做一次增量保存
    def __add_user(self, user_dict: dict):
        self.id_list.append(user_dict["id2"])
        self.user_token_list.append(user_dict["url_token"])
        self.user_name_list.append(user_dict["name"])
        if user_dict["gender"] == 1 or user_dict["gender"] == "男":
            self.user_gender_list.append("男")
        elif user_dict["gender"] == 0 or user_dict["gender"] == "女":
            self.user_gender_list.append("女")
        else:
            self.user_gender_list.append("未知")
        self.user_level_list.append(user_dict["level"])
        self.avatar_url_list.append(user_dict["avatar_url"])
        self.user_type_list.append(user_dict["type"])
        self.user_headline_list.append(user_dict["headline"])
        self.user_description_list.append(user_dict["description"])
        self.user_business_list.append(user_dict["business"])
        self.user_following_count_list.append(user_dict["following_count"])
        self.user_follower_count_list.append(user_dict["follower_count"])
        self.user_answer_count_list.append(user_dict["answer_count"])
        self.user_zvideo_count_list.append(user_dict["zvideo_count"])
        self.user_question_count_list.append(user_dict["question_count"])
        self.user_articles_count_list.append(user_dict["articles_count"])
        self.user_columns_count_list.append(user_dict["columns_count"])
        self.user_favorite_count_list.append(user_dict["favorite_count"])
        self.user_following_question_count_list.append(user_dict["following_question_count"])
        self.user_following_topic_count_list.append(user_dict["following_topic_count"])
        self.user_following_columns_count_list.append(user_dict["following_columns_count"])
        self.user_following_favlists_count_list.append(user_dict["following_favlists_count"])
        self.user_location_list.append(user_dict["location"])
        self.user_voteup_count_list.append(user_dict["voteup_count"])
        # print("已获取用户：{uuid}的信息".format(uuid=user_dict["id2"]))
        self.job_logger.info("已获取用户：{uuid}的信息".format(uuid=user_dict["id2"]))

    def add_user(self, single_user_info_dict: dict):
        self.lock.acquire()
        try:
            if self.index > self.list_size or (
                    self.user_uuid_sum_num < self.list_size and (self.user_uuid_sum_num == self.index)):
                self.times += 1
                for i in range(0, len(self.index_list)):
                    self.df_dict[self.index_list[i]] = list(self.__dict__.values())[i + 2]
                save_util.save(self.df_dict)
                print("已进行{times}数据次保存，单次数据保存量为：{size}".format(times=str(self.times), size=str(self.list_size)))
                self.job_logger.info(
                    "已进行{times}数据次保存，单次数据保存量为：{size}".format(times=str(self.times), size=str(self.list_size)))
                self.index = 1
                self.clear_list()
                self.__add_user(single_user_info_dict)
                self.user_uuid_sum_num -= self.list_size
            else:
                self.__add_user(single_user_info_dict)
                self.index += 1
        finally:
            self.lock.release()

    # 清空各个列表
    def clear_list(self):
        self.id_list = []
        self.user_token_list = []
        self.user_name_list = []
        self.user_gender_list = []
        self.user_level_list = []
        self.avatar_url_list = []
        self.user_type_list = []
        self.user_headline_list = []
        self.user_description_list = []
        self.user_business_list = []
        self.user_following_count_list = []
        self.user_follower_count_list = []
        self.user_answer_count_list = []
        self.user_zvideo_count_list = []
        self.user_question_count_list = []
        self.user_articles_count_list = []
        self.user_columns_count_list = []
        self.user_favorite_count_list = []
        self.user_following_question_count_list = []
        self.user_following_topic_count_list = []
        self.user_following_columns_count_list = []
        self.user_following_favlists_count_list = []
        self.user_location_list = []
        self.user_voteup_count_list = []

    # 保存1000条数据
    # def check_save(self):
    #     if self.index == self.list_size:
    #         for i in range(0, len(self.index_list)):
    #             self.df_dict[self.index_list[i]] = list(self.__dict__.values())[i]
    #             print("以获取列表："+list(self.__dict__.values())[i])
    #             save_util.save(self.df_dict)
    #         self.index = 0
    #         self.clear_list()
    #     else:
    #         pass


if __name__ == '__main__':
    entity = UserEntityList()
    entity.check_save()
