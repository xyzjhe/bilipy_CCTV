#coding=utf-8
#!/usr/bin/python
import sys
sys.path.append('..')
from base.spider import Spider
import base64
import math
import json
import requests
import urllib
from urllib import request, parse
import urllib.request
import re

class Spider(Spider):
	def getName(self):
		return "西瓜视频(个人中心)"
	def init(self,extend=""):
		pass
	def isVideoFormat(self,url):
		pass
	def manualVideoCheck(self):
		pass
	def homeContent(self,filter):
		result = {}
		cateManual = {
			"收藏2":"collect",
			"观看历史":"history"

		}
		classes = []
		for k in cateManual:
			classes.append({
				'type_name': k,
				'type_id': cateManual[k]
			})

		result['class'] = classes
		if (filter):
			result['filters'] = self.config['filter']
		return result
	def homeVideoContent(self):
		rsp = self.fetch('http://www.ikmjw.com/')
		htmlTxt = rsp.text
		videos = self.get_list(html=htmlTxt)
		result = {
			'list': videos
		}
		return result

	def categoryContent(self,tid,pg,filter,extend):
		result = {}
		if int(pg)>1:
			return result
		url = ''
		if tid=='history':#历史
			url = 'https://www.ixigua.com/api/videov2/get/history?maxTime=1678090877&type=lvideo&count=4'
		elif tid=='collect':#收藏
			url = 'https://www.ixigua.com/api/videov2/get/favorite?maxTime=1678003966&type=all&count=12'
		rsp = self.fetch(url,headers=self.header)
		htmlTxt=rsp.text
		videos = self.get_list(html=htmlTxt)
		
		
		numvL = len(videos)
		result['list'] = videos
		result['page'] = pg
		result['pagecount'] = 999
		result['limit'] = numvL
		result['total'] = numvL
		return result

	def detailContent(self,array):
		result = {}
		aid = array[0].split('###')
		key=aid[2]
		pic=aid[3]
		
		videoList=[]
		
		vodItems = []
		title=aid[1]
		#playFrom=[v for v in jo['albumInfo']['tagList']]
		typeName=''#'/'.join(playFrom)
		year=''
		#playFrom=[v for v in jo['albumInfo']['areaList']]
		area=''#'/'.join(playFrom)
		#playFrom=[v['name'] for v in jo['albumInfo']['actorList']]#问题
		act=''#'/'.join(playFrom)
		#playFrom=[v['name'] for v in jo['albumInfo']['directorList']]
		dir=''#'/'.join(playFrom)
		cont=''#jo['albumInfo']['intro']
		vod = {
			"vod_id": aid,
			"vod_name": title,
			"vod_pic": pic,
			"type_name": '',
			"vod_year": '',
			"vod_area": '',
			"vod_remarks": '',
			"vod_actor": '',
			"vod_director": '',
			"vod_content": ''
		}
		vod['vod_play_from'] = '西瓜'
		vod['vod_play_url'] = "#".join(vodItems)
		result = {
			'list': [
				vod
			]
		}
		return result

	def verifyCode(self):
		pass

	def searchContent(self,key,quick):
		Url='http://www.ikmjw.com/ppyssearch.html?wd={0}&submit='.format(urllib.parse.quote(key))
		rsp = self.fetch(Url)
		htmlTxt = rsp.text
		videos = self.get_list(html=htmlTxt)
		result = {
				'list': videos
			}
		return result

	def playerContent(self,flag,id,vipFlags):
		result = {}
		result["parse"] = 0
		result["playUrl"] = ''
		result["url"] = id
		result["header"] = ''
		return result
	def get_RegexGetText(self,Text,RegexText,Index):
		returnTxt=""
		Regex=re.search(RegexText, Text, re.M|re.I)
		if Regex is None:
			returnTxt=""
		else:
			returnTxt=Regex.group(Index)
		return returnTxt	
	def get_RegexGetTextLine(self,Text,RegexText,Index):
		returnTxt=[]
		pattern = re.compile(RegexText)
		ListRe=pattern.findall(Text)
		if len(ListRe)<1:
			return returnTxt
		for value in ListRe:
			returnTxt.append(value)	
		return returnTxt
	def get_playlist(self,Text,headStr,endStr):
		circuit=""
		origin=Text.find(headStr)
		if origin>8:
			end=Text.find(endStr,origin)
			circuit=Text[origin:end]
		return circuit
	def removeHtml(self,txt):
		soup = re.compile(r'<[^>]+>',re.S)
		txt =soup.sub('', txt)
		return txt.replace("&nbsp;"," ")
	def get_webReadFile(self,urlStr):
		headers = {
			'Referer':urlStr,
			'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
			'Host': 'www.ikmjw.com'
		}
		req = urllib.request.Request(url=urlStr, headers=headers)
		html = urllib.request.urlopen(req).read().decode('utf-8')
		return html
	def get_list(self,html):
		result={}
		jRoot = json.loads(html)
		if jRoot['code']!=200:
			return result
		jo = jRoot['data']['channelFeed']
		vodList = jo['Data']
		if len(vodList)<1:
			return result
		videos=[]
		for vod in vodList:
			data=vod['data']
			if len(data)<1:
				continue
			url =vod['key']
			title =data['title']
			img =vod['data'].get('image_url') 
			maxTime=vod['maxTime']
			if img is None:
				img =data['coverList'][0].get('url')
			if len(url) == 0:
				continue
			#maxTime###标题###地址###封面
			vod_id="{0}###{1}###{2}###{3}".format(maxTime,title,url,img)
			videos.append({
				"vod_id":vod_id,
				"vod_name":title,
				"vod_pic":img,
				"vod_remarks":''
			})
		res = [i for n, i in enumerate(videos) if i not in videos[:n]]
		videos = res
		return videos
	def get_lineList(self,Txt,mark,after):
		circuit=[]
		origin=Txt.find(mark)
		while origin>8:
			end=Txt.find(after,origin)
			circuit.append(Txt[origin:end])
			origin=Txt.find(mark,end)
		return circuit
	def get_EpisodesList(self,jsonList):
		vodItems=[]
		for value in jsonList:
			vodItems.append(value['title']+"$"+value['shareUrl'])
		return vodItems
	config = {
		"player": {},
		"filter": {}
	}
	header = {
		"Referer": 'https://www.ixigua.com/',
		'User-Agent':'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
		'Cookie':'ttcid=cd196cbb0b844d559391fbb1cc90dbd350; __ac_nonce=06404494600b70f8a89b2; __ac_signature=_02B4Z6wo00f01MXq0BwAAIDBJBSBkSJFPQjFyNSAAFWEIDpvxjkTcANBTvMl0fMzITEkmmzddYvCCaE7.W0YLajEdH-JWf0lpAc5flpY14TgosM9tcYWPrDB2-cP0sv-pxR7n8N5FVw5ZJDef7; MONITOR_WEB_ID=45c3b6ab-7ad4-4805-b971-5962d1d6909a; s_v_web_id=verify_lev3h43l_rrTPrFDG_ztWQ_4ugg_8WBA_yGVYsXlVyoBh; passport_csrf_token=80e0efe90bc8bd6681a896dd90cd08cc; passport_csrf_token_default=80e0efe90bc8bd6681a896dd90cd08cc; odin_tt=91b5d4bd5b2c49b52a7eff16c14df7c66e509864a8ec7edd5612e67cbdd863ae7227ed4b95d66dbb65a3a427caf69fd7; sid_guard=54266b282adf9c8dbb69f9cc37342191%7C1678002757%7C3024000%7CSun%2C+09-Apr-2023+07%3A52%3A37+GMT; uid_tt=3c0e8cb286ad3de4d95252bb7d5e0fc6; uid_tt_ss=3c0e8cb286ad3de4d95252bb7d5e0fc6; sid_tt=54266b282adf9c8dbb69f9cc37342191; sessionid=54266b282adf9c8dbb69f9cc37342191; sessionid_ss=54266b282adf9c8dbb69f9cc37342191; sid_ucp_v1=1.0.0-KDQ5MzZiMjFhZjBkODU1MjRiZDMxNThkMzhlNDExYWUwMTY5NTNlZTkKFQjL2cnx9AIQxZSRoAYYGCAMOAhABRoCaGwiIDU0MjY2YjI4MmFkZjljOGRiYjY5ZjljYzM3MzQyMTkx; ssid_ucp_v1=1.0.0-KDQ5MzZiMjFhZjBkODU1MjRiZDMxNThkMzhlNDExYWUwMTY5NTNlZTkKFQjL2cnx9AIQxZSRoAYYGCAMOAhABRoCaGwiIDU0MjY2YjI4MmFkZjljOGRiYjY5ZjljYzM3MzQyMTkx; support_webp=true; support_avif=false; ttwid=1%7CCueNR-HU9tGVF30WaiFCjXDxh0FUXoXsZr-cIb9Dogg%7C1678003714%7C668bcb31fd4bbd27d96c2e9b8b54ee19d432e07e2dc29424ed7d4f565afbb72f; csrf_session_id=5bbbd0c6b4a64b19dc32694083983872; msToken=zneoThG9FFaRAzZIk88NksVv1_nOKubCtSbgADqPrvnQfGmRu3awlR-RqO_kdAauJffkdzGnSKGfatuHr_NDK5gVV559naHVVms0KBugXVh3pb7w6eaJPnt0LClhXL4=; tt_scid=dt.GJVugJWLpeXtGQtz6SCsIykASc.5FpVWCkR3J2nt-7Rr8igGA9UlwRtQlKKKf621b; ixigua-a-s=1'
	}

	def localProxy(self,param):
		return [200, "video/MP2T", action, ""]
