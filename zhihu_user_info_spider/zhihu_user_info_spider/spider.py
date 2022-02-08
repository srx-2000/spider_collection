import os
import sys

rootPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(rootPath)

from zhihu_user_info_spider.requester.UserRequester import UserRequester
from zhihu_user_info_spider.requester.QuestionRequester import QuestionRequester

# 批量爬取用户数据时，将会保存以下信息：
# id【每个用户的唯一标识】（id）  用户token【可以用来访问用户空间】（url_token）  用户昵称（name）  用户性别（gender）  用户等级（level_info.level）  用户头像url（avatar_url）  用户类型（type）  用户头文字【用户昵称后面跟的那个东西】（headline）
# 个人简介（description）  所在行业（business.name）  关注数（following_count）  粉丝数（follower_count）  回答数量（answer_count）  视频数（zvideo_count）  提问数量（question_count） 文章数（articles_count）
# 专栏数（columns_count） 收藏数（favorite_count）  关注的问题数量（following_question_count）  关注的话题数量（following_topic_count）  关注的专栏数量（following_columns_count）
# 关注的文件夹数量（following_favlists_count）  居住地（location.name【注意这里是个list，详情见刘看山的数据】）  被赞同次数（voteup_count）

question_requester = QuestionRequester()
user_requester = UserRequester()


class Spider(object):

    def __init__(self):
        pass

    def get_questions(self):
        question_requester.get_user_uuid()

    def get_users(self):
        user_requester.get_users()


if __name__ == '__main__':
    spider = Spider()
    # 这里获取问题的爬虫建议一天跑3-4次
    spider.get_questions()
    # 这里获取用户信息的爬虫建议一天跑一次，且在上方question爬虫运行至少一次之后再运行。
    # 上面那个问题次数爬虫运行的越多单次爬取的用户数据越多，重复率越低
    spider.get_users()
