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
		return "蓝海地星人的空间"
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
			"关注的Pu主1": "pu",
			"个人收藏": "Collection"
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
		videos=[]
		if tid=="pu":
			videos=self.get_list_pu()
		else:
			videos = self.get_list_pu()
		result['list'] = videos
		result['page'] = pg
		result['pagecount'] = 9999
		result['limit'] = 90
		result['total'] = 999999
		return result
	def detailContent(self,array):
		result = {}
		aid = array[0].split('###')
		if aid[2].find("http")<0:
			return result
		tid = aid[0]
		logo = aid[3]
		lastVideo = aid[2]
		title = aid[1]
		date = aid[0]
		if lastVideo == '_':
			return result
		rsp = self.fetch(lastVideo,headers=self.header)
		htmlTxt=rsp.text
		vodItems =[]
		if tid=="西瓜":
			vodItems = get_collection_xg(html=htmlTxt)
		vod = {
			"vod_id":tid,#array[0],
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
		headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
			'Host': 'www.66s.cc'
		}

		data="show=title&tempid=1&tbname=article&mid=1&dopost=search&submit=&keyboard="+urllib.parse.quote(key)
		payUrl="https://www.66s.cc/e/search/index.php"
		req = request.Request(url=payUrl, data=bytes(data, encoding='utf8'),headers=headers, method='POST')
		response = request.urlopen(req)
		urlTxt=response.geturl()
		response = urllib.request.urlopen(urlTxt)
		htmlTxt=response.read().decode('utf-8')
		videos = self.get_list(html=htmlTxt,tid="6v电影")
		result = {
			'list':videos
		}
		return result
	def playerContent(self,flag,id,vipFlags):
		result = {}
		htmlTxt=self.webReadFile(urlStr=id)
		pattern=re.compile(r'(https{0,1}://.+?\.m3u8.*?)')
		ListRe=pattern.findall(htmlTxt)
		url=""
		if ListRe==[]:	
			url=self.get_playUrlMethodOne(html=htmlTxt)
		else:
			url=ListRe[0]
		result["parse"] = 0
		result["playUrl"] =""
		result["url"] = url
		result["header"] = ''
		return result
	def get_playUrlMethodOne(self,html):
		#自定义函数时self参数是必要的,调用时self参数留空
		pattern =re.search( r'<div class="video"><iframe.+?src="(.+?)"></iframe></div>', html, re.M|re.I).group(1)
		if len(pattern)<4:
			return ""
		rsp = self.fetch(pattern)
		htmlTxt=rsp.text
		head=re.search( r'(https{0,1}://.+?)/', pattern, re.M|re.I).group(1)
		if len(head)<4:
			return ""
		url=re.search( r'var\smain\s*=\s*"(.+?)"', htmlTxt, re.M|re.I).group(1)
		url=head+url
		return url
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
	def get_list_pu(self):
		ListRe=[("科技猿人","https://www.ixigua.com/home/62435616925/","西瓜"),("妈咪说MommyTalk","https://www.ixigua.com/home/62786280361/","西瓜")]
		videos = []
		for vod in ListRe:
			lastVideo = vod[1]
			title =vod[0]
			tid=vod[2]
			img = "https://agit.ai/lanhaidixingren/Tvbox/raw/branch/master/%E5%8D%93%E9%9B%85%281%29.jpg"
			if len(lastVideo) == 0:
				lastVideo = '_'
			guid = tid+'###'+vod[1]+'###'+lastVideo+'###'+img
			videos.append({
				"vod_id":guid,
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
		"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36",
		'Host': 'www.ixigua.com'
	}

	def localProxy(self,param):
		return [200, "video/MP2T", action, ""]