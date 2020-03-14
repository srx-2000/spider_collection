#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import requests as rq
from bs4 import BeautifulSoup as BS
import os
import re

#551886644

cloud = 'http://music.163.com/song/media/outer/url?id='
def getMusic(ID,path):
    kv={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
    try:
        url=cloud+ID+'.mp3'
        tmp=rq.get(url,headers=kv)
        tmp.raise_for_status()
        print("访问成功，正在下载.....")
        with open(path,'wb') as f:
            f.write(tmp.content)
        f.close()
        print("下载成功")
    except:
        print("下载失败")
def getMusicList(ID):
    headers = {
        'Referer': 'https://music.163.com',
        'Host': 'music.163.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }
    base_url='http://music.163.com/playlist?id='
    s=rq.session()
    url=base_url+str(ID)
    response=s.get(url,headers=headers).content
    soup=BS(response,'lxml')
    title=soup.find('h2',{'class':'f-ff2 f-brk'}).text
    main=soup.find('ul',{'class':'f-hide'})
    ls=main.find_all('a')
    song_dic={}
    print('一共有'+str(len(ls))+'首歌')
    for music in ls:
        name=music.text
        ID=str(music['href'].replace('/song?id=',''))
        song_dic[name]=ID
        print("Name:{:30}\tID{:^10}".format(name,ID))
    return title,song_dic
# print(getMusicList(2848226139))
def UrlToID(Url):
    ID=''
    count=0
    for i in range(0,len(Url)):
        count+=1;
        if Url[i]=='=':
            break;
    for i in range(count,len(Url)):
        ID+=Url[i]
    return ID
# print(UrlToID('https://music.163.com/#/playlist?id=551886644'))
def main():
    Url=input("请输入一个你想下载的歌单的网址或者Id:")
    if(len(Url)>36):
        ID=UrlToID(Url)
    else:
        ID=Url
    title,song_dic=getMusicList(ID)
    if os.path.exists(title):
        print("文件夹已存在")
    else:
        os.mkdir(title)
        print("创建文件夹"+title)
    for item in song_dic:
        print(item,end="    ")
        path=title+'/'+item+'.mp3'
        getMusic(song_dic[item],path)
if __name__=='__main__':
    main()