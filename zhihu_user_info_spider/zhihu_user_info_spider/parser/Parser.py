from zhihu_user_info_spider.entities.UserEntity import UserEntityList
import parsel
import re
from zhihu_user_info_spider.Exception import SpiderException

user_entity = UserEntityList()


class Parser(object):
    '''该方法后续加入的is_add属性和database属性主要是为了迎合接口
    is_add 主要是用来区分是否要加入到csv中的，默认为True，
    database 主要是用来解析从数据库中读取的数据的，默认为False'''

    @staticmethod
    def user_info_parser(json: dict, is_add=True, database=False):
        single_user_info_dict = {}
        if database:
            single_user_info_dict["id2"] = json["id2"]
        else:
            single_user_info_dict["id2"] = json["id"]
        single_user_info_dict["url_token"] = json["url_token"]
        single_user_info_dict["name"] = json["name"]
        if json["gender"] == 1:
            single_user_info_dict["gender"] = "男"
        elif json["gender"] == 0:
            single_user_info_dict["gender"] = "女"
        else:
            single_user_info_dict["gender"] = "未知"
        single_user_info_dict["type"] = json["type"]
        single_user_info_dict["headline"] = json["headline"]
        single_user_info_dict["description"] = json["description"]
        single_user_info_dict["following_count"] = json["following_count"]
        single_user_info_dict["follower_count"] = json["follower_count"]
        single_user_info_dict["answer_count"] = json["answer_count"]
        single_user_info_dict["zvideo_count"] = json["zvideo_count"]
        single_user_info_dict["question_count"] = json["question_count"]
        single_user_info_dict["articles_count"] = json["articles_count"]
        single_user_info_dict["columns_count"] = json["columns_count"]
        single_user_info_dict["favorite_count"] = json["favorite_count"]
        single_user_info_dict["following_question_count"] = json["following_question_count"]
        single_user_info_dict["following_topic_count"] = json["following_topic_count"]
        single_user_info_dict["following_columns_count"] = json["following_columns_count"]
        single_user_info_dict["following_favlists_count"] = json["following_favlists_count"]
        location_list = json["location"]
        single_user_info_dict["location"] = []
        single_user_info_dict["voteup_count"] = json["voteup_count"]
        if database:
            single_user_info_dict["level"] = json["level"]
            single_user_info_dict["avatar_url"] = json["avatar_url"]
            single_user_info_dict["business"] = json["business"]
            if location_list == None:
                single_user_info_dict["location"] = []
            else:
                for item in location_list:
                    single_user_info_dict["location"].append(item)
        else:
            single_user_info_dict["level"] = json["level_info"]["level"]
            single_user_info_dict["avatar_url"] = json["avatar_url_template"]
            single_user_info_dict["business"] = json["business"]['name']
            if location_list == None:
                single_user_info_dict["location"] = []
            else:
                for item in location_list:
                    single_user_info_dict["location"].append(item["name"])
        if is_add:
            user_entity.add_user(single_user_info_dict)
        else:
            return single_user_info_dict

    @staticmethod
    def hot_question_list_parser(response_text: str):
        if response_text != None and response_text != "":
            url_list = parsel.Selector(response_text).xpath("//div[@class='HotItem-content']/a/@href").getall()
            i = 0
            n = 0
            while i < len(url_list) - n:
                if not url_list[i].__contains__("question"):
                    url_list.pop(i)
                    n = n + 1
                i = i + 1
            if len(url_list) == 0:
                print("接收到的hot文档已失效，请及时更换cookie")
                raise SpiderException("接收到的hot文档已失效，请及时更换cookie")
            else:
                id_list = []
                for i in url_list:
                    id_list.append(i.split("/")[-1])
                return id_list
        else:
            print("请输入正确的hot文档")
            raise SpiderException("请输入正确的hot文档")


if __name__ == '__main__':
    print()
