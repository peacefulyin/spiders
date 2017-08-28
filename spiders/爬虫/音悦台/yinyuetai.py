#coding=utf-8
import requests
from lxml import etree
import json
import time
from urllib import parse

"//ul[@class='mv-list']/li"
headers = {
    'Host':'mvapi.yinyuetai.com',
    'Connection':'keep-alive',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
    'Accept':'*/*',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
}

def getlinks():
    list = []
    url = "http://mvapi.yinyuetai.com/mvchannel/so?callback=success_jsonpCallback_so&sid=&tid=&a=&p=&c=&s=totalViews&pageSize=20&page=1"
    gets = requests.get(url,headers=headers).text
    index = gets.find('({')
    gets = gets[index+1:-1]
    print(gets)
    Json = json.loads(gets)
    for each in Json.get('result'):
        item = {}
        item["title"] = each.get('title')
        item["image"] = each.get('image')
        item["id"] = str(each.get('videoId'))
        item["url"] = 'http://v.yinyuetai.com/video/' + str(item["id"])
        list.append(item)
    return list

def getvideourl(itemlist):
    mvlist = []

    for item in itemlist[:3]:
        id = item.get('id')
        data = {
            'json': 'true',
            'position': 'preroll,overlay,bottompop',
            'ptp': 'mv',
            'rd': 'yinyuetai.com',
            'v2': 'true',
            'videoId': id,
        }
        data = parse.urlencode(data)
        url = 'http://www.yinyuetai.com/proment/get-play-medias?'+data
        headers = {
            'Host': 'www.yinyuetai.com',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'X-Requested-With': 'ShockwaveFlash/26.0.0.151',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        }
        gets = requests.get(url,headers=headers).text
        jsonstr = json.loads(gets)
        videourl = jsonstr.get('preroll')[0].get('url')
        item['videourl'] = videourl
        mvlist.append({id:item.get('title'),'url':videourl})
        time.sleep(2)
    print(mvlist,itemlist)
    return mvlist,itemlist


def getvideo(mvlist,items):
    for each in mvlist:
        for k,v in each.items():
            print('序号:',k,'mv:',v)
            break
    downNum = input('请输入要下载的序号:')
    for each in mvlist:
        item = each.get(downNum)
        if item:
            url =each.get('url')
            gets = requests.get(url,headers=headers).content
            with open(item+'.mp4','wb') as f:
                f.write(gets)









def main():
    itemlist = getlinks()
    mvlist,items = getvideourl(itemlist)
    getvideo(mvlist,items)

if __name__ == '__main__':
    main()