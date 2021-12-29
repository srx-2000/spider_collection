import os
import sys

rootPath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(rootPath)
from zhihu_user_info_spider.scheduler.QuestionScheduler import QuestionScheduler
from zhihu_user_info_spider.scheduler.UserScheduler import UserScheduler

question_sche = QuestionScheduler()
user_sche = UserScheduler()


# @click.command("uuid")
def start_get_uuid():
    question_sche.daily_get_user_uuid()


# @click.command("hot")
def start_get_hot():
    question_sche.update_hot_list()


# @click.command("info")
def start_get_info():
    user_sche.get_user_info()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("请输入参数【hot、uuid、info】")
    else:
        if sys.argv[1] == "hot":
            start_get_hot()
        elif sys.argv[1] == "uuid":
            start_get_uuid()
        elif sys.argv[1] == "info":
            start_get_info()
        else:
            print("请正确输入要启动的模式【hot、uuid、info】")
