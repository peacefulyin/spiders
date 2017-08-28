#coding=utf-8
#!/usr/bin/env python

import urllib
import urllib2
from lxml import etree
import time

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"}


def getlink(url):
    global pn
    global add
    global headers

    request = urllib2.Request(url)
    html = urllib2.urlopen(request).read()
    content = etree.HTML(html)
    link_list = content.xpath('//div[@class="t_con cleafix"]/div/div/div/a/@href')
    for link in link_list:
        fullLink = "http://tieba.baidu.com" + link
        # 组合为每个帖子的链接
        loadImage(fullLink)

def loadImage(fullLink):
    #print fullLink
    request = urllib2.Request(fullLink)
    html = urllib2.urlopen(request).read()
    content = etree.HTML(html)
    text_link = content.xpath("//a[@class='p_author_face']/img/@src")
    for i in text_link:
        print i

    #link_list = content.xpath('//div[@class="post_bubble_middle"]')
    link_list = content.xpath('//img[@class="BDE_Image"]/@src')
    # 取出每个图片的连接
    for link in link_list:
        print link
        writeImage(link)

def writeImage(link):
    request = urllib2.Request(link)
    pic = urllib2.urlopen(request).read()
    with open(link[-10:],'wb')as f:
        f.write(pic)

def tiebaSpider(url, beginPage, endPage):
    """
        作用：贴吧爬虫调度器，负责组合处理每个页面的url
        url : 贴吧url的前部分
        beginPage : 起始页
        endPage : 结束页
    """
    for page in range(beginPage, endPage + 1):
        pn = (page - 1) * 50
        #filename = "第" + str(page) + "页.html"
        fullurl = url + "&pn=" + str(pn)
        #print fullurl
        getlink(fullurl)
        #print html

        print "谢谢使用"



def main():
    kw = raw_input("请输入需要爬取的贴吧名:")
    beginPage = int(raw_input("请输入起始页："))
    endPage = int(raw_input("请输入结束页："))

    url = "http://tieba.baidu.com/f?"
    key = urllib.urlencode({"kw": kw})
    url = url + key
    tiebaSpider(url, beginPage, endPage)





if __name__ == '__main__':

    main()