#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author duzy
# @Time      : 2020/2/13 20:12
# @Author    : duzy
# @File      : MyWindow.py
# @Software  : PyCharm
import sys
import magazineDownload.mainUI as mainui
from PyQt5.QtWidgets import QApplication, QWidget, QTreeWidgetItem
from PyQt5.QtCore import pyqtSignal, QObject, QThread
from magazineDownload.downloadInfo import scrpy
import re


class AddWork(QObject):
    addSignal = pyqtSignal(str)

    def __init__(self, parentItem, type, url=None):
        super(AddWork, self).__init__()
        # super().__init__()
        self.type = type
        self.parentItem = parentItem
        self.scy = scrpy()
        self.url = url

    def work(self):
        print('1')
        if self.type == 'top':
            data = self.scy.getIndex()
            self.addSignal.emit('正在读取目录数据')
        elif self.url is not None:
            if self.type == 'second':
                data = self.scy.getChildPage(self.url)
                self.addSignal.emit('正在读取次级目录数据')
            elif self.type == 'three':
                data = self.scy.getMagzineList(self.url)
                self.addSignal.emit('正在读取文章目录数据')
        else:
            self.addSignal.emit('传入数据不正确，请修改后重试')
            return
        for item in data:
            self.addSignal.emit('正在在显示目录插入数据')
            node = QTreeWidgetItem(self.parentItem)
            node.setText(0, item[0])
            node.setText(1, item[1])
            self.addSignal.emit('显示完成')


class DownloadWork(QObject):
    downSignal = pyqtSignal(str)

    def __init__(self, name, url):
        super(DownloadWork, self).__init__()
        self.url = url
        self.scy = scrpy()
        self.name = name

    def work(self):
        self.downSignal.emit('正在下载文章...')
        self.scy.downloadMagzine(self.name, self.url)
        self.downSignal.emit('下载完成')


class MyWin(QWidget, mainui.Ui_Form):
    def __init__(self, parent=None):
        super(MyWin, self).__init__(parent)
        self.setupUi(self)
        self.top = []
        self.second = set()
        self.three = set()
        self.InitWin()

    def InitWin(self):
        self.rootNode = QTreeWidgetItem(self.treeWidget)
        self.rootNode.setText(0, '总目录')
        self.rootNode.setText(1, 'root')

        self.treeWidget.setColumnCount(1)
        self.treeWidget.setHeaderLabels(['名字'])
        self.treeWidget.addTopLevelItem(self.rootNode)
        self.treeWidget.clicked.connect(self.onTreeClicked)
        self.treeWidget.doubleClicked.connect(self.onTreeDoubleClicked)
        self.pushButton.clicked.connect(self.ButtonReadData)

        self.threadList = []
        self.workers = []

        self.show()

    def ButtonReadData(self):
        if self.rootNode.childCount() != 0:
            return
        worker = AddWork(self.rootNode, 'top')
        worker.addSignal.connect(self.ShowLog)

        thread = QThread()
        print('ready start button thread')
        thread.start()
        print('end start button thread')
        worker.moveToThread(thread)
        thread.started.connect(worker.work)
        self.threadList.append(thread)
        self.workers.append(worker)


    def onTreeClicked(self, qmodelindex):
        item = self.treeWidget.currentItem()
        self.ShowLog("key=%s ,value=%s" % (item.text(0), item.text(1)))

    def onTreeDoubleClicked(self, qmodelindex):
        item = self.treeWidget.currentItem()
        if item.childCount() != 0:
            return
        if item == self.rootNode:
            return
        print(item.text(1))
        if item.text(1).endswith('pdf'):
            print('This Is A Wz')
            print('download,start download thread')
            worker = DownloadWork(item.text(0), item.text(1))
            worker.downSignal.connect(self.ShowLog)

            thread = QThread()
            worker.moveToThread(thread)
            thread.started.connect(worker.work)
            thread.start()
            self.threadList.append(thread)
            self.workers.append(worker)
            return
        parten = re.compile('.*?\/\d\.shtml')
        if parten.search(item.text(1)):
            worker = AddWork(item, 'second', item.text(1))
            worker.addSignal.connect(self.ShowLog)

            thread = QThread()
            worker.moveToThread(thread)
            thread.started.connect(worker.work)
            thread.start()
            self.threadList.append(thread)
            self.workers.append(worker)
        else:
            worker = AddWork(item, 'three', item.text(1))
            worker.addSignal.connect(self.ShowLog)

            thread = QThread()
            worker.moveToThread(thread)
            thread.started.connect(worker.work)
            thread.start()
            self.threadList.append(thread)
            self.workers.append(worker)

    def ShowLog(self, text):
        self.logEdit.append(text)
        width = 6
        self.logEdit.append('=' * width)


if __name__ == '__main__':
    myapp = QApplication(sys.argv)
    myMainWin = MyWin()
    sys.exit(myapp.exec_())
