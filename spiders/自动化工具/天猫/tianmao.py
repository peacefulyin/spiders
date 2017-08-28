#coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from pyquery import PyQuery as pq
import pymongo
import time
import random
import codecs

from lxml import etree
import csv

MONGO_URL = 'localhost'
MONGO_DB = 'taobao'
MONGO_TABLE = 'maotai'

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

SERVICE_ARGS = ['--load-images=false','--disk-cache=true']

browser = webdriver.Chrome(executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
options = webdriver.ChromeOptions()
#options.add_argument("'Cookie' = 'pnm_cku822=231UW5TcyMNYQwiAiwQRHhBfEF8QXtHcklnMWc%3D%7CUm5Ockp3SXVLf0R%2FS3ZNcCY%3D%7CU2xMHDJ7G2AHYg8hAS8UKQcnCVU0Uj5ZJ11zJXM%3D%7CVGhXd1llXWBeYlxoU2hcYVpnUG1PekV9Rn5Df0tyRn9Ae0N4VgA%3D%7CVWldfS0TMwwwBSUbOxUlTjIcShw%3D%7CVmhIGCUFOBgkEC0TMw04ADoaJhItEDAMMQQ5GSURLhMzDzILNmA2%7CV25Tbk5zU2xMcEl1VWtTaUlwJg%3D%3D; cq=ccp%3D0; _tb_token_=e683ebee85e1e; ck1=; uc1=cookie14=UoTcDNt4fVz%2BTg%3D%3D&lng=zh_CN&cookie16=U%2BGCWk%2F74Mx5tgzv3dWpnhjPaQ%3D%3D&existShop=false&cym=1&cookie21=VT5L2FSpczFp&tag=8&cookie15=WqG3DMC9VAQiUQ%3D%3D&pas=0; uc3=sg2=W5iWHPI7JVWNacIu2UE7NGvqwPtj3t6D1Y91%2FtSRPUs%3D&nk2=GgIKwHsFXEOCsA%3D%3D&id2=UoncijBC459k&vt3=F8dBzWXe5%2F4GKoAINlQ%3D&lg2=URm48syIIVrSKA%3D%3D; lgc=yinweiqiab; tracknick=yinweiqiab; cookie2=1cd1b7eb2ec4a22519f2e59cfbb4a587; cookie1=UteFRKjYzy1RM2tYGSZsUcGfr0TBF%2BgICpwRP%2F4rw7U%3D; unb=187347289; t=d49e83d6e5b6168d0ee0193f34dfa486; skt=0a20435a23cd9b4b; _nk_=yinweiqiab; _l_g_=Ug%3D%3D; cookie17=UoncijBC459k; hng=CN%7Czh-CN%7CCNY%7C156; uss=BxNQXjwbF9ihs1wgZqTKWjWIcbHmcGqVct6vOJ57QTjwwrA0T57BfPytRA%3D%3D; login=true; cna=; isg=Ai4udNFA-4Es1w9r9ENLdB2sf4Qwh_NMOS1ryVj3uzHsO8-VwL6xOE99hZEs'")
#browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
#browser.set_window_size(1400,900)
wait = WebDriverWait(browser,10)

list = []


def search():
    print('正在搜索')
    url = 'https://xiaomi.tmall.com/search.htm'
    try:
        browser.get(url)
        #input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"#mq")))
        #submit =  wait.until(EC.element_to_be_clickable((By.XPATH,"//a[@class='page-cur']/following::a[1]")))
        #input.send_keys(MONGO_TABLE)
        #total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"#content > div.main > div.ui-page > div > b.ui-page-skip > form")))
        #get_products()
        #return total.text
        #url = browser.current_url
        #get_detail()
        #browser.get(url)
        nextpage()
    except TimeoutError:
        browser.get(url)

def nextpage():
    while True:
        submit = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@class='page-cur']/following::a[1]")))
        url = submit.get_attribute('href')
        print(submit.get_attribute('href'))
        if submit.get_attribute('class') == 'J_SearchAsync':
            get_detail()
            browser.get(url)
            #submit.click()
        else:
            break
        time.sleep(5)


def get_detail():
    print('正在',browser.current_url)
    urls = []
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,".J_TItems .item")))
    html = browser.page_source
    doc = pq(html)
    items = doc('.J_TItems .item').items()
    for item in items:
        url = item.find('.photo a').attr('href')
        if url:
            urls.append(url)
    getinto(urls)
    #return urls


def getinto(urls):
    num = 0
    for url in urls:
        if num < 4:
            print(url)
            url = 'https:'+url
            browser.get(url)
            get_products(url)
            time.sleep(random.randint(3,4))
            num+=1


def get_products(url):
    item = {}
    html = browser.page_source
    text = etree.HTML(html)
    some = text.xpath("//ul[@id='J_AttrUL']/li/text()")
    param = ';'.join(some)

    shopinfo = text.xpath("//meta[@name='microscope-data']/@content")[0]
    shopid = re.search(r'shopId=(\d+)',shopinfo).group()
    itemid = text.xpath("//input[@name='rootCatId']/@value")[0]

    items1 = text.xpath('//div[@class="tb-wrap"]')
    for each in items1:
        item['标题'] = each.xpath('.//div[@class="tb-detail-hd"]/h1/text()')[0].replace('\t','').replace('\n','').strip()
        item['说明'] = each.xpath('.//div[@class="tb-detail-hd"]/p/text()')[0].replace('\t','').replace('\n','').strip()
        try:
            item['价格'] = each.xpath('.//dl[@class="tm-price-panel tm-price-cur"]//span/text()')[0].replace('\t','').replace('\n','').strip()
        except Exception:
            item['价格'] = each.xpath('.//dl[@class="tm-price-panel"]//span[@class="tm-price"]/text()')[0].replace('\t','').replace('\n','').strip()

        item['链接'] = url
        item['人气'] = 'nothing'
        item['地址'] = each.xpath('.//div[@class="tb-postAge"]//span/text()')[0].replace('\t','').replace('\n','').strip()
        item['销量数'] = each.xpath('.//div[@class="tm-indcon"]//span[2]/text()')[0].replace('\t','').replace('\n','').strip()
        item['评论数'] = each.xpath('.//div[@class="tm-indcon"]//span[2]/text()')[1].replace('\t','').replace('\n','').strip()
        try:
            kucun = each.xpath('.//em[@class="tb-hidden"]/text()')[0].replace('\t','').replace('\n','').strip()
            item['库存'] = re.search(r'(\d+)',kucun).group()
        except Exception:
            item['库存'] = '0'
        item['商品ID'] = itemid
        item['店铺ID'] = shopid
        item['参数'] = param
        print(item)
        list.append(item)


def write_to_csv(item):
    headers = ['标题','说明','价格','链接','人气','地址','销量数','评论数','库存','商品ID','店铺ID','参数']
    rows = item
    with codecs.open('xiaomi.csv','wb','utf_8_sig') as f:
        f_csv = csv.DictWriter(f,headers)
        f_csv.writeheader()
        f_csv.writerows(rows)

"""
def save_to_mongo(item):
    try:
        if db[MONGO_TABLE].insert(item):
            print('save success')
    except Exception:
        print('save to mongo error')
"""



def main():
    try:
        search()
        #urls = get_detail()
        #getinto(urls)
        write_to_csv(list)
        client.close()
        browser.close()
    except Exception:
        print('程序出错,继续写入')
        write_to_csv(list)



if __name__ == '__main__':
    main()