import requests
import yaml
import os


'''特别鸣谢项目：https://github.com/jhao104/proxy_pool 提供的代理池服务'''

'''这个类主要使用来对上述项目接口的进一步封装以方便调用'''

StopEvent = object()
class Proxy_pool():

    # 默认本机ip，端口是https://github.com/jhao104/proxy_pool项目的默认端口。
    host="127.0.0.1"
    port="5010"

    def __init__(self):
        config=open(os.getcwd()+"\\config.yaml",mode="r",encoding="utf-8")
        cfg=config.read()
        yaml_line=yaml.load(stream=cfg,Loader=yaml.FullLoader)
        self.host=yaml_line["host"]
        self.port=yaml_line["port"]

    def get_proxy(self):
        return requests.get("http://{host}:{port}/get/".format(host=self.host,port=self.port)).json()

    def delete_proxy(self,proxy):
        requests.get("http://{host}:{port}/delete/?proxy={}".format(host=self.host,port=self.port,proxy=proxy))

    # your spider code

    def get_response(self,url,headers,https=False,cookie="",retry_count=5):
        if https:
            is_https=self.get_proxy().get("https")
            print(is_https)
        proxy = self.get_proxy().get("proxy")
        while retry_count > 0:
            try:
                response = requests.get(url=url,headers=headers,cookies=cookie, proxies={"http": "http://{}".format(proxy)})
                # 使用代理访问
                return response
            except Exception:
                retry_count -= 1
        # 删除代理池中代理
        self.delete_proxy(proxy)
        return response

    def post_response(self,url,headers,cookie,data,retry_count=5):
        proxy = self.get_proxy().get("proxy")
        while retry_count > 0:
            try:
                response = requests.post(url=url,headers=headers,data=data,cookies=cookie, proxies={"http": "http://{}".format(proxy)})
                # 使用代理访问
                return response
            except Exception:
                retry_count -= 1
        # 删除代理池中代理
        self.delete_proxy(proxy)
        return response
