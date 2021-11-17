from data_analysis.util.SaveUtil import SaveUtil
import os

save_util = SaveUtil()


# 数据的清洗频率是每天一次，确保每天进入数据库的用户数据是唯一的，
# 但如果以月为单位从数据库中读取的数据用户数据就不用保证唯一性了。
# 如果一个用户在这一个月之内频繁出现在数据库中，那么仅有一种可能就是
# 该用户在这一个月内多次回答了热榜问题，这无非反映了用户的活跃性，
# 是一种良性的重复，可以利用做活跃榜
class PandasCleanser(object):
    def __init__(self):
        self.df_clean = save_util.restore_df(save_util.DAILY,save_util.CLEAN)
        self.index_list = ["index", "id", "用户token", "用户昵称", "用户性别", "用户等级", "用户头像url", "用户类型", "用户头文字", "个人简介", '所在行业',
                           "关注数", "粉丝数", "回答数量", "视频数", "提问数量", "文章数", "专栏数", "收藏数", "关注的问题数量", "关注的话题数量", "关注的专栏数量",
                           "关注的文件夹数量", "居住地", "被赞同次数"]

    # 高质量数据清洗【清洗过后数据中除所在地以外任意一项均有实际值,所以可能导致数据量骤减，没有特殊需求谨慎使用】
    def high_clean(self):
        df_clean = self.df_clean.dropna(how="any")
        df1 = df_clean.drop_duplicates(subset="id", keep="first", inplace=False)
        df1.columns = self.index_list
        del df1["index"]
        df1.to_csv(save_util.spider_daily_result_path + os.sep + "user_info_high_cleaned.csv", encoding='utf_8_sig',
                   index=None)
        print("人类高质量数据以清洗完毕")

    # 低质量数据清洗【仅以id为索引去重】
    def low_clean(self):
        # df_clean = self.df_clean.dropna(how="any")
        df1 = self.df_clean.drop_duplicates(subset="id", keep="first", inplace=False)
        df1.columns = self.index_list
        del df1["index"]
        df1.to_csv(save_util.spider_daily_result_path + os.sep + "user_info_low_cleaned.csv", encoding='utf_8_sig',
                   index=None)
        print("人类低质量数据以清洗完毕(大雾)")


if __name__ == '__main__':
    cleanser = PandasCleanser()
    cleanser.low_clean()
    cleanser.high_clean()
