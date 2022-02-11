### Git-爬虫

​	这个库主要用来装一些平时用来学习或者搞着玩的爬虫，主要涉及技术点：requests，parsel，BeautifulSoup，线程使用，代理池使用及封装，pandas简单应用，matplotlib简单应用，scrapy框架简单应用。库中所包含的爬虫如果需要使用代理池技术的皆以使用 [jhao104/proxy_pool](https://github.com/jhao104/proxy_pool)代理池，后经过我个人再次封装并将其部署到相应的服务器，以基本保障了我个人的ip使用，具体使用方法详见：[代理池封装](https://github.com/srx-2000/spider_collection/tree/master/proxy_pool)。感谢大家的star与fork，本项目中的任一爬虫皆是在本机或服务器上部署运行成功后上传的，如在运行时出现任何问题欢迎大家在issue中提出。

目前库存项目有：

**1.b站相关**

1.1 [B站视频爬虫](https://github.com/srx-2000/spider_collection/tree/master/bilibiliSP)

1. Scrapy

2. you-get

1.2 [B站视频封面提取器](https://github.com/srx-2000/spider_collection/tree/master/bilibili%E5%B0%81%E9%9D%A2%E6%8F%90%E5%8F%96)

1. requests

2. json

3. re

4. parsel

5. os

6. yaml

7. Threading

**2.知乎相关**

2.1 [知乎问答多线程爬虫](https://github.com/srx-2000/spider_collection/tree/master/zhihuAnswerSpider)

1. requests

2. json

3. re

4. threading

2.2 [知乎用户数据爬虫+数据清洗+数据分析](https://github.com/srx-2000/spider_collection/tree/master/zhihu_user_info_spider)

1. requests
2. json
3. parsel
4. yaml
5. threading
6. pandas

**3.微博相关**

3.1 [微博个人信息爬虫](https://github.com/srx-2000/spider_collection/tree/master/weibo_user_info)

1. requests
2. os
3. parsel
4. threading
5. re
6. random
7. time
8. json
9. pandas
9. selenium

**4.刚需相关**

4.1 [xvideos视频爬虫](https://github.com/srx-2000/spider_collection/tree/master/hubSpider)

1. requests
2. scrapy
3. json
4. parsel
5. cookiejar
6. threading

**5.github相关**

5.1 [github用户爬虫](https://github.com/srx-2000/spider_collection/tree/master/github_spider)

1. requests
2. json
3. parsel
4. threading

**6.其他类型**

5.1 [安居客武汉租房信息爬虫+数据清洗+分析+数据可视化](https://github.com/srx-2000/spider_collection/tree/master/anjuke_room_rent_info)

1. requests
2. pandas
3. parsel
4. matplotlib

5.2 [有声小说音频爬虫](https://github.com/srx-2000/spider_collection/tree/master/audioBook)

1. requests
2. os
3. parsel
4. threading
5. mongodb
6. re

5.3 [网易云音乐的歌单下载程序](https://github.com/srx-2000/spider_collection/tree/master/python%20spider)

1. BeautifulSoup
2. requests

5.4 [壁纸网站的爬虫](https://github.com/srx-2000/spider_collection/tree/master/beautyImgSpider)【基本弃用】

1. Scrapy

5.5 [答案网的学习强国的答案爬虫+结果文档](https://github.com/srx-2000/spider_collection/tree/master/xuexiSpider)【仅爬取结果有用】

1. Scrapy

5.6 [代理池封装](https://github.com/srx-2000/spider_collection/tree/master/proxy_pool)【二次封装】



#### 叨叨

欢迎大家在issue中提出一些好玩的爬虫想法，我会根据情况去尝试实现并及时通知的~~才不是因为莫得灵感了~~，同时也欢迎大家提出宝贵的意见。

**star**可以持续追更呦

**fork**可以一起做有意思的东西呦

**有关代理池**

1. 这个库里所有的爬虫都是使用的这个项目提供的[代理池](https://github.com/jhao104/proxy_pool)，强烈安利大家去star，大佬们维护的这个项目非常棒，提供了一个十分可靠得代理池接口，调用方便，搭建简单，如果有需求可以自己组一个服务器，把这个项目放到上面24小时更新代理呦~，一起来感受白嫖的快乐~~

2. 上面大佬们已经给出了十分方便的方便调用的代理接口，而我自己又根据自己的需求对这些接口进行了进一步的封装，添加了一些细节，这里也会直接放到这个库里面供大家参考，在[这里](https://github.com/srx-2000/git_spider/tree/master/proxy_pool)我会说明具体的使用方法。
3. 后续我会渐渐将这个库里面需要用到代理池来进行反爬的项目都渐渐的更新为代理爬取的，至于代理的具体使用方法就不在每个项目的子目录里进行说明了。大家直接参考[这里](https://github.com/srx-2000/git_spider/tree/master/proxy_pool)即可。

**鸣谢**

在这里谢过所有我看过的教学视频，网站。

不定时更新ing.........

