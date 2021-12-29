import os
import sys

rootPath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(rootPath)
from zhihu_user_info_spider.requester.UserRequester import UserRequester
from zhihu_user_info_spider.scheduler.BaseScheduler import BaseScheduler

user_requester = UserRequester()


class UserScheduler(BaseScheduler):
    def __init__(self):
        BaseScheduler.__init__(self, name="userLogger")

    # 每天11点30分爬取用户详细信息
    def get_user_info(self):
        print("已开启爬取用户相信信息时刻表，每晚11点59分开始爬取")
        self.sche.add_job(user_requester.get_users, "cron", day_of_week="mon-sun", hour=23, minute=59)
        # self.sche.add_job(user_requester.get_users, "interval", seconds=0.5)
        self.sche.start()


if __name__ == '__main__':
    iser = UserScheduler()
    iser.get_user_info()
