import os
import json
import time


# 工具类父类
class Util(object):
    json_result = {}

    def __init__(self):
        self.abs_path = os.path.dirname(os.path.abspath(__file__)) + os.sep
        f = open(self.abs_path + "util_content.json", mode="r", encoding="utf-8")
        self.json_result = json.load(f)
        self.year = time.strftime("%Y", time.localtime())
        self.month = time.strftime("%m", time.localtime())
        self.day = time.strftime("%d", time.localtime())

    def update_date(self):
        self.year = time.strftime("%Y", time.localtime())
        self.month = time.strftime("%m", time.localtime())
        self.day = time.strftime("%d", time.localtime())