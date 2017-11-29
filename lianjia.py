#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
def parseUrl(url):
	import urllib2
	print 'req'+url
	response = urllib2.urlopen(url)
	soup = BeautifulSoup(response.read(),"lxml")
	print 'build sucess' + url
	return soup

def parseBaseInfo(item):
	try:
		namelink=item.find("a")
		return (item.find("span",class_='region').string,
			namelink.string,
			item.find("span",class_='onsold').string,
			item.find("span",class_='live').string,
			item.find("span",class_='num').string,namelink["href"])
	except Exception as e:
		print e
		return ('','','','','','')
	


def parseMainPage():
	return parseUrl("https://gz.fang.lianjia.com/loupan/")

def parsePage(soup):
	info_panels=soup.find_all("div",class_="info-panel")
	return list(map(parseBaseInfo,info_panels))
def parseOnePage(x):
	print 'scan page'+str(x)
	return parsePage(parseUrl('https://gz.fang.lianjia.com/loupan/pg'+str(x)+'/'))

def output(baseInfos):
	print 'start output'
	from openpyxl import Workbook
	wb = Workbook()
	ws = wb.active
	ws.append(["区域","销售状态","物业类型","地址", "名称", "价格","链接"])
	
	for (region,name,onsold,live,price,link) in baseInfos:
		area=''
		if len(region)==0:
			continue
		if len(region)>2:
			area=region[0:2]
		link="https://gz.fang.lianjia.com"+link
		try:
			ws.append([area,onsold,live,region,name,price,link])
		except Exception as e:
			print e	
	wb.save("houses.xlsx")

soup=parseMainPage()
pagectl=soup.find("div",class_='page-box house-lst-page-box')

import json
pageObj=json.loads(pagectl['page-data'])
baseInfos=parsePage(soup)
from multiprocessing.dummy import Pool as ThreadPool 
pool = ThreadPool(4)
results = pool.map(parseOnePage, xrange(2,pageObj['totalPage']))
for infos in results:
	print len(infos)
	baseInfos=baseInfos+infos
output(baseInfos)
