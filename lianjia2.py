#!/usr/bin/env python
# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import json
import mysql.connector
class OldHouseSpider(scrapy.Spider):
	name="oldhouse"
	start_urls=["https://gz.lianjia.com/ershoufang/",]
	cnx = mysql.connector.connect(user='root', database='mysql',password='root')
	cursor = cnx.cursor()
	cursor.execute("truncate table house_info")
	cnx.commit()
	cursor.close()
	cnx.close()

	






	
	def parse(self,response):
		add_house = ("insert into house_info  (title,region,houseType,houseArea,houseDirection,houseFitment,houseElevator,totalPrice,unitPrice,houseHigh,totalHigh,year,types,area,line,station,distance) values "+
		"(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
		soup = BeautifulSoup(response.body,"lxml")
		baseInfos=soup.find_all("div",class_="info clear")
		cnx = mysql.connector.connect(user='root', database='mysql',password='root')
		cursor = cnx.cursor()
		for baseInfo in baseInfos:
			houseInfo=baseInfo.find("div",class_="houseInfo")
			houseEleList=list(iter(houseInfo.children))
			region=houseEleList[1].string
			(houseType,houseArea,houseDirection,houseFitment,houseElevator)=parseHouseInfo(houseEleList[2])
			priceInfo=baseInfo.find("div",class_="priceInfo")
			priceInfoList=list(iter(priceInfo.children))
			totalPrice=priceInfoList[0].children.next().string
			unitPrice=priceInfoList[1]['data-price']
			(houseHigh,totalHigh,year,types,area)=parsePositionInfo(baseInfo)
			(line,station,distance)=parseSubway(baseInfo)
			house=(
			str(baseInfo.find("div",class_="title").find("a").string.encode("utf8")),
			str(region.encode("utf8")),
			str(houseType.encode("utf8")),
			str(houseArea.encode("utf8")),
			str(houseDirection.encode("utf8")),
			str(houseFitment.encode("utf8")),
			str(houseElevator.encode("utf8")),
			str(totalPrice.encode("utf8")),
			str(unitPrice.encode("utf8")),
			str(houseHigh.encode("utf8")),
			str(totalHigh.encode("utf8")),
			str(year.encode("utf8")),
			str(types.encode("utf8")),
			str(area.encode("utf8")),
			str(line.encode("utf8")),
			str(station.encode("utf8")),
			str(distance.encode("utf8"))
			)
			cursor.execute(add_house,house)
		cnx.commit()
		cursor.close()
		cnx.close()
		yield {'region':region}
		pageCtrl=soup.find("div",class_="page-box house-lst-page-box")
		pageJson=json.loads(pageCtrl['page-data'])
		next_page=None
		if(pageJson['totalPage']!=pageJson['curPage']):
			next_page=pageCtrl['page-url'].replace('{page}',str(int(pageJson['curPage'])+1))
		if next_page is not None:
			 yield response.follow(next_page, self.parse)




def parseHouseInfo(infostring):
	infos=infostring.split('|')
	houseType=''
	houseArea=0
	houseDirection=''
	houseFitment=u'其他'
	houseElevator=u'未知'
	for info in infos:
		if info==None or info=='':
			continue
		if info.find(u'室')<>-1 and info.find(u'厅')<>-1:
			houseType=info
			continue
		if info.find(u'平米')<>-1:
			houseArea=info[0:info.find(u'平米')]
			continue
		if info.find(u'东')<>-1 or info.find(u'西')<>-1 or info.find(u'南')<>-1 or info.find(u'北')<>-1:
			houseDirection=info
			continue
		if info.find(u'装')<>-1:
			houseFitment=info
			continue
		if info.find(u'电梯')<>-1:
			houseElevator=info
			continue
	return (houseType,houseArea,houseDirection,houseFitment,houseElevator)


def parsePositionInfo(baseInfo):
	nullObj=('','','','','')
	positionInfo=baseInfo.find("div",class_="positionInfo")
	positionInfoList=list(iter(positionInfo.children))
	positonString=positionInfoList[1]
	leftIndex=positonString.find(u'(')
	rightIndex=positonString.find(u')')
	if rightIndex==-1 or rightIndex==-1:
		print positonString
		return nullObj
	houseHigh=positonString[0:leftIndex]
	totalHighString=positonString[leftIndex+1:rightIndex]
	if totalHighString.find(u'共')==-1 or totalHighString.find(u'层')==-1:
		print positonString
		return nullObj
	totalHigh=totalHighString[totalHighString.find(u'共')+1:totalHighString.find(u'层')]
	yearTypeString=positonString[rightIndex+1:]
	year=''
	types=''
	if is_number(yearTypeString[0:4]):
		year=yearTypeString[0:4]
		types=yearTypeString[6:8]
	else:
		types=yearTypeString
	return  (houseHigh,totalHigh,year,types,positionInfoList[2].string)

def parseSubway(baseInfo):
	nullObj=('','','')
	subwayInfo=baseInfo.find("span",class_='subway')
	if subwayInfo==None:
		return nullObj
	subwayString=subwayInfo.string
	lineIndex=subwayString.find(u'号线')
	line=subwayString[2:lineIndex+2]
	stationIndex=subwayString.rfind(u'站')
	station=subwayString[lineIndex+2:stationIndex+1]
	distance=subwayString[stationIndex+1:]
	return (line,station,distance)

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

#aa=response.xpath('//body//div[@class="page-box fr"]').extract_first()

#python -m scrapy runspider lianjia2.py -o oldhouse.csv -t csv

#subwayInfo=baseInfo.find("span",class_='subway')
#python -m scrapy shell https://gz.lianjia.com/ershoufang/