# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import json
import mysql.connector
import logging
import time



class SingleweiboSpider(scrapy.Spider):
    name = 'SingleWeibo'
    id=4246461874825682
    index=4544
    allowed_domains = ['weibo.cn']
    start_urls = ['https://m.weibo.cn/api/statuses/repostTimeline?id='+str(id)+'&page='+str(index)]
    #cnx = mysql.connector.connect(user='root', database='mysql',password='root')
    #cursor = cnx.cursor()
    #cursor.execute("truncate table weibo_info")
    #cnx.commit()
    #cursor.close()
    #cnx.close()
    retry_time=0

    def parse(self, response):
    	result=json.loads(response.body)
    	add_weibo = ("insert into weibo_info "+
    		" (root_id,created_at,source,text,id,mid,uid,uname,ufollowers_count,ufollow_count,ugender,retweet_time,retweet_id,retweet_mid,reposts_count,comments_count)  "+
		"values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
    	print result["msg"]
    	if result["ok"]==1:
    		cnx = mysql.connector.connect(user='root', database='mysql',password='root')
    		cursor = cnx.cursor()
    		for item in result["data"]['data']:
    			textError=False
    			sourceError=False
    			type(item["text"])
    			try:
    				print item["text"]
    			except Exception as e:
    				textError=True
    				print e
    			try:
    				print item["source"]
    			except Exception as e:
    				sourceError=True
    				print e
    			webo_info=(
    				self.id,
    				str(item["created_at"].encode("utf8")),
    				item["source"],
    				item["text"],
    				item["id"],
    				item["mid"],
    				item["user"]['id'],
    				item["user"]['screen_name'],
    				item["user"]['followers_count'],
    				item["user"]['follow_count'],
    				item["user"]['gender'],
    				item["retweeted_status"]["created_at"],
    				item["retweeted_status"]["id"],
    				item["retweeted_status"]["mid"],
    				item["reposts_count"],
    				item["comments_count"]
    				)
    			try:
    				cursor.execute(add_weibo,webo_info)
    			except Exception as e:
    				webo_info=(
    					self.id,
    					str(item["created_at"].encode("utf8")),
    					'error' if sourceError else item["source"] ,
    					'error' if textError else item["text"],
    					item["id"],
    					item["mid"],
    					item["user"]['id'],
    					item["user"]['screen_name'],
    					item["user"]['followers_count'],
    					item["user"]['follow_count'],
    					item["user"]['gender'],
    					item["retweeted_status"]["created_at"],
    					item["retweeted_status"]["id"],
    					item["retweeted_status"]["mid"],
    					item["reposts_count"],
    					item["comments_count"]
    				)
    				print 'insert tooooooooooo'
    				try:
    					cursor.execute(add_weibo,webo_info)
    				except Exception as e1:
    					print e1
    				
    				print e
    			
    		cnx.commit()
    		cursor.close()
    		cnx.close()
    		self.index=self.index+1
    		time.sleep(3)
    		yield response.follow('https://m.weibo.cn/api/statuses/repostTimeline?id='+str(self.id)+'&page='+str(self.index), self.parse)		
        else:
        	if self.retry_time==3:
        		self.retry_time=0
        		pass
        	else:
        		time.sleep(3)
        		self.retry_time=self.retry_time+1
        		yield response.follow('https://m.weibo.cn/api/statuses/repostTimeline?id='+str(self.id)+'&page='+str(self.index), self.parse)
