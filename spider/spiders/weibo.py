'http://weibo.com/6066480974/profile?topnav=1&wvr=6'
import urllib
import requests

data = {
'service':'miniblog',
'servertime':'1501828050',
'nonce':'Y0T6M4',
'pwencode':'rsa2',
'rsakv':'1330428213',
'sp':'066c2d8851d13b4bbd84241bd495ba87e1c94e64d80571957fe97bccb00165dcc9dab7194629fca23d2e3c30d06a3bafe42d7ffc5cf46412516001354ce97b0eeea571df9d7f673ae5d615a0e40b8861eafb5ca3a25766e7a6d95d973a36974dc75af7c2f5a1f65ca078200e6cd250d1dd1da1b12a961410b452de3ff9e41b95',
'sr':'1920*1080',
'encoding':'UTF-8',
'prelt':'722',
'url':'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
'returntype':'META',
}

headers = {
'Host':'login.sina.com.cn',
'Connection':'keep-alive',
'Cache-Control':'max-age=0',
'Origin':'http://weibo.com',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
'Content-Type':'application/x-www-form-urlencoded',
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Referer':'http://weibo.com/',
'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',

}

data = urllib.urlencode(data)
sess = requests.session()
gets = requests.get(url)

