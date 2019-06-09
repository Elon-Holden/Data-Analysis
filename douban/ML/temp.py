# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#from urllib.request import urlopen
#from bs4 import BeautifulSoup
#
#html = urlopen('https://movie.douban.com/top250')
#bsObj = BeautifulSoup(html)
#nameList = bsObj.findAll('span',{'class':'title'})
#L = []
#for name in nameList:
#    content = name.get_text()
#    L.append(content)
#print(L)

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
#html = urlopen('https://www.163.com/')
#bsObj = BeautifulSoup(html)
#for link in bsObj.find('li',{'class':'liw2'}).a.attrs:
##    print(link.get_text())
#    print(link)
#    print(type(link))

def getInternalLinks(bsObj,includeUrl):
    internalLinks = []
    for link in bsObj.findAll("a",href=re.compile("^(/|.*"+includeUrl+")")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internalLinks:
                internalLinks.append(link.attrs['href'])
    return internalLinks


def getExternalLinks(bsObj,excludeUrl):
    externalLinks = []
    for link in bsObj.findAll("a",href=re.compile("^(http|www)((?!"+excludeUrl+").)*$")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalLinks:
                externalLinks.append(link.attrs['href'])
    return externalLinks

def splitAddress(address):
    addressParts = address.replace("http://", "").split("/")
    return addressParts

allExtLinks = set()
allIntLinks = set()
def getAllExternalLinks(siteUrl):
    html = urlopen(siteUrl)
    bsObj = BeautifulSoup(html)
    internalLinks = getInternalLinks(bsObj,splitAddress(siteUrl)[0])
    externalLinks = getExternalLinks(bsObj,splitAddress(siteUrl)[0])
    for link in externalLinks:
        allExtLinks.add(link)
        print(link)
    for link in internalLinks:
        if link not in allIntLinks:
            print('即将获取链接的URL是:' + link)
            allIntLinks.add(link)
            getAllExternalLinks(link)

getAllExternalLinks('https://www.douban.com/')