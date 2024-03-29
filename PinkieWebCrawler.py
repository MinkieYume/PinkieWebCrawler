#!/usr/bin/env python
# -*_ coding: utf-8 -*-
#Pinkie Web-Crawler.py
import urllib.request
import sys
import os
import os.path
import re
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
        1是爬取音乐，链接和文本
        """
        #获取4399小马专区音乐首页的内容：
        MusicStations = urllib.request.urlopen(link)
        Htmls = BeautifulSoup(MusicStations.read().decode('UTF-8'),'html.parser')
        """
        关于BeauifulSoup的用法，具体看网站：
        https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html
        """
        if mode == 0 or mode == 1:#设定模式为0或1时的情况
            #下面是处理和读取网站文件
            """
            由于4399小马专区的音乐序列存放在ul代码块的li代码块中,
            所以应该从文档中的ul代码块搜索<li>代码块
            """
            isa = False#写入文件时是否使用追加模式写入
            lines = Htmls.ul.find_all('li')
            Musiclist = []#音乐清单序列
            Musiclistindex = 0#列表索引变量，用于在遍历时记录音乐清单的索引
            for line in lines:#遍历lines代码块
                """
                以下代码用于从配置文件中检测是否已经存在相应音乐
                """
                if os.path.exists('4399MusicList.txt'):#判断文件是否存在
                    isa = True
                    f = open('4399MusicList.txt','rb')
                    existmusics = f.read().decode('UTF-8')
                Musicd = {'img':'','name':'','url':'','discuss':'','music':''}
                """
                这里创建一个字典对象，用来储存图片链接，名字链接
                音乐页面链接
                以及介绍
                """
                #直接读取图片链接
                img = line.find('img')
                if img['data-src'] in existmusics:
                    print(img['data-src'])
                    break
                Musicd['img'] = img['data-src']
                url = line.find(attrs={"class": "more"})
                """
                由于4399的音乐链接在class为more的链接标签里面
                所以这里用find_all指令直接遍历line中有class="more"的标签
                """
                Musicd['url'] = 'http://www.4399er.com'+url['href']#获取音乐页面链接
                Musicd['name'] = line.a['title']#获取音乐名字
                Musiclist.append(Musicd)
                if isa:
                    f.close()
            print('共找到%d首歌，准备爬取中.......'%len(Musiclist))
            for Musicd in Musiclist:#遍历整个音乐列表
                #通过音乐的页面url获取音乐介绍
                IsError = False#异常记录变量
                Musicstation = urllib.request.urlopen(Musicd['url'])
                try:
                    Musichtml = BeautifulSoup(Musicstation.read().decode('UTF-8'),'html.parser')
                    #打开并读取音乐页面的url
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
                    if mode == 1:#设定模式为1时，将音乐直链爬取
                        Music = Musichtml.find(name = 'embed')
                        Musicd['music'] = Music['src']
                        Musicd['music'] = re.findall(r"(?<=currentSong=)http://[\S\s]*\.mp3",Musicd['music'])#用正则表达式匹配currentSong=后面到.mp3的字符串部分
                        for XXX in Musicd['music']:
                            Musicd['music'] = XXX
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
                if mode == 1:#如果模式为1的话，则将音乐也读取,存音乐文件
                    try:
                        Music = urllib.request.urlopen(Musicd['music'])
                        with open(os.getcwd()+'\\'+Musicd['name']+'.mp3','wb') as m:
                            m.write(Music.read())#将音乐数据写入文件
                            print('已下载%d/%d首歌'%(Musiclistindex+1,len(Musiclist)))
                    except:
                        print('神驹似乎咬断了你的网线呢！')
                Musiclist[Musiclistindex] = Musicd
                Musiclistindex += 1
            Musiclistindex = 0#清空索引记录值数据，以备下次再用
            if isa:#判断是否使用向前追加模式打开文件
                """
                由于这里要在文件开头写入文件，
                所以写之前需要把原文件储存到old变量中。
                """
                with open('4399MusicList.txt','rb') as h:
                    old = h.read().decode('utf-8')
                with open('4399MusicList.txt','wb') as h:
                    for PPhtmlwrites in Musiclist:
                        h.write(PPhtmlwrites['img'].encode('UTF-8')+'\n\n'.encode('UTF-8'))
                        h.write(PPhtmlwrites['name'].encode('UTF-8')+'\n\n'.encode('UTF-8'))
                        h.write(PPhtmlwrites['url'].encode('UTF-8')+'\n\n'.encode('UTF-8'))
                        h.write(PPhtmlwrites['discuss'].encode('UTF-8')+'\n\n'.encode('UTF-8'))
                        Musiclistindex += 1
                        print('已将%d/%d首歌写入文件'%(Musiclistindex,len(Musiclist)))
                    h.write(old.encode('utf-8'))
            else:
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
    def getstories(link="http://www.4399er.com/xzt/xmblgsdhj/"):
        StoryStations = urllib.request.urlopen(link)
        Htmls=BeautifulSoup(StoryStations.read().decode('utf-8'),'html.parser')
        """
        上面是如何获取网页内容
        """
        lines=Htmls.ul.find_all("li")
        StoriesList=[]
        Storyindex = 0
        print('开始 获取小马故事中.....总共有%d个故事。'%len(lines))
        for line in lines:
            try:
                story={'title':'','href':'','discus':''}
                storytab=line.find(name="a",class_="tit")
                story.update(title=storytab.get_text())
                story.update(href='http://www.4399er.com'+storytab['href'])
                discuss=urllib.request.urlopen(story['href'])
                discussoup=BeautifulSoup(discuss.read().decode('utf-8'),'html.parser')
                discustext=discussoup.find(name='div',class_='introduce__body-intro').get_text()
                story.update(discus=discustext)
                StoriesList.append(story)
                Storyindex+=1
                print('已经获取了%d/%d个故事'%(Storyindex,len(lines)))
            except:
                print('这个页面已经被小呆吞掉了哦')
        with open('4399Stories.txt','wb') as h:
            Storyindex=0
            for PPwrites in StoriesList:
                h.write('标题：'.encode('utf-8')+PPwrites['title'].encode('utf-8')+'\n\n'.encode('utf-8'))
                h.write('介绍：'.encode('utf-8')+PPwrites['discus'].encode('utf-8')+'\n\n'.encode('utf-8'))
                h.write('地址：'.encode('utf-8')+PPwrites['href'].encode('utf-8')+'\n\n'.encode('utf-8'))
                Storyindex+=1
                print('已经写入了%d/%d个故事'%(Storyindex,len(lines)))
    def getcomic(link="http://www.4399er.com/xzt/xmblmh/"):
        ComicStations=urllib.request.urlopen(link)
        Htmls=BeautifulSoup(ComicStations.read().decode('utf-8'),'html.parser')
        lines=Htmls.ul.find_all("li")
        StoriesList=[]
        Storyindex = 0
        print('开始 获取小马漫画中.....总共有%d个漫画。'%len(lines))
        for line in lines:
            try:
                story={'title':'','href':'','discus':''}
                storytab=line.find(name="a",class_="tit")
                story.update(title=storytab.get_text())
                story.update(href='http://www.4399er.com'+storytab['href'])
                discuss=urllib.request.urlopen(story['href'])
                discussoup=BeautifulSoup(discuss.read().decode('utf-8'),'html.parser')
                discuss=urllib.request.urlopen(story['href'])
                discussoup=BeautifulSoup(discuss.read().decode('utf-8'),'html.parser')
                discustext=discussoup.find(name='div',class_='introduce__body-intro').get_text()
                story.update(discus=discustext)
                StoriesList.append(story)
                Storyindex+=1
                print('已经获取了%d/%d个漫画'%(Storyindex,len(lines)))
            except:
                print('这个页面已经被小呆吞掉了哦')
        with open('4399Comic.txt','wb') as h:
            Storyindex=0
            for PPwrites in StoriesList:
                h.write('标题：'.encode('utf-8')+PPwrites['title'].encode('utf-8')+'\n\n'.encode('utf-8'))
                h.write('介绍：'.encode('utf-8')+PPwrites['discus'].encode('utf-8')+'\n\n'.encode('utf-8'))
                h.write('地址：'.encode('utf-8')+PPwrites['href'].encode('utf-8')+'\n\n'.encode('utf-8'))
                Storyindex+=1
                print('已经写入了%d/%d个漫画'%(Storyindex,len(lines)))

    def getEQG(link="http://www.4399er.com/xzt/xmblmh/"):
        EQGStations=urllib.request.urlopen(link)
        Htmls=BeautifulSoup(EQGStations.read().decode('utf-8'),'html.parser')
        lines=Htmls.ul.find_all("li")
        StoriesList=[]
        Storyindex = 0
        print('开始 获取小马国女孩中.....总共有%d个女孩。'%len(lines))
        for line in lines:
            try:
                story={'title':'','href':'','discus':''}
                storytab=line.find(name="a",class_="tit")
                story.update(title=storytab.get_text())
                story.update(href='http://www.4399er.com'+storytab['href'])
                discuss=urllib.request.urlopen(story['href'])
                discussoup=BeautifulSoup(discuss.read().decode('utf-8'),'html.parser')
                try:
                    discustext=discussoup.find(name='span',style="color: rgb(0, 128, 128);").get_text()
                    story.update(discus=discustext)
                except:
                    try:
                        discustext=discussoup.find(name='span',style="color: #008080").get_text()
                        story.update(discus=discustext)
                    except:
                        discustext='暂无'
                StoriesList.append(story)
                Storyindex+=1
                print('已经获取了%d/%d个女孩视频'%(Storyindex,len(lines)))
            except:
                print('这个页面已经被小呆吞掉了哦')
        with open('4399Comic.txt','wb') as h:
            Storyindex=0
            for PPwrites in StoriesList:
                h.write('标题：'.encode('utf-8')+PPwrites['title'].encode('utf-8')+'\n\n'.encode('utf-8'))
                h.write('介绍：'.encode('utf-8')+PPwrites['discus'].encode('utf-8')+'\n\n'.encode('utf-8'))
                h.write('地址：'.encode('utf-8')+PPwrites['href'].encode('utf-8')+'\n\n'.encode('utf-8'))
                Storyindex+=1
                print('已经写入了%d/%d个漫画'%(Storyindex,len(lines)))
if __name__ =='__main__':#测试运行程序
    #PonyCrawler4399.getmusic(mode=1)
    #PonyCrawler4399.getstories()
    #PonyCrawler4399.getcomic()
    PonyCrawler4399.getEQG()
    pass
