import os

# t_l = [(1, 2, 3,), (1, 2, 3,), (1, 2, 3,), (1, 2, 3,)]
#
# for i, j, k in t_l:
#     print("i:" + str(i))
#     print("j:" + str(j))
#     print("k:" + str(k))


path = r"D:\pycharm\PyCharm 2020.1.1\workplace\zhihu_user_info_spider\zhihu_user_info\result"

for root, dirs, files in os.walk(path):
    for f in files:
        with open(os.path.join(root, f), mode="r", encoding="utf-8") as f_r:
            for i in f_r.readlines():
                print(i.strip("\n"))
