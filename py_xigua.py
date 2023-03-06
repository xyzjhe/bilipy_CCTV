#coding=utf-8
#!/usr/bin/python
import sys
sys.path.append('..') 
from base.spider import Spider
import json
import time
import base64
import re
from urllib import request, parse
import urllib
import urllib.request

class Spider(Spider):  # 元类 默认的元类 type
	def getName(self):
		return "西瓜视频(个人中心)"
	def init(self,extend=""):
		print("============{0}============".format(extend))
		pass
	def isVideoFormat(self,url):
		pass
	def manualVideoCheck(self):
		pass
	def homeContent(self,filter):
		result = {}
		cateManual = {
			"关注": "follow",
			"收藏":"collect",
			"观看历史":"history"
		}
		classes = []
		for k in cateManual:
			classes.append({
				'type_name':k,
				'type_id':cateManual[k]
			})
		result['class'] = classes
		if(filter):
			result['filters'] = self.config['filter']
		return result
	def homeVideoContent(self):
		result = {
			'list':[]
		}
		return result
	def categoryContent(self,tid,pg,filter,extend):
		result = {}
		htmlTxt=''
		rsp = self.fetch('https://www.ixigua.com/api/videov2/get/favorite?maxTime=1678003966&type=all&count=12',headers=self.header)
		htmlTxt = rsp.text
		videos = self.get_list_json(jsonTxt=htmlTxt)		
		result['list'] = videos
		result['page'] = pg
		result['pagecount'] = 1
		result['limit'] = 90
		result['total'] = 999999
		return result
	def detailContent(self,array):
		result = {}
		aid = array[0].split('###')
		tid = aid[0]
		logo = aid[3]
		url = aid[1]
		title = aid[1]
		vodItems=[]
		Url=''
		rsp = self.fetch(Url)
		htmlTxt = rsp.text
		pattern = re.compile('')
		ListRe=pattern.findall(htmlTxt)
		for value in ListRe:
			vodItems.append(value[1]+"$"+value[0])
		vod = {
			"vod_id":array[0],
			"vod_name":title,
			"vod_pic":logo,
			"type_name":tid,
			"vod_year":"",
			"vod_area":"",
			"vod_remarks":"",
			"vod_actor":"",
			"vod_director":"",
			"vod_content":""
		}
		vod['vod_play_from'] = "线路"
		vod['vod_play_url'] = "#".join(vodItems)
		result = {
			'list':[
				vod
			]
		}
		print(result)
		return result

	def searchContent(self,key,quick):
		result = {
			'list':[]
		}
		return result
	def playerContent(self,flag,id,vipFlags):
		result = {}
		parse=1
		Url=id
		rsp = self.fetch(Url)
		htmlTxt = rsp.text
		m3u8Line=self.get_RegexGetTextLine(Text=htmlTxt,RegexText=r'(http.+?m3u8)',Index=1)
		if len(m3u8Line)>0:
			Url=m3u8Line[0].replace("/","")
			parse=0 
		result["parse"] = parse
		result["playUrl"] = ''
		result["url"] = Url
		result["header"] = ''
		return result
	def get_collection_xg(html):
		videoList = []
		pattern = re.compile(r'title="(.+?)"\s*href="(.+?&amp;)".+? src="(.+?)"')
		ListRe=pattern.findall(html)
		for video in ListRe:
			videoList.append(video[0]+"$https://www.ixigua.com"+video[1].replace('&amp;' , '&'))
		return videoList
	def webReadFile(self,urlStr):
		if urlStr.find("http")<0:
			return ""
		req = urllib.request.Request(url=urlStr, headers=self.header)
		html = urllib.request.urlopen(req).read().decode('utf-8')
		return html
	def get_UrlParameter(self,parameter):
		aid =parameter.split('###')
		for t in aid:
			if t.find("http")>-1 and t.find("html")>-1:
				return t	
		return "https://www.ixigua.com/"	
	def get_list_json(jsonTxt):
		result={}
		jRoot = json.loads(jsonTxt)
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
		return videos
	config = {
		"player": {},
		"filter": {}
		}
	header = {
		"Referer": 'https://www.ixigua.com/my/favorite',
		'User-Agent':'my.ie.2345.com',
		'Cookie':'ttcid=cd196cbb0b844d559391fbb1cc90dbd350; __ac_nonce=06404494600b70f8a89b2; __ac_signature=_02B4Z6wo00f01MXq0BwAAIDBJBSBkSJFPQjFyNSAAFWEIDpvxjkTcANBTvMl0fMzITEkmmzddYvCCaE7.W0YLajEdH-JWf0lpAc5flpY14TgosM9tcYWPrDB2-cP0sv-pxR7n8N5FVw5ZJDef7; MONITOR_WEB_ID=45c3b6ab-7ad4-4805-b971-5962d1d6909a; s_v_web_id=verify_lev3h43l_rrTPrFDG_ztWQ_4ugg_8WBA_yGVYsXlVyoBh; passport_csrf_token=80e0efe90bc8bd6681a896dd90cd08cc; passport_csrf_token_default=80e0efe90bc8bd6681a896dd90cd08cc; odin_tt=91b5d4bd5b2c49b52a7eff16c14df7c66e509864a8ec7edd5612e67cbdd863ae7227ed4b95d66dbb65a3a427caf69fd7; sid_guard=54266b282adf9c8dbb69f9cc37342191%7C1678002757%7C3024000%7CSun%2C+09-Apr-2023+07%3A52%3A37+GMT; uid_tt=3c0e8cb286ad3de4d95252bb7d5e0fc6; uid_tt_ss=3c0e8cb286ad3de4d95252bb7d5e0fc6; sid_tt=54266b282adf9c8dbb69f9cc37342191; sessionid=54266b282adf9c8dbb69f9cc37342191; sessionid_ss=54266b282adf9c8dbb69f9cc37342191; sid_ucp_v1=1.0.0-KDQ5MzZiMjFhZjBkODU1MjRiZDMxNThkMzhlNDExYWUwMTY5NTNlZTkKFQjL2cnx9AIQxZSRoAYYGCAMOAhABRoCaGwiIDU0MjY2YjI4MmFkZjljOGRiYjY5ZjljYzM3MzQyMTkx; ssid_ucp_v1=1.0.0-KDQ5MzZiMjFhZjBkODU1MjRiZDMxNThkMzhlNDExYWUwMTY5NTNlZTkKFQjL2cnx9AIQxZSRoAYYGCAMOAhABRoCaGwiIDU0MjY2YjI4MmFkZjljOGRiYjY5ZjljYzM3MzQyMTkx; support_webp=true; support_avif=false; ttwid=1%7CCueNR-HU9tGVF30WaiFCjXDxh0FUXoXsZr-cIb9Dogg%7C1678003714%7C668bcb31fd4bbd27d96c2e9b8b54ee19d432e07e2dc29424ed7d4f565afbb72f; csrf_session_id=5bbbd0c6b4a64b19dc32694083983872; msToken=zneoThG9FFaRAzZIk88NksVv1_nOKubCtSbgADqPrvnQfGmRu3awlR-RqO_kdAauJffkdzGnSKGfatuHr_NDK5gVV559naHVVms0KBugXVh3pb7w6eaJPnt0LClhXL4=; tt_scid=dt.GJVugJWLpeXtGQtz6SCsIykASc.5FpVWCkR3J2nt-7Rr8igGA9UlwRtQlKKKf621b; ixigua-a-s=1'
	}

	def localProxy(self,param):
		return [200, "video/MP2T", action, ""]