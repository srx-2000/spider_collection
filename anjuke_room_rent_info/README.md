### 安居客出租房（武汉为例）爬虫+数据分析+可视化

这个爬虫是我前段时间在淘宝上做单子的时候遇见的一个客户需求。本来以为就是一个简单的爬虫项目。但后面客户加了数据清洗和数据分析的要求。而后又加了要详细代码解释的需求等等。直到最后客户坦白说这是他们大专的毕设.......但是这个单子坐下来只有200左右，我想了一下，感觉好亏啊。在淘宝上随便找一个做毕设的都要好多钱的，而且客户本身的代码能力、数学、逻辑能力都很差，导致我每行都给注释以及看不懂，在我交付代码后又纠缠了我一个多礼拜。反正总体做下来的感觉就是烦躁。头一次感觉到了客户需求变更带来的巨大麻烦。

总之这是一次不是很愉快的爬虫经历。但是作为我写爬虫以来注释最详细的一次，以及第一次真正使用像matplotlib这种数据分析库的代码，我认为还是有必要分享出来给大家当个参考的（PS：大佬轻拍~）。爬虫本身几乎没有什么难度，写的也比较乱，敬请见谅。

**功能**

爬取安居客上的出租房信息（武汉地区的），并通过爬取的数据进行数据清洗以及数据分析。给出四个不同层面的可视化图。最终结果如下图所示：

![Image text](https://raw.githubusercontent.com/srx-2000/git_spider/master/anjuke_room_rent_info/result/1.png)

![Image text](https://raw.githubusercontent.com/srx-2000/git_spider/master/anjuke_room_rent_info/result/2.png)

![Image text](https://raw.githubusercontent.com/srx-2000/git_spider/master/anjuke_room_rent_info/result/3.png)

![Image text](https://raw.githubusercontent.com/srx-2000/git_spider/master/anjuke_room_rent_info/result/4.png)

**环境**

1. Windows 10

2. python3.7

**使用方法**

首先声明该爬虫由于是特定情况下写的，所以本身的通用性特别差，仅可以对安居客网站上的武汉的出租房信息进行爬取，且需要自己手动更新cookie。同时在对数据进行分析及可视化的时候由于也是特别针对武汉出租房的进行的，所以针对性也比较强。如果别的需求需要自己进行更改。

1. 访问[安居客网址](https://wuhan.anjuke.com/)，获取cookie。

   > tip：获取cookie的方法可根据[此链接](https://jingyan.baidu.com/article/5d368d1ea6c6e33f60c057ef.html)

2. 在项目中找到`spider.py`的文件，将第12行的cookie换成你自己的cookie。
3. 运行`spider.py`，获取房源信息。运行后应会产生一个`武汉出租房源情况.csv`的文件。此文件为我们从安居客上爬取的房源信息，其中包含`房屋租住链接、房屋描述、房屋地址、房屋详情（户型）以及经纪人、房屋价格`五个属性。
4. 在获取了数据之后我们运行`matplotlib.py`文件。进行数据清洗，分析，可视化。运行后即可获得**功能**中展示四个图片。

**技术栈**

1. request
2. parsel
3. pandas
4. matplotlib

**进步（相比之前）**

此次爬虫相比之前的技术上可以说有减无增。但其中注释相当详细，可谓是每行代码都有注释。所以对于初学者应该有一些用处。同时使用matplotlib进行了数据分析可视化等。对于数据处理的代码的注释也是几乎每行都有注释的。

