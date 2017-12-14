# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys
import mysql.connector
import logging

class LianjiaPipeline(object):
	logger = logging.getLogger(__name__)
	def __init__(self):
		self.logger.info('init')
		self.conn  = mysql.connector.connect(user='root', database='mysql',password='root')
		self.cursor = self.conn.cursor()
		self.cursor.execute("""truncate table house_area""")
		self.conn.commit()
		self.logger.info('init suc')

	def process_item(self, item, spider):
		self.logger.info('process')   

		self.cursor.execute("""INSERT INTO house_area (area_code, area_name,city_code,city_name,areaurl)
					VALUES (%s, %s, %s, %s,%s)""", (item.get('code','').encode('utf-8'), item.get('name','').encode('utf-8'),
					 item.get('citycode','').encode('utf-8'), item.get('cityname','').encode('utf-8'),item.get('url','').encode('utf-8')))
		self.conn.commit()
		self.logger.info('process suc') 
		return item
	def close_spider(self, spider):
		self.logger.info( 'close')
		self.cursor.close()
		self.conn.close()
