#!/usr/bin/env python
# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import mysql.connector
class LianjiaAreaSpider(scrapy.Spider):
	name = "lianjia_area"
	start_urls = [
        'https://gz.lianjia.com/ershoufang/tianhe/'
    ]
#	self.conn  = mysql.connector.connect(user='root', database='mysql',password='root')
#	self.cursor = self.conn.cursor()
#	self.cursor.execute("""truncate table house_area""")
#	self.conn.commit()
#	self.cursor.close()
#	self.conn.close()

	def cleanElement(self,elist):
		if elist is None:
			return None
		resultList=[]
		for item in elist:
			if item is None or item.string=='' or item.string=='\n':
				continue
			resultList.append(item)
		return resultList

	def parse(self,response):
		soup = BeautifulSoup(response.body,"lxml")
		positiondiv=soup.find('div',class_='position')
		positioncon=list(positiondiv.children)[3]
		positionlist=positioncon.find_all("div")
		citydiv=positionlist[1]
		currentCity=citydiv.find("a",class_	="selected")
		currentCityName=currentCity.string
		currentCityUrl=currentCity["href"]
		currentCityCode=currentCityUrl.split('/')[2]
		areaList=positionlist[2].find_all("a")
		#self.conn  = mysql.connector.connect(user='root', database='mysql',password='root')
		#self.cursor = self.conn.cursor()
		for area in areaList:
			yield {
                'code': area['href'].split('/')[2],
                'name': area.string,
                'citycode':currentCityCode,
                'cityname':currentCityName,
                'url':'https://gz.lianjia.com'+area['href']
            }
			#print item
			#self.cursor.execute("""INSERT INTO house_area (area_code, area_name,city_code,city_name) VALUES (%s, %s, %s, %s)""", (item.get('code','').encode('utf-8'), item.get('name','').encode('utf-8'),
			#item.get('citycode','').encode('utf-8'), item.get('cityname','').encode('utf-8')))
		#self.conn.commit()
		#self.cursor.close()
		#self.conn.close()
		siblings=self.cleanElement(list(currentCity.next_siblings))
		next_page=None
		if siblings is None	 or len(siblings)==0:
			next_page=None	
		else:
			next_page=siblings[0]['href']
		if next_page is not None:
			 yield response.follow(next_page, self.parse)
	

