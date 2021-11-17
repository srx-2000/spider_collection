from data_analysis.util.Util import Util
import os


class ConfigLoader(Util):

    def __init__(self):
        super().__init__()

    def get_province_dict(self):
        if "province" in self.json_result:
            province_dict = self.json_result["province"]
            return province_dict
        else:
            print("config.json中配置province。")

    def get_binary_list(self):
        if "binary" in self.json_result:
            binary_list = self.json_result["binary"]
            return binary_list
        else:
            print("config.json中配置binary。")

    def get_single_list(self):
        if "single" in self.json_result:
            single_list = self.json_result["single"]
            return single_list
        else:
            print("config.json中配置single。")

    def get_data_path_dict(self) -> dict:
        if "data_type_path" in self.json_result:
            if self.json_result["data_type_path"].keys().__contains__("//"):
                # 去除注释
                del self.json_result["data_type_path"]["//"]
            data_path_dict = self.json_result["data_type_path"]
            return data_path_dict
        else:
            print("config.json中配置data_type_path。")

    # mode 参数是由用户提供的，具体要什么路径，is_month参数是由用户提供的，具体是要保存到月文件夹里还是日文件夹里
    def get_result_path(self, mode: int, is_month=False) -> str:
        data_path_dict = self.get_data_path_dict()
        if is_month:
            for key in data_path_dict.keys():
                if mode == data_path_dict[key]:
                    return self.monthly_result_path + key + os.sep
        else:
            for key in data_path_dict.keys():
                if mode == data_path_dict[key]:
                    return self.daily_result_path + key + os.sep

    # 获取算法公式
    def get_algorithm_formula(self):
        if "algorithm_formula" in self.json_result:
            if self.json_result["algorithm_formula"].keys().__contains__("//"):
                # 去除注释
                del self.json_result["algorithm_formula"]["//"]
            data_path_dict = self.json_result["algorithm_formula"]
            return data_path_dict
        else:
            print("config.json中配置algorithm_formula。")

    # 获取算法入选范围
    def get_algorithm_scope(self):
        if "algorithm_scope" in self.json_result:
            if self.json_result["algorithm_scope"].keys().__contains__("//"):
                # 去除注释
                del self.json_result["algorithm_scope"]["//"]
            data_path_dict = self.json_result["algorithm_scope"]
            return data_path_dict
        else:
            print("config.json中配置algorithm_scope。")


if __name__ == '__main__':
    config = ConfigLoader()
    c2 = config.get_algorithm_scope()
    c1 = config.get_algorithm_formula()
    print(c1)
    print(c2)
