import os
import time
import json


class Util(object):
    def __init__(self):
        self.year = time.strftime("%Y", time.localtime())
        self.month = time.strftime("%m", time.localtime())
        self.day = time.strftime("%d", time.localtime())
        self.abs_path = os.path.dirname(os.path.abspath(__file__)) + os.sep
        f = open(self.abs_path + "config.json", mode="r", encoding="utf-8")
        self.json_result = json.load(f)
        self.path = os.path.dirname(os.path.dirname(self.abs_path)) + os.sep + "result" + os.sep
        # 每月统计的数据分析结果保存路径
        self.monthly_result_path = self.path + self.year + os.sep + self.month + os.sep
        # 每日统计的数据分析结果保存路径
        self.daily_result_path = self.path + self.year + os.sep + self.month + os.sep + self.day + os.sep
        # 从爬虫中获取数据的路径
        self.spider_result_path = os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    self.abs_path))) + os.sep + "zhihu_user_info_spider" + os.sep + "result" + os.sep + "userInfo"
        self.spider_daily_result_path = self.spider_result_path + os.sep + self.year + os.sep + self.month + os.sep + self.day + os.sep
        self.spider_monthly_result_path = self.spider_result_path + os.sep + self.year + os.sep + self.month + os.sep
