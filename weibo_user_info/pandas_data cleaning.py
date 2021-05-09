import pandas as pd
import numpy as np

df=pd.read_csv("微博粉丝信息.csv")
# print(df)
list=["index","关注数","粉丝数","vip等级","阳光信用","点赞数","评论数","转发数","注册时间",'微博总数',"用户名称","微博认证"]
df=df.dropna(how="any")
print(df)
df1=df.drop_duplicates(inplace=False)
df1.columns=list
del df1["index"]
df1.to_csv("微博粉丝信息（数据清洗后）.csv",encoding='utf_8_sig',index=None)







