from data_analysis.analysis.DataAnalysis import DataAnalysis

'''该类主要用来分析所有二元组关系'''


class BinaryPivotTable(DataAnalysis):
    def __init__(self, is_month=False):
        DataAnalysis.__init__(self=self, is_month=is_month)

    '''is_low属性主要是用来区分到底使用高质量清洗结果还是使用低质量清洗结果的'''
    '''该方法主要用来生成所有二元的透视表'''

    def get_binary_pivot_table(self):
        param_df = self._cleaner_location()
        for i in range(0, len(self.binary_pivot_column1)):
            param_list = [self.binary_pivot_column1[i], self.binary_pivot_column2[i]]
            self._comprehensive_pivot_table(index=param_list, group_by=param_list, rename="num",
                                            filename=self.binary_pivot_column1[i] + "-" + self.binary_pivot_column2[
                                                i] + ".csv", param_df=param_df)
            print(self.binary_pivot_column1[i] + "-" + self.binary_pivot_column2[i] + ".csv 已完成")
        print("*" * 50 + "所有二元表数据已处理完毕，请到相应的月份或天数的文件夹中获取" + "*" * 50)


if __name__ == '__main__':
    bt = BinaryPivotTable(is_month=False)
    bt.get_binary_pivot_table()
