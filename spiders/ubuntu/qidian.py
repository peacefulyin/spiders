#coding=utf-8
import requests
from lxml import etree
import time
import threading

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"}


def getsbooks(offset):
    url = 'http://se.qidian.com/?kw=&vip=0&page='+str(offset)
    html = etree.HTML(requests.get(url,headers=headers).text)
    going = html.xpath("//div[@class='book-mid-info']//h4/a/@href")
    #print( going)
    for i in going:
        print( 'http:'+i)
        ghtml = etree.HTML(requests.get('http:'+i, headers=headers).text)
        book = ghtml.xpath("//a[@id='readBtn']/@href")
        title = ghtml.xpath("//h1/em/text()")[0]
        print( title)
        startcopy('http:'+book[0],title,0)

def startcopy(url,title,wrongNum):
    file = open(title+'.txt','a')
    #try:
    html = etree.HTML(requests.get(url,headers=headers).text)
    texts = html.xpath('//p/text()')
    text = '\n'.join(texts)
    file.write(text)
    nurl = 'http:' + html.xpath("//a[@id='j_chapterNext']/@href")[0]
    time.sleep(2)
    try:
        startcopy(nurl,title,wrongNum)
    except Exception:
        print( '出错')
        wrongNum+=1
        if wrongNum >4:
            return
        startcopy(nurl, title,wrongNum)



def main():
    for page in range(1,51):
        if page < 17:
            t1 = threading.Thread(target=getsbooks, args=(page,))
        if page < 34:
            t2 = threading.Thread(target=getsbooks, args=(page+17,))
        if page < 52:
            t3 = threading.Thread(target=getsbooks, args=(page+34,))

        t1.start()
        t2.start()
        t3.start()
        t1.join()
        t2.join()
        t3.join()
        #getsbooks(page)

if __name__ == '__main__':
    main()
