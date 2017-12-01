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
			yield{
			'title':baseInfo.find("div",class_="title").find("a").string
			}
		pageCtrl=soup.find("div",class_="page-box house-lst-page-box")
		pageJson=json.loads(pageCtrl['page-data'])
		next_page=None
		if(pageJson['totalPage']!=pageJson['curPage']):
			next_page=pageCtrl['page-url'].replace('{page}',str(int(pageJson['curPage'])+1))
		if next_page is not None:
			 yield response.follow(next_page, self.parse)

#aa=response.xpath('//body//div[@class="page-box fr"]').extract_first()

#soup = BeautifulSoup(response.body,"lxml")
