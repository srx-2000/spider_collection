import pandas as pd
import numpy as np

df = pd.read_csv(
    r"D:\pycharm\PyCharm 2020.1.1\workplace\zhihu_user_info\zhihu_user_info_spider\result\userInfo\2021\10\17\user_info_low_cleaned.csv")
df1 = df.drop_duplicates(subset="id")

print(df1.groupby("所在行业").size())


# print(df1.pivot_table)

# print(df1["id"].value_counts())
