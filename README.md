### Git-爬虫

这个库主要用来装一些平时用来学习或者搞着玩的爬虫，目前有用Scrapy框架写的，也有用BeautifulSoup+requests写的，未来可能还会有涉及到java等其他语言的爬虫代码。

目前库存项目有：

**1.b站相关**

1.1 一个B站视频爬取spider（Scrapy+you-get）

1.2 一个B站视频封面提取器（requests+json+re+parsel+os+yaml+Threading）

**2.知乎相关**

2.1 一个知乎问答多线程爬虫（requests+json+re+threading）——已加入ip代理池

2.2 一个知乎用户数据爬虫+数据清洗+数据分析（requests+json+parsel+yaml+threading+pandas）——已加入ip代理池

**3.微博相关**

3.1 一个微博个人信息爬虫（requests+os+parsel+threading+re+random+time+json+pandas）——已加入ip代理池

**4.刚需相关**

4.1 一个xvideos视频爬虫（requests+scrapy+json+parsel+cookiejar+threading）

**5.其他类型**

5.1 一个安居客武汉租房信息爬虫+数据清洗+分析+数据可视化(requests+pandas+parsel+matplotlib)——已加入ip代理池

5.2 一个有声小说音频爬虫（requests+os+parsel+threading+mongodb+re）

5.3 一个网易云音乐的歌单下载程序（BeautifulSoup+request）

5.4 一个壁纸网站的爬图spider（Scrapy）

5.5 一个答案网的学习强国的答案spider+结果文档（Scrapy）



欢迎大家在issue中提出一些好玩的爬虫想法，我会根据情况去尝试实现并及时通知的~~才不是因为莫得灵感了~~，同时也欢迎大家提出宝贵的意见。

**star**可以持续追更呦

**fork**可以一起做有意思的东西呦



**代理池**

1. 这个库里所有的爬虫都是使用的这个项目提供的[代理池](https://github.com/jhao104/proxy_pool)，强烈安利大家去star，大佬们维护的这个项目非常棒，提供了一个十分可靠得代理池接口，调用方便，搭建简单，如果有需求可以自己组一个服务器，把这个项目放到上面24小时更新代理呦~，一起来感受白嫖的快乐~~

2. 上面大佬们已经给出了十分方便的方便调用的代理接口，而我自己又根据自己的需求对这些接口进行了进一步的封装，添加了一些细节，这里也会直接放到这个库里面供大家参考，在[这里](https://github.com/srx-2000/git_spider/tree/master/proxy_pool)我会说明具体的使用方法。
3. 后续我会渐渐将这个库里面需要用到代理池来进行反爬的项目都渐渐的更新为代理爬取的，至于代理的具体使用方法就不在每个项目的子目录里进行说明了。大家直接参考[这里](https://github.com/srx-2000/git_spider/tree/master/proxy_pool)即可。

**鸣谢**

在这里谢过所有我看过的教学视频，网站。

不定时更新ing.........

