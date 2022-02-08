from zhihu_user_info_spider.proxypool.ProxyPool import Proxy_pool
from zhihu_user_info_spider.util.SaveUtil import SaveUtil
from zhihu_user_info_spider.util.SpiderUtil import SpiderUtil
from zhihu_user_info_spider.parser.Parser import Parser
from zhihu_user_info_spider.requester.ModeRequester import ModelRequester
from zhihu_user_info_spider.threadpool.ThreadPool import ThreadPool
from zhihu_user_info_spider.scheduler.BaseScheduler import BaseScheduler
import time
import traceback
import re

"""原定的使用用户的粉丝和关注进行传播，后经过尝试发现知乎经过这几年的迭代，
    在这模块的反爬已经做到很强了，需要独立的请求头，需要cookie，每个cookie请求500次左右就会被检测到【如果要爬百万级数据至少需要请求10w左右】
    需要使用打码平台进行打码操作【当然也可以建立cookie池，但是相比于打码更费时间】，而一向主张白嫖的我怎么会屈服，所以就有了以下的解决方式"""

# ip池
proxy_pool = Proxy_pool()
# 爬虫配置工具
spider_util = SpiderUtil()
# 保存配置工具
save_util = SaveUtil()
# 开启线程池
thread_pool = ThreadPool(spider_util.get_thread_num())


# parser = Parser() //原解析器，现已使用静态方法


class QuestionRequester(ModelRequester, BaseScheduler):
    sum_num = 0
    __LIMIT = 20
    total_list = []

    def __init__(self):
        ModelRequester.__init__(self)
        BaseScheduler.__init__(self, name="questionLogger")

    # 获取知乎的热门话题，然后进入话题内直接查看回答者的uuid
    def __get_hot_question(self):
        # 该接口已被知乎使用动态加载给ban了
        # url = "https://www.zhihu.com/hot"
        url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total"
        try:
            response = proxy_pool.get(url=url, headers=ModelRequester._random_header(self), retry_count=100,
                                      anonymity=True).json()
            return response
        except Exception:
            self.job_logger.error("热榜更新失败,请带着以下报错去github原仓库提出issue")
            self.job_logger.exception(traceback.print_exc())
            return None

    # 获取知乎热榜并保存的接口，现定为该方法每天自动执行多次，然后每一个月统计一次用户数据，这样每天平均下来大概有3w-10w用户数据，一个月下来就是100w。
    def parse_hot_list_and_save(self):
        response_json = self.__get_hot_question()
        hot_list = Parser.hot_question_list_parser_v2(response_json)
        hot_url_list = [
            f"https://www.zhihu.com/api/v4/questions/{question_id}/answers?" \
            f"include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2" \
            f"Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2" \
            f"Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2" \
            f"Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Cis_labeled%2" \
            f"Cpaid_info%2Cpaid_info_content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_recognized%3" \
            f"Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cvip_info%2Cbadge%5B%2A%5D.topics%3Bdata%5B%2A%5D." \
            f"settings.table_of_content.enabled&limit={self.__LIMIT}&offset=0&platform=desktop&sort_by=default"
            for question_id
            in hot_list]
        # 筛选去重
        restore_list = save_util.restore_middle_data(save_util.HOT_LIST)
        for i in hot_url_list:
            if not restore_list.__contains__(i):
                restore_list.append(i)
        save_util.middle_save(save_util.question_list_model, restore_list)
        print("已更新今日热榜...")

    # 获取一个问题中所有回答者的uuid
    def __get_single_question_user_id(self, question: str):
        user_uuid_list = []
        count_list = []
        now = 0
        # 如果break_count大于20，证明一个问题的获取以超出了20秒，那么此时放弃这个问题后续的用户获取
        break_count = 0
        question_id = question.split("/")[6]
        try:
            total_num = self.__get_total(question)
            for i in range(0, (total_num // self.__LIMIT) + 1):
                thread_pool.run(func=self.__get_uuid, args=(question, now, user_uuid_list, count_list))
                now = now + self.__LIMIT
            while True:
                spider_util.process_bar(len(count_list) / total_num,
                                        start_str=f"从问题{question_id}中获取{total_num}个回答，"
                                                  f"其中匿名回答数量：{len(count_list) - len(user_uuid_list)}，爬取百分比：",
                                        end_str="100%",
                                        total_length=50)
                if len(count_list) < total_num:
                    last_count = len(count_list)
                    time.sleep(1)
                    if last_count == len(count_list):
                        break_count += 1
                    else:
                        break_count = 0
                    if break_count >= 20:
                        print("\n该问题回答的获取时间卡了超过20秒，已放弃后续用户id获取")
                        break
                else:
                    break
            print(f"\n从该问题{question_id}中获取{len(user_uuid_list)}个用户id")
            print(user_uuid_list)
            thread_pool.close()
            return user_uuid_list
        except Exception as e:
            self.job_logger.error("用户回答获取失败,请带着以下报错去github原仓库提出issue")
            self.job_logger.exception(traceback.print_exc())
            print(e)

    # 获取当前问题所有回答数量
    def __get_total(self, question_url: str):
        json_result = proxy_pool.get(url=question_url,
                                     headers=self._header_with_zse_96(api_url=question_url),
                                     anonymity=True,
                                     retry_count=100).json()
        try:
            total_num = json_result['paging']['totals']
            self.sum_num += int(total_num)
            print(f"共从问题中获取用户数量：{self.sum_num}个")
            return total_num
        except Exception as e:
            self.job_logger.error("用户回答加载失败,请带着以下报错去github原仓库提出issue")
            self.job_logger.exception(traceback.print_exc())
            print(e)

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

    # 获取一个批次里面的所有用户的id，该方法主要配合多线程使用，提高一个问题的所有回答的获取速度
    def __get_uuid(self, question, now, user_uuid_list, count_list):
        datepat = re.compile(r'offset=\d+')
        base_url = question
        next_url = datepat.sub(r'offset={offset}'.format(offset=now), base_url)
        json_result = proxy_pool.get(next_url, headers=self._header_with_zse_96(api_url=next_url),
                                     anonymity=True).json()
        data = json_result["data"]
        for j in data:
            count_list.append(j['author']['id'])
            if not j['author']['id'] == "0":
                user_uuid_list.append(j['author']['id'])


if __name__ == '__main__':
    question_util = QuestionRequester()
    question_util.get_user_uuid()
    # question_util.parse_hot_list_and_save()
