import requests
import yaml
import os

abs_path = os.path.dirname(os.path.abspath(__file__))

'''特别鸣谢项目：https://github.com/jhao104/proxy_pool 提供的代理池服务'''

'''这个类主要使用来对上述项目接口的进一步封装以方便调用'''


class Proxy_pool(object):
    # 默认本机ip，端口是上述项目的默认端口。
    host = "127.0.0.1"
    port = "5010"
    is_proxy = True

    # 初始化用过yaml文件读取配置
    def __init__(self):
        config = open(abs_path + os.sep + "config.yaml", mode="r", encoding="utf-8")
        cfg = config.read()
        yaml_line = yaml.load(stream=cfg, Loader=yaml.FullLoader)
        self.host = yaml_line["host"]
        self.port = yaml_line["port"]
        self.is_proxy = bool(yaml_line["is_proxy"])

    # 调用get接口，获取一个代理
    def __get_proxy(self):
        return requests.get("http://{host}:{port}/get/".format(host=self.host, port=self.port)).json()

    # 调用delete接口，删除一个代理，主要作用就是通过下面的get_response方法进一步筛掉redis数据库中不可用的代理
    def __delete_proxy(self, proxy):
        requests.get("http://{host}:{port}/delete/?proxy={proxy}".format(host=self.host, port=self.port, proxy=proxy))

    def __is_anonymity(self, headers, is_https=False):
        try:
            test_url = "http://httpbin.org/ip"
            origin_ip = requests.get(url=test_url, headers=headers).json()["origin"]
            while True:
                if is_https:
                    https_proxy = self.__is_https()
                    proxy = https_proxy[1]
                    proxies = https_proxy[0]
                else:
                    # json = self.__get_proxy()
                    proxy = self.__get_proxy().get("proxy")
                    proxies = {"http": "http://{ip}".format(ip=proxy)}
                ip_json = requests.get(url=test_url, headers=headers, proxies=proxies, timeout=5)
                if ip_json.status_code != 404:
                    proxy_ip = ip_json.json()["origin"]
                    if not proxy_ip.__contains__(origin_ip):
                        # print("获取可匿代理：:" + str(proxy_ip))
                        return proxies, proxy
        except Exception as e:
            # print("匿名代理筛选出错：")
            # print(e)
            pass

    # 筛选https代理
    def __is_https(self):
        while True:
            json = self.__get_proxy()
            is_https = bool(json.get("https"))
            # print(json)
            if is_https:
                proxy = json.get("proxy")
                proxies = {"https": "https://{ip}".format(ip=proxy)}
                # print(proxy)
                return proxies, proxy

    # 非必要不要使用https代理，因为需要进一步的筛选同时还有可能出现：代理池中并未有https代理导致程序崩溃或卡死
    # 基本别把https和匿名代理的开关同时打开，这样可能筛到最后啥也没有了
    def get(self, url, headers, https=False, anonymity=False, timeout=10, cookies="", retry_count=5):
        if self.is_proxy:
            return self.__wrapping_request(is_get=True, url=url, headers=headers, https=https, anonymity=anonymity,
                                           timeout=timeout, cookies=cookies, retry_count=retry_count)
        else:
            return requests.get(url=url, headers=headers, timeout=timeout, cookies=cookies)

    # https代理与get同理
    def post(self, url, headers, https=False, anonymity=False, timeout=10, data={}, cookies="", retry_count=5):
        if self.is_proxy:
            return self.__wrapping_request(is_get=False, url=url, headers=headers, data=data, https=https,
                                           anonymity=anonymity,
                                           timeout=timeout, cookies=cookies, retry_count=retry_count)
        else:
            return requests.post(url=url, headers=headers, cookies=cookies, timeout=timeout, data=data)

    # requests封装
    def __wrapping_request(self, is_get, url, headers, https=False, anonymity=False, timeout=10, data={}, cookies="",
                           retry_count=5):
        proxy = ""
        response = None
        while retry_count > 0:
            try:
                if https:
                    https_proxy = self.__is_https()
                    proxy = https_proxy[1]
                    proxies = https_proxy[0]
                if anonymity:
                    anonymity_proxy = self.__is_anonymity(headers=headers, is_https=https)
                    proxy = anonymity_proxy[1]
                    proxies = anonymity_proxy[0]
                else:
                    proxy = self.__get_proxy().get("proxy")
                    proxies = {"http": "http://{ip}".format(ip=proxy)}
                if is_get:
                    response = requests.get(url=url, headers=headers, cookies=cookies, timeout=timeout, proxies=proxies)
                else:
                    response = requests.post(url=url, headers=headers, data=data, cookies=cookies, timeout=timeout,
                                             proxies=proxies)
                # 使用代理访问
                return response
            except Exception as e:
                # print(e)
                retry_count -= 1
                # print("代理{ip}连接失败，更换代理".format(ip=proxy))
        if response is None:
            # 删除代理池中代理
            self.__delete_proxy(proxy)
        return response
