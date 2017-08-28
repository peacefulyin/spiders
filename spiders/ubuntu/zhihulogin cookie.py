from bs4 import BeautifulSoup
import requests
from lxml import etree

url = 'https://www.zhihu.com/people/a-dong-62-98/activities'

headers = {
"Host":"www.zhihu.com",
"Connection":"keep-alive",
"Origin":"https://www.zhihu.com",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
"X-Requested-With":"XMLHttpRequest",
"X-Xsrftoken":"996d46bb-19f3-411b-abc1-df8190c1b244",
"Referer":"https://www.zhihu.com/",
"Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",
}

sess = requests.session()
gets = sess.get(url,headers=headers)
newurl = 'https://www.zhihu.com/question/30602857/answer/201941986'
newgets = sess.get(newurl,headers=headers)
html = etree.HTML(newgets.text)
print newgets.text
content = html.xpath("//div[@class='RichContent-inner']//p/text()")[0]
print content