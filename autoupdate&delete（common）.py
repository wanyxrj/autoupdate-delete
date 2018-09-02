#!/usr/bin/python
#coding=utf-8
import urllib
import urllib2
import time
import datetime
import re
import os
from bs4 import BeautifulSoup

#######download schedule, not in use yet
def Schedule(a, b, c):
    '''''
    A:已经下载的数据块
    B:数据块的大小
    C:远程文件的大小
   '''
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
        #print '%.2f%%' % per
        print "download complete"


#######file list
FILELIST = {
    "download path":"url",
    "/var/www/html/uploads/、聊天工具/wechat/":"https://pc.qq.com/detail/8/detail_11488.html",
    ... ...
}

#######auto update
FILEPATH = FILELIST.keys()
for i in range(len(FILEPATH)):
    FILEURL = FILELIST[FILEPATH[i]]
    page = urllib2.urlopen(FILEURL)
    contents = page.read()
    soup = BeautifulSoup(contents, 'html.parser')
    for url in soup.find_all(href=re.compile(".*exe$"), text='普通下载'):
        m_url = url.get("href")
        LIST = m_url.split('/')
        LIST.reverse()
        filename = LIST[0]
        path = FILEPATH[i]
        for root, dirs, files in os.walk(path):
            for l in files:
                if filename == l:
                    j = path+l
                    k = os.path.getctime(j)
                    timestruct = time.localtime(k)
                    ctime = time.strftime('%Y-%m-%d %H:%M:%S', timestruct)
                    print filename, "already exist, ctime is", ctime
                    break
            else:
                print filename, "need update"
                local = os.path.join(path, filename)
                urllib.urlretrieve(m_url, local, Schedule)
        break
    else:
        for url in soup.find_all(href=re.compile(".*360safe.*exe$")):
            m_url = url.get("href")
            LIST = m_url.split('/')
            LIST.reverse()
            filename = LIST[0]
            path = FILEPATH[i]
            for root, dirs, files in os.walk(path):
                for l in files:
                    if filename == l:
                        j = path+l
                        k = os.path.getctime(j)
                        timestruct = time.localtime(k)
                        ctime = time.strftime('%Y-%m-%d %H:%M:%S', timestruct)
                        print filename, "already exist, ctime is", ctime
                        break
                else:
                    print filename, "need update"
                    local = os.path.join(path, filename)
                    urllib.urlretrieve(m_url, local, Schedule)

#########auto delete 
FILEPATH = FILELIST.keys()
for i in range(len(FILEPATH)):
    path = FILEPATH[i]
    for root, dirs, files in os.walk(path):
        if len(files) > 4:
            m = path+files[1]
            print m, "is removed"
            os.remove(m)
print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
