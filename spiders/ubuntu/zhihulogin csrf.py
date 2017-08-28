import requests
import urllib
import re
from bs4 import BeautifulSoup

headers = {
'Host':'www.zhihu.com',
'Connection':'keep-alive',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
'X-Requested-With':'XMLHttpRequest',
'Referer':'https://www.zhihu.com/',
'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
}
sess = requests.session()


def xsrf():
    url = 'https://www.zhihu.com/#signin'
    content = sess.get(url,headers=headers).text
    soup = BeautifulSoup(content,'lxml')
    _xsrf = soup.find('input',attrs={'name':'_xsrf'}).get('value')
    login(_xsrf)

def login(_xsrf):
    url = 'https://www.zhihu.com/login/phone_num '
    data = {
        '_xsrf': _xsrf,
        'captcha_type': 'cn',
        'password': '...',
        'phone_num': '...',
    }
    data = urllib.urlencode(data)
    content = requests.post(url,data,headers=headers).text
    print content


def main():
    xsrf()


if __name__ == '__main__':
    main()