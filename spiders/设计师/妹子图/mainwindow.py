import os
import shutil
import time

import requests
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import *
from designer import Ui_MainWindow
from lxml import etree


class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    _signal = QtCore.pyqtSignal(str)  # 定义信号,定义参数为str类型

    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        #palette1 = QtGui.QPalette()
        #palette1.setColor(self.backgroundRole(), QColor(192, 253, 123))
        #self.setPalette(palette1)
        self.pagenum = 1
        self.urlnum = 0
        self.headers = {
            'Host': 'www.mzitu.com',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',

        }
        self.log.setText('正在启动')
        self.links = self.geturls(1)
        self.log.setText('启动完毕，可以点击开始了')
        self.showlist = []
        self.showing = ''
        self.nowurl = ''

    @QtCore.pyqtSlot()
    def on_down_clicked(self):
        print(len(self.links))
        lenth = len(self.links)
        if self.urlnum < lenth:
            url = self.links[self.urlnum]
            self.nowurl = url
            print('url',url)
            time.sleep(5)
            images = []
            for j in range(1, 4):
                gets = requests.get(self.links[self.urlnum] + '/' + str(j))
                html = etree.HTML(gets.text)
                title = html.xpath("//h2/text()")[0]
                image = html.xpath("//div[@class='main-image']//img/@src")[0]
                images.append(image)
            print(images)
            self.Dimages(images,url)
            #self.title.setText(title)
            self.log.setText('完毕，请预览',title)

        else:
            self.urlnum = 0
            self.pagenum += 1
            self.links = self.geturls(self.pagenum)

    @QtCore.pyqtSlot()
    def on_next_clicked(self):
        try:
            index = self.showlist.index(self.showing)
            if index < len(self.showlist)-1:
                pixmap = QPixmap(self.showlist[index+1]).scaled(self.label.width(), self.label.height())
                self.label.setPixmap(pixmap)
                now = index + 1
                self.now.setText('正在%s' % str(now+1))
                self.showing = self.showlist[index+1]
                print(self.showing)
        except Exception as e:
            print(e)


    @QtCore.pyqtSlot()
    def on_prev_clicked(self):
        try:
            index = self.showlist.index(self.showing)
            if index > 0 :
                pixmap = QPixmap(self.showlist[index - 1]).scaled(self.label.width(), self.label.height())
                self.label.setPixmap(pixmap)
                now = index + 1
                self.now.setText('正在%s' % str(now-1))
                self.showing = self.showlist[index - 1]
                print(self.showing)
        except Exception as e:
            print(e)

    @QtCore.pyqtSlot()
    def on_change_clicked(self):
        try:
            self.now.clear()
            self.urlnum +=1
            try:
                self.remove()
            except Exception as e:
                print(e,'pass')
            self.showlist = []
            self.showing = ''
            self.on_down_clicked()
        except Exception as e:
            print(e)


    @QtCore.pyqtSlot()
    def on_save_clicked(self):
        self.log.setText('正在保存')
        print(self.showing)
        str = self.nowurl[-6:]
        if not os.path.exists('./imgs/'+str):
            os.mkdir('./imgs/'+str)
        for each in self.showlist:
            shutil.copyfile(each, './imgs/'+str+'/'+each)
        self.log.setText('保存完毕')
        self.remove()

    def remove(self):
        for each in self.showlist:
            os.remove(each)



    @QtCore.pyqtSlot()
    def on_showimg_clicked(self):
        try:
            pixmap = QPixmap(self.showlist[0]).scaled(self.label.width(), self.label.height())
            self.showing = self.showlist[0]
            self.now.setText('正在%s'%str(1))
            self.label.setPixmap(pixmap)
        except Exception as e:
            print(e)

    def geturls(self,page):
            url = 'http://www.mzitu.com/page/%d' % page
            gets = requests.get(url, headers=self.headers)
            html = etree.HTML(gets.text)
            links = html.xpath("//div[@class='postlist']//li/a/@href")
            return links

    def Dimages(self,urls,i):
        headers = {
            'Host': 'i.meizitu.net',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'Referer': i,
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        }
        num = 0
        for url in urls:
            print(url)
            image = requests.get(url, headers=headers).content
            if url.endswith('jpeg'):
                with open(str(num) + url[-5:], 'wb') as f:
                    text = str(num) + url[-5:]
                    self.showlist.append(text)
                    f.write(image)
                    num += 1
            else:
                with open(str(num)+url[-4:], 'wb') as f:
                    text = str(num)+url[-4:]
                    self.showlist.append(text)
                    f.write(image)
                    num += 1
                self.total.setText('总页面%s'%str(len(self.showlist)))
                self.log.setText('图片加载完毕')
                #self.deal_img()

    """
    def deal_img(self):
        for each in self.showlist:
            img = Image.open(each)
            w, h = img.size
            img.resize((960, 640))
            img.save(each)
    """







if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = MyWindow()
    ui.show()
    sys.exit(app.exec_())





