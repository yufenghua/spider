# -*- coding: utf-8 -*-
from openpyxl import Workbook
import mysql.connector
import datetime
from datetime import datetime
cnx = mysql.connector.connect(user='root', database='mysql',password='root')
cursor = cnx.cursor()
cursor.execute('select root_id,id,mid,source, text, created_at,uid,uname,ufollowers_count,ufollow_count,ugender,retweet_time,retweet_id,retweet_mid,reposts_count,comments_count,retweet_uid,retweet_uname,retweet_source from  weibo_info_all ')
wb = Workbook()
ws = wb.active
formatstr='%b%d%H%Y'
ws.append(["root_id","id","mid","source", "text", "created_at","uid","uname","ufollowers_count","ufollow_count","ugender","retweet_time"
	,"retweet_id","retweet_mid","reposts_count","comments_count","retweet_uid","retweet_uname","retweet_source"])
for (root_id,id,mid,source, text, created_at,uid,uname,ufollowers_count,ufollow_count,ugender,retweet_time,retweet_id,retweet_mid,reposts_count,comments_count,retweet_uid,retweet_uname,retweet_source) in cursor:
	realtimestr=retweet_time[4:7]+retweet_time[8:10]+retweet_time[11:13]+retweet_time[-4:]
	ws.append([str(root_id),str(id),str(mid),source, text, created_at,str(uid),uname,ufollowers_count,ufollow_count,ugender, datetime.strptime(realtimestr, formatstr).strftime('%Y-%m-%d %H'),str(retweet_id),str(retweet_mid),reposts_count,comments_count,'' if retweet_uid==None else str(retweet_uid),retweet_uname,retweet_source])

wb.save('D:/weibo.xlsx')