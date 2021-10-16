# from zhihu_user_info.util.SpiderUtil import SpiderUtil
from zhihu_user_info.util.SaveUtil import SaveUtil
# from zhihu_user_info.util.Utils import Util
from zhihu_user_info.threadpool.ThreadPool import ThreadPool
import threading

# spider_util = SpiderUtil()
# save_util = SaveUtil()
#
# result_list = [1, 2, 3]
# save_util.middle_save(save_util.question_list_model, result_list)
#
# # with open(r"D:\pycharm\PyCharm 2020.1.1\workplace\taobao\zhihu_user_info\result\hot_list-2021-10-05.txt",
# #           mode="w", encoding="utf-8") as f_w:
# #     f_w.write("111")
# # f_w.close()
#
# list1 = [1, 2, 3]
# for i in range(0, len(list1)):
#     print(list1[i])
# str='https://www.zhihu.com/special/1421924027711156224'
# print(str.__contains__("question"))

save_util = SaveUtil()
thread_pool = ThreadPool(20)


class test():

    def __init__(self):
        self.lock = threading.RLock()

    def get(self, name, i):
        print(name + "：" + str(i))
        return 1

    # def get3(name, i):
    #     print("new get3："+name + "：" + str(i))
    #     return 1

    def get1(self):
        for i in range(0, 100):
            thread_pool.run(func=self.get, args=("get1", i,), callback=self.get1_callback)
        # thread_pool.close()
    #
    # def lock_test(self):
    #     self.lock.acquire()
    #     try:
    #

    def get1_callback(self, status, result):
        if status:
            # get2(num=result)
            # print(11111111111111111111111111111111111111111111)
            print("call_back：" + str(status) + "\n")
            print("call_back_result：" + str(result) + "\n")
        # return result

    # def get2(num):
    #     for i in range(0, 100):
    #         thread_pool.run(func=get3, args=("get2", i,))
    #     print("new get2"+str(num+1))
    #     close()
    # thread_pool.close()

    def close(self):
        thread_pool.close()

    def save(self, i):
        test_dict = {"thread": i, "thread": i, "thread": i, "thread": i, "thread": i, "thread": i,
                     "thread": i, "thread": i, "thread": i}
        save_util.save(test_dict)
        print(i)

    def debug_callback(self, status, result):
        print(status)
        print(result)


if __name__ == '__main__':
    t = test()
    for i in range(0, 1000):
        pass
        # t.save(str(i))
        # thread_pool.run(func=t.save, args=(i,))
    # thread_pool.close()
    # t.get1()
    # # get2()
    # t.close()
