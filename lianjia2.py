#!/usr/bin/env python
# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import json
class OldHouseSpider(scrapy.Spider):
	name="oldhouse"
	start_urls=["https://gz.lianjia.com/ershoufang/",]
	
	def parse(self,response):
		soup = BeautifulSoup(response.body,"lxml")
		baseInfos=soup.find_all("div",class_="info clear")
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
			yield{
			'title':baseInfo.find("div",class_="title").find("a").string,
			'region':region,
			'houseType':houseType,
			'houseArea':houseArea,
			'houseDirection':houseDirection,
			'houseFitment':houseFitment,
			'houseElevator':houseElevator,
			'totalPrice':totalPrice,
			'unitPrice':unitPrice,
			'houseHigh':houseHigh,
			'totalHigh':totalHigh,
			'year':year,
			'types':types,
			'area':area,
			'line':line,
			'station':station,
			'distance':distance

			}
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
	year=yearTypeString[0:4]
	types=yearTypeString[6:8]
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

#aa=response.xpath('//body//div[@class="page-box fr"]').extract_first()

#python -m scrapy runspider lianjia2.py -o oldhouse.csv -t csv

#subwayInfo=baseInfo.find("span",class_='subway')