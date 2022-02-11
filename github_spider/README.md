## github用户爬虫

​	最近一直在忙毕设的事情，身边的同学也是。正好身边的一个朋友的课题是对github的库进行优化的题目，所以就拜托我给他写一个github的用户爬虫，大致需要用户的基础信息和用户所有的公开库的信息，所以这个爬虫就诞生了。说起来爬github其实并不困难，因为github本身就已经提供了相当完善的rest api。同时对于反爬措施也仅有一个速率限制【但就是这个速率限制挺致命的】。所以这个爬虫大概用了半天就写了出来，后续加上各种完善以及代码的重构还有各种小bug又花费了一天多的时间。同时有了上次知乎爬虫的经验之后，我开始对自己有一定规模的爬虫的代码进行了组件化设计，不再是一个spider文件写所有代码了。未来如果我这个架构足够成熟了，我有可能会做一些造轮子的开发，比如写个框架或者爬虫包啥的。

首先说一下这次的需求吧：

1. **对用户**
   1. 用户基础信息：id，login，email，location，hireable，public_repos【数量】，followers【数量】，following【数量】
   2. 用户公开库的地址列表：public_repos_urls
2. **对库**
   1. 库基础信息：repo_name，fork【数量】，description
   2. 库的提交信息：commit_num，file_changes，additions，deletions，commit_list【提交列表，每次提交的sha，文件修改数量，代码添加行数，代码减少行数】

​	该项目的数据量大概定在几万到十几万的标准，但由于github对接口调用的速率限制，只能做到每小时5000条。不过相对的我也做了一个自动化的处理，即自动检测每小时爬取数量，如果超过5000次就会自动沉睡剩余时间，使爬虫实现了自动化。

**使用方法【仅提供pycharm运行方式】**

- **git clone**

 `https://github.com/srx-2000/git_spider.git`

- **安装依赖**

  需要使用到的库已经放在requirements.txt，使用pip安装的可以使用指令`pip install -r requirements.txt`。如果国内安装第三方库比较慢，可以使用以下指令进行清华源加速`pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/`

- **配置文件【如果未配置下列文件，则爬虫无法运行】**

  1. 打开`util/config.json`文件，配置以下是五个配置项，

     | save_method         | 用于规定保存方式，现仅有csv保存方式                          |
     | ------------------- | ------------------------------------------------------------ |
     | **api_token**       | **用来保存个人api_token的，api_token的获取方式见[连接](https://blog.csdn.net/weixin_43274247/article/details/106577653)** |
     | **batch_size**      | **用来规定爬取多少条数据向csv中保存一次的**                  |
     | **thread_num**      | **线程数，一般开20左右就够用了，我这里自己测的时候，20个线程2分钟就能爬到1w的数据了** |
     | **user_batch_size** | **用户批量保存数量，即一批保存多少个**                       |
     | **repo_batch_size** | **库批量保存数量，即一批保存多少个**                         |

  ```json
  {
    "save_method": "csv",
    "thread_num": 20,
    "api_token": "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",
    "user_batch_size": 1000,
    "repo_batch_size": 200
  }
  ```

> 提示：limit_count.txt、start_time.txt这两个文件是用来监测每小时请求数量的，所以别删，删了可能导致运行到一半报错

* **运行爬虫**

​	爬取用户就运行userRequester模块：

|          方法名          |                 描述                 |                      参数:类型【描述】                       |             返回值             |
| :----------------------: | :----------------------------------: | :----------------------------------------------------------: | :----------------------------: |
| **get_single_user_info** |     **给定用户名，爬取单个用户**     | **1. username:str【用户名】<br/>2. is_save:bool【是否保存】** | **用户字典【字典属性见需求】** |
|      **get_users**       | **给定用户数量，爬取给定数量的用户** | **1. user_num:int【用户数量】<br/>2. is_save:bool【是否保存】** |          **用户列表**          |

​	爬取用户的库就运行repoRequester模块

|                   方法名                   |                             描述                             |                     参数:类型【描述】                      |             返回值             |
| :----------------------------------------: | :----------------------------------------------------------: | :--------------------------------------------------------: | :----------------------------: |
|               **get_readme**               |           **给定用户名，库名，爬取单个库的README**           | **1. username:str【用户名】<br/>2. repo_name:str【库名】** | **无** |
| **get_repo_detail** | **给定用户名，库名，爬取单个库的详细信息** |                        **1. username:str【用户名】<br/>2. repo_name:str【库名】**                        |**库字典【字典属性见需求】**|
|            **get_repo_commit**             |         **给定用户名，库名，爬取单个库的commit信息**         | **1. username:str【用户名】<br/>2. repo_name:str【库名】<br />3.is_save:bool【是否保存】** | **commit字典和commit列表组成的元组【字典和列表属性见需求】** |
|               **get_repos**                | **给定用户名，或用户列表，爬取给定用户的所有库的信息和commit信息，或爬取给定列表中所有用户的库的信息和commit信息** | **1. user:str/list【用户名/用户列表】<br/>2.is_save:bool【是否保存】** | **返回库列表【库的详细信息+commit字典】** |

> 提示：在爬取用户库的时候，如果你的电脑本身无法访问github网站的话，可能需要科学上网，才可以继续爬取。科学上网的方式不能仅代理浏览器，一定要能全局代理【推荐v2ray】。具体的科学上网方式这里就不展开讲了，大家自行解决。

**运行效果**

1. **获取数据**

![](https://raw.githubusercontent.com/srx-2000/git_spider/master/github_spider/1.png)

2. **数据展示【用户】**

![](https://raw.githubusercontent.com/srx-2000/git_spider/master/github_spider/2.png)

3. **数据展示【repo】**

![](https://raw.githubusercontent.com/srx-2000/git_spider/master/github_spider/3.png)

**更新日志**

* 2022.2.11

  更新第一版，完成基本功能
