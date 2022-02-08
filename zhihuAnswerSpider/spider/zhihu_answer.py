import requests
import json
import re
import threading
import time
import os
import hashlib
import execjs
from spider.ProxyPool import Proxy_pool


# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
# }


class zhihu_answer():
    question_id = 0
    begin_id = 0

    similar_question_url_list = []
    copy_list = []
    question_count = 20
    proxy_pool = Proxy_pool()

    def __init__(self, begin_id, question_id, question_count=20):
        self.cookie = "_zap=08e23a53-f86c-42da-87dc-f8a3ec8e602c; d_c0=\"AGAfR6B3zBOPTrcvoCVTQZQ4_3FyaBPBQA8=|1632919082\"; _9755xjdesxxd_=32; _xsrf=HEMAC43R4Qg3ggLPWJTVJeh7sV3CL5le; __snaker__id=NHSlBQya6QYHKfFU; captcha_ticket_v2=\"2|1:0|10:1643873917|17:captcha_ticket_v2|704:eyJ2YWxpZGF0ZSI6IkNOMzFfeEFKLjJIcXhYX3dBUWlXY1d5Sl9RTDRJdTVwSGtmbXRrSkFtT1JOVVdId2RqYy1Uc1NJT2owcG5lRGZuMFAtVUFqUGhkMGxGei5kUzFLbzBNU0RSdUlzT1pvUExwYUhfdFUyYTd4a3JfR1hzS0tEa3FRSjl6V1J1bFB0US1TeFFmSkR6a0dxbVRqaTh6ZjA5RHVhYnJhaW9TRUhGRm44SU5VTURPUHNCRXFsNGQ1SnEtcFBPZzBDNndSeXlUTmtSX2lETm1jYW5CbEgtRzJrdFEweDJPak1lRGFLTXNyRGtELXdBNm5EbGxJekI4TS0ydlBwRTFXQTg1blR2VW9Ua3JYQ2FMY0JiaGt6OFJrOENpSmxycVoyendmTFNRU21xaTR4WmltMVRnaWJvdE9JbjhaOXpQN1VIbnhyMFNwMUNocnByRnlaNEM4SEJLLnJDR0xvODFucjFkbUpva1BlcTlua0dDdER0RGF2bk9iZzdvVTh0ZGdUR3Zodnp3eUNyam5DZ1RsWFd5R2g1ZTg0SUJHekVhSXF2UzV2UFMuX2RzV1NHSjQ5ZS1mUjZFMWhJcktneXlWMmprZ0NtcEJrWGhuNXh4RDFjQUlBNy0xaU5PcENQNm5wQ1FQREdmbDVnalJZckN0NG9vV2NIcE5Dc21RLTB0dWtTYXRhMyJ9|bf532e06e808d9f51dbdff04478f10a060602f2d2ab18faedd13805388af9a00\"; l_cap_id=\"NDA5NzIyY2QyZmE4NDRkZWFmZjJkZDEyN2EyYjk5MTE=|1644029109|863ceb14febd07bef73cfa00a7bb12ba399bb5a0\"; r_cap_id=\"OTE2NDRjODA2OGEyNDBlMmFmOWRkYjI0MzdkMzc5MDI=|1644029109|3fc559b64c99bbdee97d2c1f28adb644390d19a6\"; cap_id=\"ZjFiOWZjNGMyMTY1NDBhMzg1ZDI4M2FhZTBkNzU2NjQ=|1644029109|8d900be5cb787427387252d152ce0b11f5fbe425\"; YD00517437729195%3AWM_TID=P4hPS7HsHSREVBQEFQN6ufGCAUs2OOWy; YD00517437729195%3AWM_NI=mbUbGtgyf2tPGJTuoO80F%2B8SEiYmfNys75FHo85R%2Fj1qJzg9fYpQp%2FHFBlddZKzmx24ScnZqMOqmOzxti7%2B0o%2FyUGL%2F2e18j5S3jG1%2BW57O1ipS6%2Fukz2bygARVwgXKmTjY%3D; YD00517437729195%3AWM_NIKE=9ca17ae2e6ffcda170e2e6eeb9fb5bfbb9848af36898bc8fa3d84a828a8eafb67b8998a3abd979a88d8aa2c72af0fea7c3b92aafbe9b83c680a5a7aad3f75c85969c96ee45fcf08accbb5987b7978ee546bbadf9d6c544ade8fbb3ae62f3af869be633a687c0b2f3258c9a8e8de7709a95b68efb3af88dad8fd97b8f91bf8ece72bcaca7d8aa3cadf1b7b6c648edeeabd2bb62f78dfd8bc63be989fbd8ce3babb09dd7ae7fa9a6fe83fc6d838e9a98e65489b39c8bdc37e2a3; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1644039481,1644049935,1644116007,1644141996; SESSIONID=2jyFaheFXujkqsFYdYM9m6o8e6ENneWErq2KUFitQ2x; JOID=UFASB01tNQ826Coefmub14E_5X9vVVB1co1IdDsxSmpem11SKDaY8VHmLxJ_9r3iE0RIk0g9QsIBG5mc_zGsZrw=; osd=V1ERAkpqNAwz7y0ffW6c0IA84HhoVFNwdYpJdz42TWtdnlpVKTWd9lbnLBd48bzhFkNPkks4RcUAGJyb-DCvY7s=; gdxidpyhxdE=8KGdmno6oN5xwoyyI1oKnQo9Ln7g3MOMEIj4IcYNV8T%2FlajpNnjyP5VSx5HT%2BpUMUN0r9W709cD81mTcD%2FvBj31dWy%5C2C5yfWK%2BPfv1y4YgNBKlESmv4oaPyIgX1Z2LYTKBWjlQZR8koxv2TMEOo24g5feI5v1Zwn6qZkU3EhGR18y5R%3A1644144580079; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1644144043; captcha_session_v2=\"2|1:0|10:1644144043|18:captcha_session_v2|88:eDhBWnRQRTIxaXJvNTd2Wks1c25iYUNnU2tKWUptT3hBK0ZuTGZHRWt5Y0htdFZpQyt1ZzJKekpSeC9RVWZsaA==|1e9306153c8d3314afa4ad49ffbc5de16c51954d522efbd60a40591916951dc9\"; KLBRSID=5430ad6ccb1a51f38ac194049bce5dfe|1644144081|1644135071"
        self.begin_id = begin_id
        self.question_id = question_id
        self.question_count = question_count
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
            "cookie": self.cookie
        }

    def get_headers(self, api_url):
        star = 'd_c0='
        end = ';'
        cookie_mes = self.cookie[self.cookie.index(star):].replace(star, '')
        cookie_mes = cookie_mes[:cookie_mes.index(end)]
        parse_url = api_url.replace("https://www.zhihu.com", "")
        f = "+".join(["101_3_2.0", parse_url, cookie_mes])
        fmd5 = hashlib.new('md5', f.encode()).hexdigest()
        with open(os.path.dirname(__file__) + os.sep + 'g_encrypt.js', 'r', encoding="utf-8") as f:
            ctx1 = execjs.compile(f.read(), cwd=os.path.dirname(os.getcwd()) + os.sep + 'node_modules')
        encrypt_str = "2.0_%s" % ctx1.call('b', fmd5)
        self.header["x-app-za"] = 'OS=Web'
        self.header["x-zse-93"] = "101_3_2.0"
        self.header["x-zse-96"] = encrypt_str
        return self.header

    def get_answer(self, question_id, limit=1):
        now = 0
        total_num = self.get_total(question_id)
        content_list = []
        author_name_list = []
        author_id_list = []
        author_url_token_list = []
        dict = {}
        for i in range(0, total_num // limit):
            now = now + limit
            url = "https://www.zhihu.com/api/" \
                  "v4/questions/{question_id}/answers?include=data%5B*%5D." \
                  "is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_co" \
                  "llapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse" \
                  "_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_co" \
                  "unt%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvote" \
                  "up_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2C" \
                  "updated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Cis_labe" \
                  "led%2Cpaid_info%2Cpaid_info_content%2Crelationship.is_authorized%2Cis_author%" \
                  "2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_recognized%3Bdata%5B*%5D.mark_infos%5B*%5D" \
                  ".url%3Bdata%5B*%5D.author.follower_count%2Cbadge%5B*%5D.topics%3Bdata%5B*%5D.settings." \
                  "table_of_content.enabled&offset={now}&limit={limit}&sort_by=default&platform=desktop".format(
                question_id=str(question_id), limit=limit, now=now)
            response = self.proxy_pool.get(url, headers=self.get_headers(url), anonymity=False)
            json_result = json.loads(response.content)
            data = json_result["data"]
            print("爬取进度:" + str(round(i / (total_num // limit) * 100, 2)) + "%")
            for i in data:
                content_list.append(i["content"])
                author_name_list.append(i['author']['name'])
                author_id_list.append(i['author']['id'])
                author_url_token_list.append(i['author']['url_token'])
        dict["content_list"] = content_list
        dict["author_name_list"] = author_name_list
        dict["author_id_list"] = author_id_list
        dict["author_url_token_list"] = author_url_token_list
        return dict

    def get_total(self, question_id):
        url = "https://www.zhihu.com/api/" \
              "v4/questions/{question_id}/answers?include=data%5B*%5D." \
              "is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_co" \
              "llapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse" \
              "_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_co" \
              "unt%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvote" \
              "up_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2C" \
              "updated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Cis_labe" \
              "led%2Cpaid_info%2Cpaid_info_content%2Crelationship.is_authorized%2Cis_author%" \
              "2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_recognized%3Bdata%5B*%5D.mark_infos%5B*%5D" \
              ".url%3Bdata%5B*%5D.author.follower_count%2Cbadge%5B*%5D.topics%3Bdata%5B*%5D.settings." \
              "table_of_content.enabled&offset=&limit={limit}&sort_by=default&platform=desktop".format(
            question_id=str(question_id), limit=20)
        response = self.proxy_pool.get(url, headers=self.get_headers(url), anonymity=False)
        time.sleep(1)
        json_result = json.loads(response.content)
        next_json = json_result
        total_num = next_json['paging']['totals']
        return total_num

    def format_content(self, content_list):
        text_list = []
        pre = re.compile('>(.*?)<')
        for i in content_list:
            text = ''.join(pre.findall(i))
            text_list.append(text)
        return text_list

    def get_question_title(self, question_id):
        url = "https://www.zhihu.com/api/" \
              "v4/questions/{question_id}/answers?include=data%5B*%5D." \
              "is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_co" \
              "llapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse" \
              "_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_co" \
              "unt%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvote" \
              "up_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2C" \
              "updated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Cis_labe" \
              "led%2Cpaid_info%2Cpaid_info_content%2Crelationship.is_authorized%2Cis_author%" \
              "2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_recognized%3Bdata%5B*%5D.mark_infos%5B*%5D" \
              ".url%3Bdata%5B*%5D.author.follower_count%2Cbadge%5B*%5D.topics%3Bdata%5B*%5D.settings." \
              "table_of_content.enabled&offset=&limit={limit}&sort_by=default&platform=desktop".format(
            question_id=str(question_id), limit=20)
        # print(url)
        response = self.proxy_pool.get(url, headers=self.get_headers(url), anonymity=False)
        json_result = json.loads(response.content)
        data = json_result["data"]
        title = data[0]['question']['title']
        return title

    def single_answer(self, question_id):
        question_title = self.get_question_title(question_id)
        print("全部回答数量:" + str(self.get_total(question_id)))
        print("爬取的问题：" + question_title + "——问题id为：" + str(question_id))
        print("爬取ing.....请等待，等待时间依据回答数量而定")
        result_dict = self.get_answer(question_id, limit=20)

        # self.get_answer(question_id)
        text_list = self.format_content(result_dict['content_list'])
        try:
            with open(os.path.dirname(os.getcwd()) + "\\result\\" + question_title + ".txt", mode="w",
                      encoding='utf-8') as f:
                f.write("问题：" + question_title + "\n")
                f.write("问题id：" + str(question_id) + "\n\n")
                for i in range(0, len(text_list)):
                    f.write("回答者id：" + result_dict["author_id_list"][i] + "\n")
                    f.write("回答者空间地址：" + result_dict["author_url_token_list"][i] + "\n")
                    f.write("回答者昵称：" + result_dict["author_name_list"][i] + "\n")
                    f.write("回答的内容：" + text_list[i] + "\n\n")
            f.close()
        except:
            pass
        finally:
            print("爬取完成")

    def get_next_question(self, question):
        url = "https://www.zhihu.com/api/v4/questions/{question_id}/similar-questions?include=data%5B*%5D.answer_count%2Cauthor%2Cfollower_count&limit=5".format(
            question_id=question)
        # print(url)
        response = self.proxy_pool.get(url, headers=self.get_headers(url), anonymity=False)
        # print(response.text)
        json_result = json.loads(response.content)
        url_list = json_result['data']
        # with open("questions_id.txt", mode="a", encoding='utf-8') as f:
        for i in url_list:
            if not self.copy_list.__contains__(i['id']):
                self.similar_question_url_list.append(i['id'])
                self.copy_list.append(i['id'])
                # self.copy_list.append(i['id'])
                # f.write(str(i['id'])+"\n")
                print(i['id'])
                if len(self.copy_list) >= self.question_count:
                    return
                self.get_parse_question()
            # return self.similar_question_url_list
        # f.close()

    def get_parse_question(self):
        for i in self.similar_question_url_list:
            try:
                self.get_next_question(i)
                self.similar_question_url_list.remove(i)
            except:
                pass
            if len(self.copy_list) >= self.question_count:
                return

    def download_all_similar_question(self):
        threads = []
        # time.sleep(5)
        if len(self.copy_list) >= self.question_count:
            for i in self.copy_list:
                th = threading.Thread(target=self.single_answer, args=(i,))
                # print(th.name)
                th.start()
                threads.append(th)
            for th in threads:
                th.join()
        elif (len(self.copy_list) == 0):
            self.get_next_question(self.begin_id)
            self.download_all_similar_question()
        else:
            self.get_next_question(self.copy_list[len(self.copy_list) - 1])
            self.download_all_similar_question()


if __name__ == '__main__':
    model = input("请输入想要选取的模式:1.爬取单个问题  2.爬取相关问题\n")
    id = input("请输入想要爬取的问题的id，或相关问题的起点问题的id:\n")
    if int(model) == 1:
        zhihu = zhihu_answer(id, id)
        zhihu.single_answer(id)
    elif int(model) == 2:
        count = 20
        count = input("请输入想要爬取的相关问题的个数（默认为20，最大为400，知乎超过500会有反爬验证）:\n")
        zhihu = zhihu_answer(id, id, int(count))
        zhihu.download_all_similar_question()
    else:
        print("请输入规范数字1或2")
