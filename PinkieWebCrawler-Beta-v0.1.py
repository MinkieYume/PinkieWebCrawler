#!/usr/bin/env python
# -*_ coding: utf-8 -*-
#Pinkie Web-Crawler.py
import urllib.request
import sys
import os
from bs4 import BeautifulSoup

class PonyCrawler4399:#定义4399小马爬虫类，实现爬取4399资源的功能
    #声明属性
    response = urllib.request.urlopen('http://www.4399er.com/xzt/xmblzq/')
    html = response.read().decode('UTF-8')
    #声明方法
    def getmusic(link='http://www.4399er.com/xzt/xmblcq/',mode = 0):
        #从4399爬取音乐的方法
        """
        link是链接，mode是模式，
        mode为0是只爬取链接和文本，
        1是爬取音乐，链接和文本，2是只爬取音乐
        """
        #获取4399小马专区音乐首页的内容：
        MusicStations = urllib.request.urlopen(link)
        Htmls = BeautifulSoup(MusicStations.read().decode('UTF-8'),'html.parser')
        """
        关于BeauifulSoup的用法，具体看网站：
        https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html
        """
        if mode == 0:#设定模式为0时的情况
            #下面是处理和读取网站文件
            """
            由于4399小马专区的音乐序列存放在ul代码块的li代码块中,
            所以应该从文档中的ul代码块搜索<li>代码块
            """
            lines = Htmls.ul.find_all('li')
            Musiclist = []#音乐清单序列
            Musiclistindex = 0#列表索引变量，用于在遍历时记录音乐清单的索引
            for line in lines:#遍历lines代码块
                Musicd = {'img':'','name':'','url':'','discuss':''}
                """
                这里创建一个字典对象，用来储存图片链接，名字链接
                音乐页面链接
                以及介绍
                """
                #直接读取图片链接
                img = line.find('img')
                Musicd['img'] = img['data-src']
                url = line.find(attrs={"class": "more"})
                """
                由于4399的音乐链接在class为more的链接标签里面
                所以这里用find_all指令直接遍历line中有class="more"的标签
                """
                Musicd['url'] = 'http://www.4399er.com'+url['href']#获取音乐页面链接
                Musicd['name'] = line.a['title']#获取音乐名字
                Musiclist.append(Musicd)
            print('共找到%d首歌，准备爬取中.......'%len(Musiclist))
            for Musicd in Musiclist:#遍历整个音乐列表
                #通过音乐的页面url获取音乐介绍
                #打开并读取音乐页面的url
                IsError = False#异常记录变量
                Musicstation = urllib.request.urlopen(Musicd['url'])
                try:
                    Musichtml = BeautifulSoup(Musicstation.read().decode('UTF-8'),'html.parser')
                except:
                    IsError = True
                """
                由于音乐的介绍文本是第一个具有
                style="color: rgb(0, 128, 128)"
                属性的标签，所以就直接搜索第一个这样的标签
                """
                try:
                    discusstag = Musichtml.find(name='span',attrs={"style":"color: rgb(0, 128, 128);"})
                    discusz = discusstag.get_text()#记录并方便测验是否有错误
                except:
                    try:
                        discusstag = Musichtml.find(name='span',attrs={"style":"color: #008080"})
                        discusz = discusstag.get_text()
                        if discusz == '"小马宝莉同人歌曲':
                            discusz = discusstag.find_all(name='span',attrs={"style":"color: #008080"})[1]
                    except:
                        try:
                            discusstag = Musichtml.find(name='span',attrs={"style":"color: rgb(0, 0, 0);"})
                            discusz = discusstag.get_text()
                        except:
                            print('此页面被小呆吃了哦，未找到哦')
                            IsError = True#将异常记录变量设置为有异常
                if IsError == False:#设置无异常的情况
                    Musicd['discuss'] = discusz
                    Musiclist[Musiclistindex] = Musicd
                    Musiclistindex += 1
                    print('已爬取%d/%d首歌'%(Musiclistindex,len(Musiclist)))
                else:#有异常的情况
                    Musicd['discuss'] = '暂无'
                    Musiclist[Musiclistindex] = Musicd
                    Musiclistindex += 1
                    print('第%d首歌无法爬取，具体url为%s'%(Musiclistindex,Musicd['url']))
            Musiclistindex = 0#清空索引记录值数据，以备下次再用
            for Musicd in Musiclist:
                """
                下面的方法就是将文本格式化成wordpress的html格式
                """
                Musicd['img'] = '<img src="%s" />'%Musicd['img']
                Musicd['url'] = '链接：<a href="%s">%s</a>'%(Musicd['url'],'4399源地址')
                Musicd['name'] = '音乐名：%s'%Musicd['name']
                Musicd['discuss'] = '简介：%s'%Musicd['discuss']
                Musiclist[Musiclistindex] = Musicd
                Musiclistindex += 1
            Musiclistindex = 0#清空索引记录值数据，以备下次再用
            with open('4399MusicList.txt','wb') as h:
                """
                最后一步，整合排版并依次写入,导出TxT文件
                """
                for PPhtmlwrites in Musiclist:
                    h.write(PPhtmlwrites['img'].encode('UTF-8')+'\n\n'.encode('UTF-8'))
                    h.write(PPhtmlwrites['name'].encode('UTF-8')+'\n\n'.encode('UTF-8'))
                    h.write(PPhtmlwrites['url'].encode('UTF-8')+'\n\n'.encode('UTF-8'))
                    h.write(PPhtmlwrites['discuss'].encode('UTF-8')+'\n\n'.encode('UTF-8'))
                    Musiclistindex += 1
                    print('已将%d/%d首歌写入文件'%(Musiclistindex,len(Musiclist)))
if __name__ =='__main__':#测试运行程序
    PonyCrawler4399.getmusic()

