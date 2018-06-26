import scrapy
from bs4 import BeautifulSoup
import json
import mysql.connector
import logging
import time



class ParentWeiboSpider(scrapy.Spider):
	name = 'ParentWeibo'
	allowed_domains = ['weibo.cn']
	root_id=4246461874825682
	cnx = mysql.connector.connect(user='root', database='mysql',password='root')
	cursor = cnx.cursor()
	cursor.execute("select mid from  weibo_info where reposts_count>0   order by reposts_count desc ")
	result=cursor.fetchall()
	id=result[0][0]
	print len(result)
	print id
	index=1
	start_urls = ['https://m.weibo.cn/api/statuses/repostTimeline?id='+str(id)+'&page='+str(index)]
	weiboIndex=0
	retry_time=0

	def midExists(self,mid):
		cnx = mysql.connector.connect(user='root', database='mysql',password='root')
		print 'midExists'+str(mid)
		cursor = cnx.cursor()
		cursor.execute('select mid,retweet_time,retweet_mid from  weibo_info where mid='+mid)
		result= cursor.fetchone()
		try:
			cnx.commit()
			cursor.close()
			cnx.close()
		except Exception as e:
			print e
		return 	result

	def parse(self, response):
		result=json.loads(response.body)
		if result["ok"]==1:
			for item in result["data"]['data']:
				mid= item["mid"]
				midinfo=self.midExists(mid)
				if midinfo==None:
					self.insertItem(item)
				else:
					(sourceid,retweet_time,retweet_mid)=midinfo
					if not self.isAncestor(self.id,retweet_mid) :
						cnx = mysql.connector.connect(user='root', database='mysql',password='root')
						cursor=cnx.cursor()
						exesql='update weibo_info set retweet_mid='+str(self.id)+',  retweet_id='+str(self.id)+' where mid='+str(sourceid)
						print 'parse:'+exesql
						cursor.execute(exesql)
						try:
							cnx.commit()
							cursor.close()
							cnx.close()
						except Exception as e:
							print e
			self.index=self.index+1
			time.sleep(3)
			yield response.follow('https://m.weibo.cn/api/statuses/repostTimeline?id='+str(self.id)+'&page='+str(self.index), self.parse)	
		else:
			print 'weibo no '
			self.retry_time=0
			self.weiboIndex=self.weiboIndex+1
			if self.weiboIndex<len(self.result):
				print 'weibo change'
				self.id=self.result[self.weiboIndex][0]
				self.index=1
				yield response.follow('https://m.weibo.cn/api/statuses/repostTimeline?id='+str(self.id)+'&page='+str(self.index), self.parse)

	def isAncestor(self,acid,mid):
		childid=mid
		cnx = mysql.connector.connect(user='root', database='mysql',password='root')
		try:
			while True:
				cursor=cnx.cursor()
				cursor.execute('select retweet_mid from weibo_info where mid='+str(childid))
				ac=cursor.fetchone()
				print 'isAncestor'
				print ac
				if ac==None:
					return False
				if ac[0]==acid:
					return True
				childid=ac[0]
				cursor.close()

		except Exception as e:
			print e
		finally:
			cnx.close()
		
		

	def insertItem(self,item):
		cnx = mysql.connector.connect(user='root', database='mysql',password='root')
		add_weibo = ("insert into weibo_info "+
			" (root_id,created_at,source,text,id,mid,uid,uname,ufollowers_count,ufollow_count,ugender,retweet_time,retweet_id,retweet_mid,reposts_count,comments_count)  "+
			"values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
		textError=False
		sourceError=False
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
			self.root_id,
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
			self.id,
			self.id,
			item["reposts_count"],
			item["comments_count"]
			)
		cnx = mysql.connector.connect(user='root', database='mysql',password='root')
		cursor = cnx.cursor()
		try:
			cursor.execute(add_weibo,webo_info)
		except Exception as e:
			print e
		cnx.commit()
		cursor.close()
		cnx.close()

	

