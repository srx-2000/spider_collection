import execjs
import os
import hashlib
import requests
from loguru import logger

x_zse_93 = "101_3_3.0"
node_modules_path = r"C:\Users\TRS\Desktop\spider\node_modules"
keyCode_path = os.path.dirname(os.path.abspath(__file__))


class ZhiHuEncrypt:
    headers = {
        'x-zse-93': x_zse_93,
        'x-api-version': '3.0.91',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'x-zse-96': '2.0_',
        'accept': '*/*',
    }

    def __init__(self):
        pass

    @staticmethod
    def get_d_c0():
        url_param = "/udid"
        a_v = ZhiHuEncrypt.getEncryCode(x_zse_93 + url_param)
        ZhiHuEncrypt.headers.update({"x-zse-96": '2.0_' + a_v})
        first_res = requests.post('https://www.zhihu.com/udid', data={}, headers=ZhiHuEncrypt.headers, timeout=10)
        cookie_t = requests.utils.dict_from_cookiejar(first_res.cookies)
        d_c0 = cookie_t.get('d_c0')
        logger.info(f"d_c0==> {d_c0}")
        return d_c0

    @staticmethod
    def getEncryCode(url: str, d_c0: str = ""):
        base_str = x_zse_93 + "+" + url + "+" + d_c0
        print(base_str)
        fmd5 = hashlib.md5(base_str.encode("utf8")).hexdigest()
        print(fmd5)
        with open(os.path.join(keyCode_path, 'zhihu_encrypt_js.js'), 'r', encoding="utf-8") as f:
            ctx1 = execjs.compile(f.read(), cwd=node_modules_path)
        encrypt_str = ctx1.call('getEncryptCode', fmd5)
        logger.info(f"EncryCode==> {encrypt_str}")
        return encrypt_str

    @staticmethod
    def get_result(url: str):
        url_host = "https://www.zhihu.com"
        url_path = url.split("?")[0].replace(url_host, "") + "?"
        url_params = url.split("?")[1]
        d_c0 = ZhiHuEncrypt.get_d_c0()
        encrypted_str = ZhiHuEncrypt.getEncryCode(url_path + url_params, d_c0)
        ZhiHuEncrypt.headers.update({"x-zse-96": '2.0_' + encrypted_str})
        ZhiHuEncrypt.headers.update({"cookie": f"d_c0={d_c0};"})
        ZhiHuEncrypt.headers.update({'accept-encoding': 'gzip, deflate, br',
                                     'accept-language': 'zh-CN,zh;q=0.9'})
        res = requests.get(url, headers=ZhiHuEncrypt.headers, timeout=10)
        logger.info(f"final_result==>{res.json()}")
        return res.json()


if __name__ == '__main__':
    url = "https://www.zhihu.com/api/v4/members/lai-si-shuang-yu-27/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&offset=220&limit=20"
    result = ZhiHuEncrypt.get_result(url)
    print(result)
