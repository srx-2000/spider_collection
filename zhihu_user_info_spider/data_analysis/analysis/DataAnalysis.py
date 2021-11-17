from data_analysis.util.SaveUtil import SaveUtil
from data_analysis.util.ConfigLoader import ConfigLoader
import pandas as pd

save_util = SaveUtil()
config_loader = ConfigLoader()


# 所有分析类的父类，主要用来初始化需要分析的数据df，以及给出通用的分析方法
class DataAnalysis(object):

    def __init__(self, is_month=False):
        self.is_month = is_month
        # 读取配置文件中的路径
        self.path_dict = config_loader.get_data_path_dict()
        # 如果是按月读取数据那么必定是低质量数据，而且这个低质量数据是连去重都没有做的那种低质量数据，
        # 主要是因为需要全部用户数据去做一个用户活跃榜，所以这里的数据是直接从数据库中读取并不去重的
        if is_month:
            self.base_low_df = save_util.restore_df(save_util.MONTHLY, save_util.LOW)
        else:
            self.base_high_df = save_util.restore_df(save_util.DAILY, save_util.HIGH)
            self.base_low_df = save_util.restore_df(save_util.DAILY, save_util.LOW)
        self.province_dict = config_loader.get_province_dict()
        self.binary_pivot_column1 = []
        self.binary_pivot_column2 = []
        self.one_pivot_column = config_loader.get_single_list()
        for i in config_loader.get_binary_list():
            middle_list = i.split("-")
            self.binary_pivot_column1.append(middle_list[0])
            self.binary_pivot_column2.append(middle_list[1])

    def _group_size(self, column_name: str, rename: str, file_name: str, limit=0, asc=False,
                    param_df: pd.DataFrame = None):
        file_path = config_loader.get_result_path(mode=self.path_dict["single"], is_month=self.is_month)
        if limit == 0:
            result_df = param_df.groupby(column_name).size().sort_values(ascending=asc).to_frame(
                rename).reset_index()
        else:
            result_df = param_df.groupby(column_name).size().sort_values(ascending=asc).to_frame(
                rename).reset_index().head(limit)
        save_util.save_result(mode=save_util.SELF, file_name=file_name, data=result_df, file_path=file_path)

    # 生成二维表的主要方法
    def _comprehensive_pivot_table(self, index: list, group_by: list, rename: str, filename: str,
                                   param_df: pd.DataFrame = None):
        file_path = config_loader.get_result_path(mode=self.path_dict["binary"], is_month=self.is_month)
        index_list = ["id2"]
        index_list.extend(index)
        df = pd.pivot_table(param_df, index=index_list).groupby(group_by).size().to_frame(rename)
        save_util.save_result(mode=save_util.SELF, file_name=filename, data=df, file_path=file_path)

    def _save_list(self, filename: str, df: pd.DataFrame):
        file_path = config_loader.get_result_path(mode=self.path_dict["list"], is_month=self.is_month)
        save_util.save_result(mode=save_util.SELF, file_name=filename, data=df, file_path=file_path)

    # 该方法用来处理位置信息，因为原数据中存储的位置信息虽然形式上是列表但本质上是字符串，而该方法主要的所用就是将原来的字符串转为真正的list,并未后面做透视表进行列处理。
    def _deal_location(self, is_low=True):
        if is_low:
            self.base_low_df.columns = ["id2", "url_token", "name", "gender", "level", "avatar_url", "type",
                                        "headline", "description", "business", "following_count", "follower_count",
                                        "answer_count", "zvideo_count",
                                        "question_count", "articles_count", "columns_count", "favorite_count",
                                        "following_question_count",
                                        "following_topic_count", "following_columns_count", "following_favlists_count",
                                        "location", "voteup_count"]
            user_list = self.base_low_df.to_dict(orient="records")
        else:
            self.base_high_df.columns = ["id2", "url_token", "name", "gender", "level", "avatar_url", "type",
                                         "headline", "description", "business", "following_count", "follower_count",
                                         "answer_count", "zvideo_count",
                                         "question_count", "articles_count", "columns_count", "favorite_count",
                                         "following_question_count",
                                         "following_topic_count", "following_columns_count", "following_favlists_count",
                                         "location", "voteup_count"]
            user_list = self.base_high_df.to_dict(orient="records")
        for dict_item in user_list:
            for j in dict_item:
                if j == "location":
                    set_list = list(set(dict_item[j].split("'")))
                    if set_list.__contains__(", "):
                        set_list.remove(", ")
                    if set_list.__contains__("]"):
                        set_list.remove("]")
                    if set_list.__contains__("["):
                        set_list.remove("[")
                    if set_list.__contains__("[]"):
                        set_list.remove("[]")
                    dict_item[j] = set_list
        new_list = []
        for i in user_list:
            if not len(i["location"]) == 0:
                for j in i["location"]:
                    # 这里使用浅复制，否则会导致元数据和新数据同时更改
                    new_dict = i.copy()
                    new_dict["location"] = j
                    new_list.append(new_dict)
            else:
                i["location"] = "未知"
                new_list.append(i)
        return pd.DataFrame(new_list)

    '''该方法是基于上面的地点分类之后的地点清洗
   因为爬虫从知乎上爬取的数据的地址都是字符串，而字符串是没法使用pandas的透视表的
   所以'''

    def _cleaner_location(self) -> pd.DataFrame:
        df = self._deal_location()
        data_dict_list = df.to_dict(orient="records")
        province_keys = list(self.province_dict.keys())
        print("处理地点数据ing.........")
        for j in data_dict_list:
            for i in range(0, len(province_keys)):
                if str(province_keys[i]).__contains__(j["location"]) or str(j["location"]).__contains__(
                        province_keys[i]):
                    j["location"] = province_keys[i]
                    break
                else:
                    continue
            if i == (len(province_keys) - 1):
                j["location"] = "海外地区"
        print("地点数据处理完毕~")
        return pd.DataFrame(data_dict_list)


if __name__ == '__main__':
    d_a = DataAnalysis(is_month=True)
    print(d_a._cleaner_location()["location"])
