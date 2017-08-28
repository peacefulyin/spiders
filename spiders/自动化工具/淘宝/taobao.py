#coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from pyquery import PyQuery as pq
import pymongo
import sy
reload(sys)
sys.setdefaultencoding('utf8')

MONGO_URL = 'localhost'
MONGO_DB = 'taobao'
MONGO_TABLE = 'python'

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

SERVICE_ARGS = ['--load-images=false','--disk-cache=true']

#browser = webdriver.Chrome(executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
browser.set_window_size(1400,900)
wait = WebDriverWait(browser,10)




def search():
    print('正在搜索')
    try:
        browser.get('https://www.taobao.com/')
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"#q")))
        submit =  wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#J_TSearchForm > div.search-button > button")))
        input.send_keys(MONGO_TABLE)
        submit.click()
        total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"#mainsrp-pager > div > div > div > div.total")))
        get_products()
        return total.text
    except TimeoutError:
        return search()

def next_page(page_number):
    print('正在翻页',page_number)
    try:
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > input")))
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit")))
        input.clear()
        input.send_keys(page_number)
        submit.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,"#mainsrp-pager > div > div > div > ul > li.item.active > span"),str(page_number)))
        get_products()
    except TimeoutError:
        next_page(page_number)

def get_products():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"#mainsrp-itemlist .items .item")))
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'img':item.find('.pic .img').attr('src'),
            'price':item.find('.price').text(),
            'deal':item.find('.deal-cnt').text()[:-3],
            'title': item.find('.title').text(),
            'location': item.find('.location').text()
        }
        save_to_mongo(product)

def save_to_mongo(item):
    try:
        if db[MONGO_TABLE].insert(item):
            print('save success')
    except Exception:
        print('save to mongo error')
def main():
    try:
        total = search()
        total = int(re.compile(r'(\d+)').search(total).group(1))
        for i in range(2,total+1):
            next_page(i)
    except Exception:
        print('有地方出错')
    finally:
        client.close()
        browser.close()

if __name__ == '__main__':
    main()