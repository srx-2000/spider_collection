from data_analysis.analysis.DataAnalysis import DataAnalysis
from data_analysis.util.SaveUtil import SaveUtil
from data_analysis.util.ConfigLoader import ConfigLoader
import pandas as pd

'''该类主要用来生成所有一元组的分析表'''
save_util = SaveUtil()
config_loader = ConfigLoader()


class RankingList(DataAnalysis):
    def __init__(self, is_month=False):
        DataAnalysis.__init__(self=self, is_month=is_month)
        data = DataAnalysis(is_month=is_month)
        df = data._cleaner_location()
        self.dict_list = df.to_dict(orient="records")

    def get_hot_list(self):
        hot_list = []
        filter_list = self._filter("hot_list", data=self.dict_list)
        for i in filter_list:
            hot_list_dict = {}
            quality = self._get_quality(i["answer_count"], i["voteup_count"])
            product = self._get_product(i["answer_count"], i["zvideo_count"], i["articles_count"], i["columns_count"])
            value = self._get_eval("hot_list", i["follower_count"], product, i["voteup_count"], quality)
            hot_list_dict["id2"] = i["id2"]
            hot_list_dict["value"] = value
            hot_list.append(hot_list_dict)
        df = pd.DataFrame(hot_list)
        df1 = df.sort_values(by="value", ascending=False).head(20)
        hot_list = df1.to_dict(orient="records")
        self._save_list("hot_list.csv", df1)
        print("热门排行榜分析完毕")
        return hot_list

    def get_water_list(self):
        water_list = []
        filter_list = self._filter("water_list", data=self.dict_list)
        for i in filter_list:
            hot_list_dict = {}
            quality = self._get_quality(i["answer_count"], i["voteup_count"])
            value = self._get_eval("water_list", quality=quality, answer_count=i["answer_count"])
            hot_list_dict["id2"] = i["id2"]
            hot_list_dict["value"] = value
            water_list.append(hot_list_dict)
        df = pd.DataFrame(water_list)
        df1 = df.sort_values(by="value", ascending=False).head(20)
        water_list = df1.to_dict(orient="records")
        self._save_list("water_list.csv", df1)
        print("水逼排行榜分析完毕")
        return water_list

    def get_new_list(self):
        new_list = []
        filter_list = self._filter_new(data=self.dict_list)
        for i in filter_list:
            hot_list_dict = {}
            quality = self._get_quality(i["answer_count"], i["voteup_count"])
            value = self._get_eval("new_list", answer_count=i["answer_count"], voteup_count=i["voteup_count"],
                                   quality=quality)
            hot_list_dict["id2"] = i["id2"]
            hot_list_dict["value"] = value
            new_list.append(hot_list_dict)
        df = pd.DataFrame(new_list)
        df1 = df.sort_values(by="value", ascending=False).head(20)
        new_list = df1.to_dict(orient="records")
        self._save_list("new_list.csv", df1)
        print("新人排行榜分析完毕")
        return new_list

    def get_quality_list(self):
        quality_list = []
        filter_list = self._filter("quality_list", data=self.dict_list)
        for i in filter_list:
            hot_list_dict = {}
            quality = self._get_quality(i["answer_count"], i["voteup_count"])
            value = self._get_eval("quality_list", quality=quality)
            hot_list_dict["id2"] = i["id2"]
            hot_list_dict["value"] = value
            quality_list.append(hot_list_dict)
        df = pd.DataFrame(quality_list)
        df1 = df.sort_values(by="value", ascending=False).head(20)
        quality_list = df1.to_dict(orient="records")
        self._save_list("quality_list.csv", df1)
        print("质量排行榜分析完毕")
        return quality_list

    def _get_quality(self, answer_count: int, voteup_count: int):
        return round(voteup_count / answer_count, 2)

    def _get_product(self, answer_count: int, zvideo_count: int, articles_count: int, columns_count: int):
        return zvideo_count + answer_count + articles_count + columns_count

    # 通过传入的公式获取相应榜单的值
    def _get_eval(self, formula_type: str, follower_count=0, product_count=0, voteup_count=0, quality=0.0,
                  answer_count=0):
        formula_dict = config_loader.get_algorithm_formula()
        result = eval(formula_dict[formula_type].format(follower_count=follower_count,
                                                        product_count=product_count,
                                                        voteup_count=voteup_count,
                                                        quality=quality,
                                                        answer_count=answer_count))
        return round(result, 2)

    # 用户排行榜入榜筛选器
    def _filter(self, scope_type: str, data: list):
        result_list = []
        new_list = []
        scope = config_loader.get_algorithm_scope()[scope_type]
        for i in data:
            for j in scope.keys():
                if not j == "quality":
                    if i[j] >= scope[j]:
                        result_list.append(i)
        for i in result_list:
            quality = round(i["voteup_count"] / i["answer_count"], 2)
            if scope["quality"][0] <= quality <= scope["quality"][1]:
                new_list.append(i)
        df = pd.DataFrame(new_list).drop_duplicates(subset="id2", keep="first", inplace=False)
        new_list = df.to_dict(orient="records")
        return new_list

    # 新人榜比较特殊，所以单列出来
    def _filter_new(self, data: list):
        result_list = []
        new_list = []
        scope = config_loader.get_algorithm_scope()["new_list"]
        for i in data:
            for j in scope.keys():
                if not j == "quality":
                    if j == "voteup_count":
                        if i[j] >= scope[j]:
                            result_list.append(i)
                    else:
                        if i[j] <= scope[j]:
                            result_list.append(i)
        for i in result_list:
            quality = round(i["voteup_count"] / i["answer_count"], 2)
            if scope["quality"][0] <= quality <= scope["quality"][1]:
                new_list.append(i)
        df = pd.DataFrame(new_list).drop_duplicates(subset="id2", keep="first", inplace=False)
        new_list = df.to_dict(orient="records")
        return new_list


if __name__ == '__main__':
    rl = RankingList()
    rl.get_hot_list()
    rl.get_quality_list()
    rl.get_water_list()
    rl.get_new_list()
