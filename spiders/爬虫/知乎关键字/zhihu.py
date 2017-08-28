#coding=utf-8
import requests
import urllib
import time
import re
import json
import random
from requests.exceptions import ProxyError
import csv
import codecs

url = 'https://www.zhihu.com/search?'
data = {}
with open('proxys.txt','r')as f:
    list = eval(f.read())

itemlist = []
key = ''


def getlinks(offset,key):
    print('获得关键字主页',offset)
    #取得网页链接
    headers = {
        'Host': 'www.zhihu.com',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    url = 'https://www.zhihu.com/r/search?'
    data = {
        'q': key,
        'correction': '1',
        'type': 'content',
        'offset': offset,
    }
    data = urllib.parse.urlencode(data)
    url = url + data
    gets = requests.get(url,headers=headers).text
    text = json.loads(gets)
    htmls = text.get('htmls')
    extracturl(htmls)
    offset+=20 #翻页
    print('网页翻页')
    getlinks(offset,key)
    #return htmls

def extracturl(htmls):
    print('正在处理html')
    #拿到帖子url
    urllist = set()
    findurl = re.compile(r'href="(.*?)"',re.S)
    for html in htmls:
        urls = findurl.findall(html)
        for each in urls:
            url = re.search('(/question/\d+/)',each)
            if url:
                #print(url.group(1))
                urllist.add(url.group(1))
    getcontent(urllist)
    #return urllist

def getcontent(urllist):
    global itemlist
    print('正在获取帖子api')
    #用帖子url组成api接口来拿取数据。
    for url in urllist:
        get_text(url) #取得内容
        print('下一个帖子',url)
        write_to_csv(itemlist)
        itemlist = []




def get_text(url):
    print('正在提取帖子第一页内容',url)
    #帖子内不断翻页取得内容
    num = re.search(r'(\d+)', url).group(1)
    # print(url)
    headers = {
        'Host': 'www.zhihu.com',
        'Connection': 'keep-alive',
        'accept': 'application/json, text/plain, */*',
        'X-UDID': 'ABDChsogQQyPTmjDvgZY7A3GLOjtr324xSI=',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
        'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
        # 'Referer:': 'https://www.zhihu.com' + url,
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    }
    proxies = random.choice(list)

    url = 'https://www.zhihu.com/api/v4/questions/%s/answers?' % num
    data = {
        'include': 'data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,upvoted_followees;data[*].mark_infos[*].url;data[*].author.follower_count,badge[?(type=best_answerer)].topics',
        'offset':'3',
        'limit': '20',
        'sort_by': 'default',
    }
    data = urllib.parse.urlencode(data)
    url = url + data
    gets = requests.get(url, headers=headers).text
    text = json.loads(gets)
    print('提取第一页内容')
    deal_text(text)  # 提取内容
    if not text.get('paging').get('is_end'):
        nexturl = text.get('paging').get('next')  # 获取翻页链接
        print('首个下一页链接',nexturl)
        #offset+=20
        print('正在进入翻页循环')
        get_next_text(nexturl)  #递归
    else:
        return
    time.sleep(random.randint(2,3))

def get_next_text(url):
    headers = {
        'Host': 'www.zhihu.com',
        'Connection': 'keep-alive',
        'accept': 'application/json, text/plain, */*',
        'X-UDID': 'AECCuVgMPAyPTp8MIKMkzp3rpgv5n2WEQF4=',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
        'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
        # 'Referer:': 'https://www.zhihu.com' + url,
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    }
    #proxies = random.choice(list)
    print('正在翻页',url)
    gets = requests.get(url, headers=headers).text
    text = json.loads(gets)
    print(text)
    print('提取内容')
    deal_text(text)  # 提取内容
    if not text.get('paging').get('is_end'):
        nexturl = text.get('paging').get('next')  # 获取翻页链接
        print('帖子下一页链接',nexturl)
        time.sleep(random.randint(2,3))
        get_next_text(nexturl)  # 递归
    else:
        print('该帖子爬取完毕')





def deal_text(text):
    global key
    for each in text.get('data'):
        item = {}
        titleinfo = []
        title = each.get('question').get('title')
        titleurl = each.get('question').get('url')
        titleauthor = each.get('question').get('author').get('name')
        titleauthorheadline = each.get('question').get('author').get('headline')
        titleinfo.append(title)
        titleinfo.append(titleauthor)
        titleinfo.append(titleauthorheadline)
        titleinfo.append(titleurl)
        item['文章信息'] = titleinfo
        item['姓名'] = each.get('author').get('name')
        item['签名'] = each.get('author').get('headline')
        item['性别'] = each.get('author').get('gender')
        author_avatar = each.get('author').get('avatar_url_template')
        item['头像链接'] = re.sub(r'{size}', 'xl', author_avatar)
        item['追随者数量'] = each.get('author').get('follower_count')
        item['key'] = each.get('author').get('url_token')
        item['api'] = each.get('author').get('url')
        content = each.get('content')
        item['评论数'] = each.get('comment_count')
        item['感谢数'] = each.get('thanks_count')
        item['点赞数'] = each.get('voteup_count')
        item['更新日期'] = each.get('updated_time')
        item['评论内容'] = re.sub(r'(<.*?>)', '', content)


        itemlist.append(item)
        print(item)

def write_to_csv(item):
    headers = ['文章信息','姓名','签名','性别','头像链接','追随者数量','key','api','评论数','感谢数','点赞数','更新日期','评论内容']
    rows = item
    with codecs.open('%s.csv'%key,'a','utf_8_sig') as f:
        f_csv = csv.DictWriter(f,headers)
        f_csv.writeheader()
        f_csv.writerows(rows)



def main():
    global key
    key = '戒色'
    text = getlinks(40,key)
    #urllist = extracturl(text)
    #getcontent(urllist)

if __name__ == '__main__':
    main()