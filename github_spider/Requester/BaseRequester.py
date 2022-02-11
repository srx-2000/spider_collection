from github_spider.util.util import Util
import time
import threading
import os

util = Util()


class BaseRequester:
    def __init__(self):
        base_path = os.path.dirname(os.path.dirname(__file__)) + os.sep + "util" + os.sep
        self.limit_path = base_path + "limit_count.txt"
        self.time_path = base_path + "start_time.txt"
        self.limit_count = 0
        last_time = self.__read_time()
        self.start_time = time.time()
        if (last_time - self.start_time) >= 3600:
            self.__write_limit_count()
        self.__write_time()
        # 声明一个线程锁
        self.lock = threading.RLock()

    def _random_header(self):
        headers = {
            "user-agent": util.get_user_agent(),
            "Authorization": "token " + util.get_api_token()
        }
        return headers

    # 下面三个方法的主要作用就是检测一小时之内是否以达到5000次的访问上限
    def __add_limit_times(self):
        limit_count = self.__read_limit_count()
        self.limit_count = limit_count + 1
        self.__write_limit_count()

    def __test_time(self):
        now_time = time.time()
        start_time = self.__read_time()
        during_time = now_time - start_time
        if during_time > 3600:
            self.start_time = now_time
            self.__write_time()
            self.limit_count = 0
            self.__write_limit_count()
        else:
            timeArray = time.localtime(now_time)
            date = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            print(f"\r{date} — INFO: 由于爬取已经超过一小时5000次的请求上限，需要睡眠{((3600 - during_time) // 60) + 1}分钟", end="",
                  flush=True)
            time.sleep(3600 - during_time)

    def _test(self):
        self.lock.acquire()
        self.__add_limit_times()
        limit_count = self.__read_limit_count()
        if limit_count >= 4999:
            self.__test_time()
        self.lock.release()

    # 该方法是提供给子方法用来判断请求是否超标了的
    def _get_limit_count(self):
        return self.__read_limit_count()

    def __read_time(self):
        with open(self.time_path, mode="r", encoding="utf-8") as f:
            try:
                start_time = float(f.read())
            except Exception:
                start_time = time.time()
        f.close()
        return start_time

    def __read_limit_count(self):
        with open(self.limit_path, mode="r", encoding="utf-8") as f:
            try:
                limit_count = int(f.read())
            except Exception:
                limit_count = 0
        f.close()
        return limit_count

    def __write_time(self):
        with open(self.time_path, mode="w", encoding="utf-8") as f:
            f.write(str(self.start_time))
        f.close()

    def __write_limit_count(self):
        with open(self.limit_path, mode="w", encoding="utf-8") as f:
            f.write(str(self.limit_count))
        f.close()
