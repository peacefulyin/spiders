import requests
from lxml import etree
from bs4 import BeautifulSoup
import re
import time


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}


def geturls(i):
    url = 'http://www.zcool.com.cn/discover/0!0!0!0!0!!!!2!-1!'+str(i)
    print (url)
    content = requests.get(url,headers=headers).text
    html = etree.HTML(content)
    links = html.xpath("//div[@class='all-work-list']//a[@class='title-content exist-fire-class']/@href")
    going(links)

def going(links):
    for each in links:
        print(each)
        content = requests.get(each,headers=headers).text
        time.sleep(2)
        html = etree.HTML(content)
        if 'work' in each:
            print('work')
            title = html.xpath("//h2/text()")
            images = html.xpath("//div[@class='work-show-box']//img/@src")
        elif 'article' in each:
            print('article')
            images = html.xpath("//p[@style='text-align: center']/img/@src")
        else:
            print('未知')
        try:
            Dimages(images[0])
        except Exception as e:
            print(e)

def Dimages(img):
    image = requests.get(img,headers=headers).content
    with open(img[-8:],'wb') as f:
        f.write(image)




def main():
    for i in range(2,50):
        geturls(i)

if __name__ == '__main__':
    main()

artical = "//p[@style='text-align: center']/img/@src"
work = "//div[@class='work-show-box']//img/@src"