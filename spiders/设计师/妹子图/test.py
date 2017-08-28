import requests

url = 'http://i.meizitu.net/2017/08/20b01.jpg'
# url = 'https://www.baidu.com'
proxies = {'http': 'http://182.35.95.176:8118'}

headers = {
    'Host': 'i.meizitu.net',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
    'Referer': 'http://www.mzitu.com/100462',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Languge': 'zh-CN,zh;q=0.8,en;q=0.6',
}

gets = requests.get(url, headers=headers).content
with open('1.jpg', 'wb') as f:
    f.write(gets)
