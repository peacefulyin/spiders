#coding=utf-8
import requests
from lxml import etree

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}

def getlinks():
    url = 'http://www.nlp.cn/xltest/page/1'
    content = requests.get(url,headers=headers).text
    html = etree.HTML(content)
    links = html.xpath("//article[@class='art_list']//p//a/@href")
    getText(links)

def getText(links):
    list = []
    for each in links:
        item = {}
        content = requests.get(each, headers=headers).text
        html = etree.HTML(content)
        item['title'] = html.xpath("//h1/text()")[0]
        item['text'] =  html.xpath("//div[@class='contents_show']//span/text()")
        list.append(item)
    with open('test.txt','wb') as f:
        f.write(str(list))


def main():
    getlinks()

if __name__ == '__main__':
    main()