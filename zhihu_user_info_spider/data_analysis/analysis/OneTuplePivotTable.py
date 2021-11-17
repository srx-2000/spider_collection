from data_analysis.analysis.DataAnalysis import DataAnalysis
from data_analysis.util.SaveUtil import SaveUtil
from data_analysis.util.ConfigLoader import ConfigLoader

'''该类主要用来生成所有一元组的分析表'''
save_util = SaveUtil()
config_loader = ConfigLoader()


class OneTuplePivotTable(DataAnalysis):
    def __init__(self, is_month=False):
        DataAnalysis.__init__(self=self, is_month=is_month)

    def get_one_tuple_pivot_table(self):
        param_df = self._cleaner_location()
        for i in range(0, len(self.one_pivot_column)):
            self._group_size(column_name=self.one_pivot_column[i], rename="num",
                             file_name=self.one_pivot_column[i] + ".csv", limit=0, asc=False, param_df=param_df)
            print(self.one_pivot_column[i] + ".csv 已完成")
        print("*" * 50 + "所有一元表数据已处理完毕，请到相应的月份或天数的文件夹中获取" + "*" * 50)


if __name__ == '__main__':
    otpt = OneTuplePivotTable(is_month=False)
    otpt.get_one_tuple_pivot_table()
