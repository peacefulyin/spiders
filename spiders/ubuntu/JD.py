#coding=utf-8
import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from pyquery import PyQuery as pq
from jdConfig import *
import pymongo
import time

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
browser = webdriver.Chrome()
wait = WebDriverWait(browser,10)
browser.maximize_window()

def search():
    print ('正在搜索')
    try:
        browser.get('https://www.jd.com/')
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#key')))

        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#search > div > div.form > button')))
        input.send_keys(KEYWORD)
        submit.click()
        total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#J_bottomPage > span.p-skip > em:nth-child(1) > b')))
        get_products()
        return total.text

    except TimeoutException:
        print ('重新搜索')
        return search()

def next_page(page_number):
    print ('正在翻页'+'\n')
    try:
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#J_bottomPage > span.p-skip > input')))
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#J_bottomPage > span.p-skip > a')))
        input.clear()
        input.send_keys(page_number)
        submit.click()
        wait.until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR,'#J_bottomPage > span.p-skip > input'),str(page_number)))
        time.sleep(2)
        get_products()
    except TimeoutException:
        print "翻页错误"
        return next_page(page_number)

def get_products():
    print ('正在存储')
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.gl-warp .gl-item .gl-i-wrap .p-img')))
    html = browser.page_source
    doc = pq(html)
    items = doc('.gl-warp .gl-item .gl-i-wrap').items()
    for item in items:
        products = {
            'image':item.find('.p-img .err-product').attr('src'),
            'price':item.find('.p-price').text(),
            'commit':item.find('.p-commit a').text(),
            'title':item.find('.p-name').text(),
            'shop':item.find('.p-shop').text(),
        }
        save_tomongo(products)

def save_tomongo(products):
    try:
        if db[MONGO_TABLE].insert(products):
            print ('存储到mongo成功',products)
    except Exception:
        print ('存储到mongo失败',products)



def main():
    try:
        total = search()
        total = int(total)
        print total
        for i in range(2,total+1):
            next_page(i)
    except Exception:
        print ('出现错误')

    finally:
        browser.close()



if __name__ == '__main__':
    main()


