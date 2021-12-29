import os
import sys

rootPath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(rootPath)
from zhihu_user_info_spider.requester.QuestionRequester import QuestionRequester
from zhihu_user_info_spider.scheduler.BaseScheduler import BaseScheduler

question_requester = QuestionRequester()


class QuestionScheduler(BaseScheduler):
    def __init__(self):
        BaseScheduler.__init__(self, name="questionLogger")

    # 由于懒得在每个类中加入logging模块了所以这里直接转接一下，从这里进行log了。
    def execute_update_hot_list(self):
        question_requester.parse_hot_list_and_save()
        self.job_logger.info("已更新今日热榜...")

    def execute_get_uuid(self):
        self.job_logger.info("正在获取用户uuid.....")
        question_requester.get_user_uuid()

    # 每隔2个小时更新一次热榜
    def update_hot_list(self):
        print("已开启热榜更新时刻表，每隔两小时获取一次")
        self.sche.add_job(self.execute_update_hot_list, "interval", hours=2)
        # self.sche.add_job(self.execute_update_hot_list, "interval", seconds=0.5)
        self.sche.start()

    # 每天晚上11点开始爬取今天获取热榜问题的回答的人的uuid，为后续爬取个人详细信息做前置准备
    def daily_get_user_uuid(self):
        print("已开启用户uuid时刻表，每晚11点爬取")
        self.sche.add_job(self.execute_get_uuid, "cron", day_of_week="mon-sun", hour=23)
        self.sche.start()


if __name__ == '__main__':
    # question_sche = QuestionScheduler()
    # question_sche.update_hot_list()
    # question_sche.daily_get_user_uuid()
    question_requester.get_user_uuid()