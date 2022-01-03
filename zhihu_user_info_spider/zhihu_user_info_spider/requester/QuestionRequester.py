from zhihu_user_info_spider.proxypool.ProxyPool import Proxy_pool
from zhihu_user_info_spider.util.SaveUtil import SaveUtil
from zhihu_user_info_spider.util.SpiderUtil import SpiderUtil
from zhihu_user_info_spider.parser.Parser import Parser
from zhihu_user_info_spider.requester.ModeRequester import ModelRequester
from zhihu_user_info_spider.threadpool.ThreadPool import ThreadPool
import time

"""原定的使用用户的粉丝和关注进行传播，后经过尝试发现知乎经过这几年的迭代，
    在这模块的反爬已经做到很强了，需要独立的请求头，需要cookie，每个cookie请求500次左右就会被检测到【如果要爬百万级数据至少需要请求10w左右】
    需要使用打码平台进行打码操作【当然也可以建立cookie池，但是相比于打码更费时间】，而一向主张白嫖的我怎么会屈服，所以就有了以下的解决方式"""

# ip池
proxy_pool = Proxy_pool()
# 爬虫配置工具
spider_util = SpiderUtil()
# 保存配置工具
save_util = SaveUtil()


# parser = Parser() //原解析器，现已使用静态方法
# thread_pool = ThreadPool()


class QuestionRequester(ModelRequester):
    sum_num = 0
    __LIMIT = 20
    total_list = []

    def __init__(self):
        ModelRequester.__init__(self)

    # 获取知乎的热门话题，然后进入话题内直接查看回答者的uuid
    def __get_hot_question(self):
        url = "https://www.zhihu.com/hot"
        response_text = proxy_pool.get(url=url, headers=ModelRequester._random_cookie(self), retry_count=100,
                                       anonymity=True)
        return response_text.text

    # 获取知乎热榜并保存的接口，现定为该方法每天自动执行多次，然后每一个月统计一次用户数据，这样每天平均下来大概有3w-10w用户数据，一个月下来就是100w。
    def parse_hot_list_and_save(self):
        response_text = self.__get_hot_question()
        hot_list = Parser.hot_question_list_parser(response_text)
        hot_url_list = [f"https://www.zhihu.com/api/v4/questions/{question_id}/answers?offset=&limit=20" for question_id
                        in hot_list]
        # 筛选去重
        restore_list = save_util.restore_middle_data(save_util.HOT_LIST)
        for i in hot_url_list:
            if not restore_list.__contains__(i):
                restore_list.append(i)
        save_util.middle_save(save_util.question_list_model, restore_list)
        print("已更新今日热榜...")

    # 获取一个问题中所有回答者的uuid
    def __get_single_question_user_id(self, question_url: str):
        user_uuid_list = []
        url_split = question_url.split("&")
        final_url = "{offset}&".join(url_split).format(offset=0)
        now = 0
        try:
            total_num = self.__get_total(final_url)
            for i in range(0, total_num // self.__LIMIT):
                now = now + self.__LIMIT
                next_url = "{offset}&".join(url_split).format(offset=now)
                json_result = proxy_pool.get(next_url, headers=self._random_header(), anonymity=True).json()
                data = json_result["data"]
                for i in data:
                    if not i['author']['id'] == "0":
                        user_uuid_list.append(i['author']['id'])
            print(user_uuid_list)
            return user_uuid_list
        except Exception as e:
            print(e)
            self.job_logger.warning("问题：" + question_url + "该问题被封了")
            print("该问题被封了")

    # 获取当前问题所有回答数量
    def __get_total(self, question_url: str):
        json_result = proxy_pool.get(url=question_url, headers=ModelRequester._random_header(self), anonymity=True,
                                     retry_count=100).json()
        try:
            total_num = json_result['paging']['totals']
            self.sum_num += int(total_num)
            print(self.sum_num)
            return total_num
        except:
            # self.job_logger.warning("该问题被封了")
            print("该问题被封了")

    # hot question,user uuid commander
    def get_user_uuid(self):
        self.parse_hot_list_and_save()
        hot_list = save_util.restore_middle_data(file_type=save_util.HOT_LIST)
        for i in range(0, len(hot_list)):
            time.sleep(0.5)
            uuid_list = self.__get_single_question_user_id(hot_list[i])
            if uuid_list != None:
                if i == 0:
                    save_util.middle_save(save_util.user_uuid_list_model, uuid_list)
                else:
                    save_util.middle_save(save_util.user_uuid_list_model, uuid_list, attach=True)
            else:
                pass


if __name__ == '__main__':
    question_util = QuestionRequester()
    # question_util.get_user_uuid()
    question_util.parse_hot_list_and_save()
