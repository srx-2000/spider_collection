import requests
import yaml
import os


'''特别鸣谢项目：https://github.com/jhao104/proxy_pool 提供的代理池服务'''

'''这个类主要使用来对上述项目接口的进一步封装以方便调用'''

class Proxy_pool():

    # 默认本机ip，端口是上述项目的默认端口。
    host="127.0.0.1"
    port="5010"

    # 初始化用过yaml文件读取配置
    def __init__(self):
        config=open(os.getcwd()+"\\config.yaml",mode="r",encoding="utf-8")
        cfg=config.read()
        yaml_line=yaml.load(stream=cfg,Loader=yaml.FullLoader)
        self.host=yaml_line["host"]
        self.port=yaml_line["port"]

    # 调用get接口，获取一个代理
    def __get_proxy(self):
        return requests.get("http://{host}:{port}/get/".format(host=self.host,port=self.port)).json()

    # 调用delete接口，删除一个代理，主要作用就是通过下面的get_response方法进一步筛掉redis数据库中不可用的代理
    def __delete_proxy(self,proxy):
        requests.get("http://{host}:{port}/delete/?proxy={proxy}".format(host=self.host,port=self.port,proxy=proxy))

    # 筛选https代理
    def __is_https(self):
        while True:
            json = self.__get_proxy()
            is_https = json.get("https")
            print(json)
            if is_https:
                proxy = json.get("proxy")
                proxies = {"https": "https://{}".format(proxy)}
                print(proxy)
                return proxies,proxy

    # 非必要不要使用https代理，因为需要进一步的筛选同时还有可能出现：代理池中并未有https代理导致程序崩溃或卡死
    def get_response(self,url,headers,https=False,cookies="",retry_count=5):
        proxy=""
        while retry_count > 0:
            try:
                if https:
                    proxies = self.__is_https()[0]
                    proxy = self.__is_https()[1]
                else:
                    proxy = self.__get_proxy().get("proxy")
                    proxies={"http": "http://{}".format(proxy)}
                # 使用代理访问
                response = requests.get(url=url,headers=headers,cookies=cookies, proxies=proxies)
                return response
            except Exception:
                retry_count -= 1
        # 删除代理池中代理
        self.__delete_proxy(proxy)
        return response

    # https代理与get同理
    def post_response(self,url,headers,https=False,data={},cookies="",retry_count=5):
        proxy = self.__get_proxy().get("proxy")
        while retry_count > 0:
            try:
                if https:
                    proxies=self.__is_https()[0]
                    proxy=self.__is_https()[1]
                else:
                    proxy = self.__get_proxy().get("proxy")
                    proxies={"http": "http://{}".format(proxy)}
                response = requests.post(url=url,headers=headers,data=data,cookies=cookies, proxies=proxies)
                # 使用代理访问
                return response
            except Exception:
                retry_count -= 1
        # 删除代理池中代理
        self.__delete_proxy(proxy)
        return response
