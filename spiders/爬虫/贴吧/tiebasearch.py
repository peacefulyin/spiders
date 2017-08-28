#coding=utf-8
import requests
import time
from bs4 import BeautifulSoup
#from queue import Queue
import csv
import codecs
from multiprocessing import Process,Queue
from threading import Lock
from queue import Queue



linkurls = Queue()
articalurls = Queue()
lock = Lock()


def getlinks(url):
    gets = requests.get(url).text
    soup = BeautifulSoup(gets,'lxml')
    htmls = soup.select('.j_th_tit')
    nextpage = 'https:'+soup.select('.next')[0].get('href')
    for each in htmls:
        try:
            url = each.a.get('href')
            linkurls.put(url)
            print('存入链接',url)
            getinfo(1)
            time.sleep(2)
        except Exception:
            pass
    print('贴吧下一页')
    time.sleep(3)
    getlinks(nextpage)


def getinfo(pn):
    if not linkurls.empty():
        url = 'http://tieba.baidu.com'+linkurls.get()+'?pn=%s'%str(pn)
        print('取出链接',url)
        gets = requests.get(url).text
        soup = BeautifulSoup(gets, 'lxml')
        articalurls.put(soup)
        print('怎么了?')
        parse_link()
        total = soup.select('.red')[1].text
        total = int(total)
        if pn < total:
            pn += 1
            print('帖子下一页',pn)
            getinfo(pn,linkurls,articalurls)
        print(total)
        time.sleep(3)
    else:
        print('等待榨取帖子链接')
        time.sleep(3)

def parse_link():
    print('来了吗')
    if not articalurls.empty():
        soup = articalurls.get()
        print('取出内容',soup[0:100])
        for each in soup.select('#j_p_postlist > div'):
            item = {}
            item['name'] = each.select('.p_author_face')[0].img.get('username')
            item['img'] = each.select('.p_author_face')[0].img.get('src')
            item['url'] = each.select('.p_author_face')[0].get('href')
            item['content'] = each.select('.d_post_content')[0].text
            #item['comment'] = each.select('.j_lzl_m_w > *').text
            print(item)
    else:
        print('等待榨取内容')
        time.sleep(3)
'#j_p_postlist > div:nth-child(1) > div.d_author > ul > li.d_name > a'



def main():
    url = 'https://tieba.baidu.com/f?kw=搞笑'
    getlinks(url)

if __name__ == '__main__':
    main()