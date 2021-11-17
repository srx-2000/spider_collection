import pandas as pd
import os
# import time
from data_analysis.util.Util import Util


class SaveUtil(Util):
    # 存储以及恢复数据的时间频率
    MONTHLY = 1
    DAILY = 2
    # 该存储模式的意思是，由用户自己指定存储路径，上面MONTHLY和DAILY模式都是由系统指定的
    # 由用户指定的模式主要用在保存不同分析结果，由于分析结果的类型可以由config.json中配置
    # 所以为了保证系统的灵活性，这里就不直接使用if判断写死在系统中了
    SELF = 3

    # 恢复数据的类型
    CLEAN = 11
    LOW = 12
    HIGH = 13

    def __init__(self):
        super().__init__()

    def save_result(self, mode: int, file_name: str, data: pd.DataFrame, file_path: str = None):
        if mode == self.SELF and (not file_path == None):
            flag = os.path.exists(file_path)
            if not flag:
                os.makedirs(file_path)
            data.to_csv(file_path + file_name, encoding='utf_8_sig')
        elif mode == self.MONTHLY:
            flag = os.path.exists(self.monthly_result_path)
            if not flag:
                os.makedirs(self.monthly_result_path)
            data.to_csv(self.monthly_result_path + file_name, encoding='utf_8_sig')
        elif mode == self.DAILY:
            flag = os.path.exists(self.daily_result_path)
            if not flag:
                os.makedirs(self.daily_result_path)
            data.to_csv(self.daily_result_path + file_name, encoding='utf_8_sig')

    def restore_df(self, mode: int, data_type: int):
        df = pd.DataFrame
        if mode == self.MONTHLY:
            file_path = self.spider_monthly_result_path + "user_info-" + self.year + "-" + self.month + ".csv"
            if not os.path.exists(file_path):
                print("not found monthly data")
            else:
                df = pd.read_csv(file_path)
        elif mode == self.DAILY:
            if data_type == self.CLEAN:
                df = pd.read_csv(
                    self.spider_daily_result_path + "user_info-" + self.year + "-" + self.month + "-" + self.day + ".csv")
            elif data_type == self.LOW:
                df = pd.read_csv(
                    self.spider_daily_result_path + "user_info_low_cleaned.csv")
            elif data_type == self.HIGH:
                df = pd.read_csv(
                    self.spider_daily_result_path + "user_info_high_cleaned.csv")
        return df


if __name__ == '__main__':
    s_u = SaveUtil()
    # print()
