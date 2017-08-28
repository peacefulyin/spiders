import os
import shutil

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
        self.pagenum = 3
        self.urlnum = 0
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
        self.log.setText('正在启动')
        self.links = self.geturls(2)
        self.log.setText('启动完毕')
        self.showlist = []
        self.showing = ''

    @QtCore.pyqtSlot()
    def on_down_clicked(self):
        print(len(self.links))
        lenth = len(self.links)
        if self.urlnum < lenth:
            self.log.setText('正在下载')
            content = requests.get(self.links[self.urlnum], headers=self.headers).text
            print(self.links[self.urlnum])
            print('到这了吗')
            html = etree.HTML(content)
            if 'work' in self.links[self.urlnum]:
                print('work')
                self.head = html.xpath("//h2/text()")[0].strip()
                self.title.setText(self.head)
                images = html.xpath("//div[@class='work-show-box']//img/@src")
            elif 'article' in self.links[self.urlnum]:
                print('article')
                images = html.xpath("//p[@style='text-align: center']/img/@src")
            else:
                print('未知')
            try:
                self.Dimages(images)
                self.log.setText('加载完毕')
                print(images)
            except Exception as e:
                print(e)
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
        self.log.setText('正在切换')
        try:
            self.now.clear()
            self.urlnum +=1
            try:
                self.remove()
            except Exception as e:
                print(e)
            self.showlist = []
            self.showing = ''
            self.on_down_clicked()
        except Exception as e:
            print(e)


    @QtCore.pyqtSlot()
    def on_save_clicked(self):
        self.log.setText('正在保存')

        print(self.head)
        if not os.path.exists('./imgs/'+self.head):
            os.mkdir('./imgs/'+self.head)
        for each in self.showlist:
            shutil.copyfile(each, './imgs/'+self.head+'/'+each)
        self.remove()
        self.log.setText('保存完毕')

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

    def Dimages(self,urls):
        num = 0

        for url in urls:
            image = requests.get(url, headers=self.headers).content
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


    def geturls(self,i):
        url = 'http://www.zcool.com.cn/discover/0!0!0!0!0!!!!2!-1!' + str(i)
        #print(url)
        content = requests.get(url, headers=self.headers).text
        html = etree.HTML(content)
        links = html.xpath("//div[@class='all-work-list']//a[@class='title-content exist-fire-class']/@href")
        return links




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = MyWindow()
    ui.show()
    sys.exit(app.exec_())





