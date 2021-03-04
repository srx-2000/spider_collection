### 有声书爬虫

​	[爬取思路](#a)

​	[功能](#b)

​	[使用方法](#c)

​	[环境及技术栈](#d)

​	[更新日志](#e)

​	最近一直有用听书软件听一些小说，之前一直使用喜马拉雅听，但是这个软件里面有一些书是付费的，尤其是有个“有声的紫襟”这个主播，之前听他播的好多书都付费了。最近又再追《我的老千生涯》。没错，又收费了。所以就在网上找了找一些免费的听书平台，想要爬下来慢慢听。一开始找到静听网，后来经过一段时间的尝试发现，那个站长太厉害了，反爬做的相当完备，所以只好调转枪头去别的网站谋生路了。终于，功夫不费有心人，让我找到了一个相对好爬一些的[网站](https://www.ishuyin.com)。这个网站，我大致查了一下东西还是挺多的，所以未来有打算慢慢维护一下这个爬虫，添加搜索，数据库等功能，也有可能会写成一个接口，未来接入Android。

 <a id="a">**爬取思路**</a>

​	说下这个网站在我爬取的时候的一个小思路，给大家当个案例。经过我研究他们的js源码，发现他们使用的前端播放器是jplayer。而这个播放器在调用时必须提供音频地址。所以我就在他的源代码中找到了这一小段加密代码(这里就不copy全了，详细见其网页源代码)。

```js
$(document).ready(function(){ 
    $("#jquery_jplayer_1").jPlayer({ 
        ready: function (event) { 
    var u="*104*116*116*112*58*47*47*109*112*51*46*97*105*107*101*117*46*99*111*109*47*50*51*55*51*54*47*50*46*109*112*51*";
	var uArr=u.split("*");
	var n = uArr.length;
	var x = '';
	for(i=1;i<n-1;i++){
   		x += String.fromCharCode(uArr[i]);
	}
		
            $(this).jPlayer("setMedia", { 
                mp3:x, 
            }).jPlayer("play"); // 自动播放
        }, 
```

​	我们可以看到在jplayer后面跟着`mp3:x`这个代码段，而通过对jplayer的了解，这个x就是音频地址了。而往上面追溯可以追溯到u这个变量。而这里通过使用`String.fromCharCode`函数对u进行了解码后就得到了音频地址。所以我们在python中我们只需要使用re库匹配到这个u的值再使用`chr()`函数进行解码，就可以获取到音频地址啦。

<a id="b">**功能**</a>

- [基础功能](https://github.com/srx-2000/git_spider/tree/audioBook-1.0)

<a id="c">**使用方法**</a>

​	需要使用到的库已经放在各个版本的requirements.txt文件中了，使用pip安装的可以使用指令`pip install -r requirements.txt`。如果国内安装第三方库比较慢，可以使用以下指令进行清华源加速`pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/`

*  [version-1.0](https://github.com/srx-2000/git_spider/tree/audioBook-1.0/#b)

<a id='d'>**环境**</a>

* Windows 10
* python 3.7

<a id='d'>**技术栈**</a>

- requests
- os
- parsel
- threading
- mongodb
- re

<a id='e'>**更新日志**</a>

* 2020.3.3

  基础功能，单线程爬取指定书的id的所有音频
  
* 2020.3.4

  加入多线程解析页面以及多线程下载