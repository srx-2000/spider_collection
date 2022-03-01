import requests
import json
import re
import threading
import time
import os
import hashlib
import execjs
from spider.ProxyPool import Proxy_pool


class zhihu_answer():
    question_id = 0
    begin_id = 0

    similar_question_url_list = []
    copy_list = []
    question_count = 20
    proxy_pool = Proxy_pool()

    def __init__(self, begin_id, question_id, question_count=20):
        self.cookie = '__snaker__id=uAXhRx1DirdxlNk6; SESSIONID=GwgRUxK1Ljbjy7hbQUmfbDnwRgTQ9XfXDHQBTwQSD5q; osd=UlkTBkse_gCrcKIRBBtf2xSgbn8Wdr43xhH1b05bqzDcFNVFRLhmG8xxpBUCWR5APhRy5uRb-bc5cFHWjXamOuI=; JOID=W18WC0wX-AWmd6sXARZY0hKlY3gfcLs6wRjzakNcojbZGdJMQr1rHMV3oRgFUBhFMxN74OFW_r4_dVzRhHCjN-U=; _zap=08e23a53-f86c-42da-87dc-f8a3ec8e602c; d_c0="AGAfR6B3zBOPTrcvoCVTQZQ4_3FyaBPBQA8=|1632919082"; _9755xjdesxxd_=32; _xsrf=HEMAC43R4Qg3ggLPWJTVJeh7sV3CL5le; __snaker__id=NHSlBQya6QYHKfFU; l_cap_id="NDA5NzIyY2QyZmE4NDRkZWFmZjJkZDEyN2EyYjk5MTE=|1644029109|863ceb14febd07bef73cfa00a7bb12ba399bb5a0"; r_cap_id="OTE2NDRjODA2OGEyNDBlMmFmOWRkYjI0MzdkMzc5MDI=|1644029109|3fc559b64c99bbdee97d2c1f28adb644390d19a6"; cap_id="ZjFiOWZjNGMyMTY1NDBhMzg1ZDI4M2FhZTBkNzU2NjQ=|1644029109|8d900be5cb787427387252d152ce0b11f5fbe425"; YD00517437729195:WM_TID=P4hPS7HsHSREVBQEFQN6ufGCAUs2OOWy; YD00517437729195:WM_NI=kCNXPfteYhbaNYXSYN7HFKYdlNzADKMT5TpD0kH0x6qSeTzV0mJMQWbjnp96EG+pKS40Wyvet2XuwDsNJhU/4gm/LVU/6obWfzFc5tO4QDJo44Nhgxtc27LESpfBKeGEeHU=; YD00517437729195:WM_NIKE=9ca17ae2e6ffcda170e2e6eeb8f13b85e9aeb5b770a38a8ab3c84b928e8faaf47facbefa8ae650e99787d3e62af0fea7c3b92aa99d82b9d36eb8bb9789e16b8e8798b4dc46f5988aacdc70b092b6a2c7418f8cfbb5f350f4b588d1fb3eb38dabb5f95ef4b386aed45da2b6a291bc3e8799e591ca59f8f0999af56fb8ee9896f650b1928689d825f8b9a3d0cf5e97f1fa90e15da6a68a84b8808dec9fa5c965f8ec8289e674b8bdfed8cf4f91b0aaa3ca6f859baba9d837e2a3; capsion_ticket="2|1:0|10:1645520619|14:capsion_ticket|44:Y2U3YTY3YzY0ZDVmNDAzOTg0MmU5NDZmMjRjYjdlYWI=|87bdeb092deb148164179838e456aebfe2f5349fe0da226067aa83dfa1f5f0a5"; captcha_ticket_v2="2|1:0|10:1645520632|17:captcha_ticket_v2|704:eyJ2YWxpZGF0ZSI6IkNOMzFfQTVQR0ZKZjZDQ0ZJVjJQUzBlbzk1emF0YnJrN2trLi1tbThUU2l6ZDFJWGF5ZzBSdC5vZlJGeWRaaDVQbWZ1RnlsX0Vmd3FkTUZkNnZLb0h5cFNmMHIuMFpRdG5jSC53RXZMMFluaU1ueUNZeDBvQkkuRmNXdGtzRC5rSGJVaFNIWnd5OS0tTUZKSEdWcEpMc2poLTRVdllYdmwucW16RzBseEVJLWQ2bWU2QUFlWGxpSDlRdkRRV283Y0RpV040MlBUeXhmdC1sZy5KWlZPZ28ubndlZEt3bG9nbC1Eb0guSENJYlZGckJFN2g1LVJsN0lNUGtjNEdOcU80QUdhelhIMExKZi1sMmY1UktSZFVNWHd6NXhmZ2puVUQ3X2diamttemtBR1JUbmQ2UTctS1AxQ0EuWkp2LjZvV1dza3pnSlNFUjdYMHZ2NC5FX0RPclcyYkt5akVtVWt6LXlGNm9wTk1QNmVXbS5YLS5FR2l2VW11MVpiUG1vS0ZFWEJQMkdoRU1VY3I5aVdMWUlzLnpfYldWMUxwSmhhd0toYk1ySFZjYXc5T0VqRFBmRl9NTm9RRWJmLWdmTHNXY2xPNVR0QUNPRmJaMGRZWk1zTlA5akQ3ZVh0U1p3c0ZvQ0ZzVVhXRUl5RkZMMENEY1M1Yml5Y0lZQWQ5UFdBMyJ9|8ce93d1c14ca26761dcf7c5c136c4bc47c93e1050854ccd24b2a46bfe1189400"; gdxidpyhxdE=vJddIQAjp9jX/R2kVJ5+/S+ReO4q8JiiQi3Vi/5oi9SAz9y78xEdOaaOnssQOzSi5KWJpoLheUcMLfi6y7owfUWhSE3cKYJwncPVBAnodoX4xn8hjxccu5ugonNkj0uQE0yHdmQViU1TxERG+TrrcJPf5qMZTkxz2ixGUCGw7hcgGtpm:1645536176270; q_c1=d44978f7366142ceb4fb7fe3a8ce066a|1645583921000|1645583921000; NOT_UNREGISTER_WAITING=1; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1646045385,1646045403,1646102448,1646107796; SESSIONID=iG4haVyIET7tawUGjkOuGAih3Jez3LpKr1Dbt7zmUpq; JOID=UVsTAUkf1CiQ-16iPx518CoplswudpYY-JsI3nJbgBrgmij3fYJJMfP6W6M7cNnjij_bTqZ1BtFj3YUgtwKTHe8=; osd=Wl8TBE8U0CiV_VWmPxtz-y4pk8olcpYd_pAM3nddix7gny78eYJMN_j-W6Y9e93jjznQSqZwANpn3YAmvAaTGOk=; tst=h; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1646107975; captcha_session_v2="2|1:0|10:1646107975|18:captcha_session_v2|88:UTJZaXpQbkJleGRzaDV0b1VJS3BQQyt1RkttbC9tRE94Z2d0MDhLUTNlRWNhaXhhZitwU2xjYWtjaTdVOHRHYQ==|248ab41550b00886d71f979b395792a0f9cc07dbe891cc2252ab4bbe5274ac20"; KLBRSID=ed2ad9934af8a1f80db52dcb08d13344|1646107978|1646107792'
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
        if self.cookie == "":
            raise Exception("请在23行输入cookie")
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
        print(self.header["x-zse-96"])
        return self.header

    def get_answer(self, question_id, limit=1):
        now = 0 - limit
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
            print("\r爬取进度:" + str(round(i / (total_num // limit) * 100, 2)) + "%", end="", flush=True)
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
        url = "https://www.zhihu.com/api/v4/questions/{question_id}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_" \
              "comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_stick" \
              "y%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%" \
              "2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Cr" \
              "elevant_info%2Cquestion%2Cexcerpt%2Cis_labeled%2Cpaid_info%2Cpaid_info_content%2Crelationship.is_authoriz" \
              "ed%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_recognized%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url" \
              "%3Bdata%5B%2A%5D.author.follower_count%2Cvip_info%2Cbadge%5B%2A%5D.topics%3Bdata%5B%2A%5D.settings.table_" \
              "of_content.enabled&limit={limit}&offset=0&platform=desktop&sort_by=default".format(
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
            print("\n爬取完成")

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
        time.sleep(3)
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
