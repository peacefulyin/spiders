import requests
import urllib

url = 'http://api-xl9-ssl.xunlei.com/sl/group_accel/motorcade_mem?'
data = {
'uid':'493627929',
'send_from':'web',
'group_id':'1759602',
'_uid':'493627929',
'_sessid':'6F8D250C527FD37F680F7097C6915B3A',
'_h[]':'Peer-Id:1C1B0D3E68A0QW7Q',
'_dev':'1',
'_callback':'_jsonpf7qd61x6a29gnoajbj9hehfr',
}
headers = {
'Host':'api-xl9-ssl.xunlei.com',
'Connection':'keep-alive',
'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36 Thunder/9.1.35.816 ThunderComponent/1.0.10.99',
'Referer':'http://pc.xunlei.com/racing',
'Accept-Language':'en-US,en;q=0.8',

}
data = urllib.urlencode(data)
nurl = url+data
gets = requests.get(nurl,headers=headers)
print gets.text