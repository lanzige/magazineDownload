#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author duzy
# @Time      : 2020/2/13 21:36
# @Author    : duzy
# @File      : downloadInfo.py
# @Software  : PyCharm
import requests
from requests.exceptions import RequestException
from pyquery import PyQuery as pq
import html
import re
import time
class scrpy():
    def getHtml(self,url):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}
        try:
            response = requests.get(url, headers=headers, timeout=20)
            if response.status_code == 200:
                return html.unescape(response.text)
            return None
        except RequestException:
            print('读取网页源码失败')
            return None


    def readHtml(self,html, content, **kwargs):
        if kwargs is None:
            return None
        # 解析html字符串
        doc = pq(html)
        its = doc(content).items()
        result = []
        if 'text' in kwargs:
            if kwargs['text'] == 'True':
                for item in its:
                    result.append(item.text())
        elif 'attr' in kwargs:
            for item in its:
                result.append(item.attr(kwargs['attr']))
        return result


    def getIndex(self):
        url = 'https://www.hanspub.org/'
        html = self.getHtml(url)
        if html:
            names = self.readHtml(html, '.left_uesrc li', text='True')
            srcs = self.readHtml(html, '.left_uesrc a', attr='href')
            links = []
            for src in srcs:
                links.append('https:'+src)
            info = list(zip(names, links))
            return info
        else:
            print('html is None')
            return None

    def getChildPage(self,url):
        example = 'url Example:https://www.hanspub.org/5.shtml'
        info = []
        pattern = re.compile(r'(\d).shtml')
        result = pattern.findall(url)
        index = result[0]
        realUrl = F'https://www.hanspub.org/CategoryOfJournal.aspx?CategoryID={index}&page='
        for i in range(1,200):
            realUrl = realUrl+str(i)
            html =self.getHtml(realUrl)
            childtexts = self.readHtml(html,'.jonBox ul li a',text='True')
            childhrefs = self.readHtml(html,'.jonBox ul li a',attr='href')
            childtexts = childtexts[::2]
            childhrefs = childhrefs[::2]
            childhrefs_new = []
            for href in childhrefs:
                childhrefs_new.append('https:'+href)
            info.extend(list(zip(childtexts,childhrefs_new)))
            if len(childtexts) != 10:
                break
            time.sleep(5)
        return info

    def getMagzineList(self,url):
        example = 'https://www.hanspub.org/journal/BP.html'
        html = self.getHtml(url)
        childtext = self.readHtml(html,'.tabMain ul .xh a',text='True')
        childsrcs = self.readHtml(html, '.tabMain ul li span a', attr='href')
        childsrcs_new = []
        for src in childsrcs:
            childsrcs_new.append('https:'+src)
        info = list(zip(childtext,childsrcs_new))
        return info

    def downloadMagzine(self,name,url):
        r = requests.get(url,stream=True)
        if r.status_code == 200:
            name = name.split('\n')[0]
            with open(F'download/{name}.pdf','wb') as wfile:
                for chunk in r.iter_content(chunk_size=512):
                    if chunk:
                        wfile.write(chunk)
        else:
            print('Download encounter error!')




if __name__ == '__main__':
    sy = scrpy()
    sy.downloadMagzine('一个四维混沌的广义发电机系统的动力学分析',r'https://www.hanspub.org/DownLoad/Page_DownLoad.aspx?FileName=PM20200200000_32695538.pdf')