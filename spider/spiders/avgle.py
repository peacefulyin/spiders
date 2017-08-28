#coding=utf-8
import requests
import urllib
from lxml import etree
import re



num = 1


def getlinks(page):
    headers = {
        'Host': 'avgle.com',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://avgle.com/videos?o=mv',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    }
    url = 'https://avgle.com/videos?o=mv&page='+str(page)
    gets = requests.get(url,headers=headers).text
    html = etree.HTML(gets)
    for each in html.xpath("//div[@class='col-md-9 col-sm-8']//div[@class='row']//div[@class='well well-sm']"):
        getvideo(each)

def getvideo(each):
    global num
    title = each.xpath(".//img/@title")[0]
    mp4url = each.xpath(".//img/@data-original")[0].replace('1.jpg','preview.mp4')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    }
    mp4 = requests.get(mp4url, headers=headers, stream=True)
    with open('./mp4/'+str(num)+'.mp4', 'wb')as f:
        for chunk in mp4.iter_content(512):
            f.write(chunk)
    num+=1


def main():
    for page in range(1,20):
        getlinks(page)


if __name__ == '__main__':
    main()