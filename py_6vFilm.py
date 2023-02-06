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

class Spider(Spider):  # 元类 默认的元类 type
	def getName(self):
		return "6V电影"
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
			"科幻片": "kehuanpian",
			"动画片": "donghuapian",
			"电视剧": "dianshiju",
			"爱情片": "aiqingpian",
			"动作片": "dongzuopian",
			"喜剧片": "xijupian",
			"恐怖片": "kongbupian",
			"剧情片": "juqingpian",
			"战争片": "zhanzhengpian",
			"纪录片": "jilupian",
			"综艺": "ZongYi"
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
		url=""
		patternTxt='<div class="thumbnail">\s*<a href="(.+)"\s*class="zoom".*?title="(.+?)".*?\n*\s*<img src="(.+?)"'
		head="https://www.66s.cc"
		if tid=="qian50m":
			url=r"https://www.66s.cc/qian50m.html"
		else:
			url=r"https://www.66s.cc/{0}/".format(tid)
			if pg!="1":#pg值是字符串
				url=url+"index_{0}.html".format(pg)
		rsp = self.fetch(url)
		htmlTxt=rsp.text
		pattern = re.compile(patternTxt)
		ListRe=pattern.findall(htmlTxt)
		videos = []
		for vod in ListRe:
			lastVideo = vod[0]
			if len(lastVideo) == 0:
				lastVideo = '_'
			if lastVideo.find(head)<0 and lastVideo!="_":
				lastVideo=head+lastVideo
			guid = tid+'###'+vod[1]+'###'+lastVideo+'###'+vod[2]
			title =vod[1]
			img = vod[2]
			videos.append({
				"vod_id":guid,
				"vod_name":title,
				"vod_pic":img,
				"vod_remarks":''
			})
		result['list'] = videos
		result['page'] = pg
		result['pagecount'] = 9999
		result['limit'] = 90
		result['total'] = 999999
		return result
	def detailContent(self,array):
		aid = array[0].split('###')
		if aid[2].find("http")<0:
			return {}
		tid = aid[0]
		logo = aid[3]
		lastVideo = aid[2]
		title = aid[1]
		date = aid[0]
		if lastVideo == '_':
			return {}
		rsp = self.fetch(lastVideo)
		htmlTxt=rsp.text
		circuit=[]
		if htmlTxt.find('<h3>播放地址')>8:
			origin=htmlTxt.find('<h3>播放地址')
			while origin>8:
				end=htmlTxt.find('</div>',origin)
				circuit.append(htmlTxt[origin:end])
				origin=htmlTxt.find('<h3>播放地址',end)
		if len(circuit)<1:
			circuit.append(htmlTxt)
		#print(circuit)
		playFrom = []
		videoList = []
		patternTxt=r'<a title=\'(.+?)\'\s*href=\s*"(.+?)"\s*target=\s*"_blank"\s*class="lBtn" >(\1)</a>'
		pattern = re.compile(patternTxt)
		head="https://www.66s.cc"
		for v in circuit:
			ListRe=pattern.findall(v)
			temporary=re.search( r'<h3>(播放地址.*?)</h3>', v, re.M|re.I).group(1)
			playFrom.append(temporary)
			vodItems = []
			for value in ListRe:
				url=value[1]
				if url.find(head)<0:
					url=head+url
				vodItems.append(value[0]+"$"+url)
			joinStr = "#".join(vodItems)
			videoList.append(joinStr)
		if len(videoList) == 0:
			return {}
		vod_play_from = '$$$'.join(playFrom)
		vod_play_url = "$$$".join(videoList)
		vod = {
			"vod_id":tid,#array[0],
			"vod_name":title,
			"vod_pic":logo,
			"type_name":"6v电影",
			"vod_year":"",
			"vod_area":"",
			"vod_remarks":"",
			"vod_actor":"",
			"vod_director":"",
			"vod_content":""
		}
		vod['vod_play_from'] = vod_play_from
		vod['vod_play_url'] = vod_play_url
		vod = {
			"vod_id":tid,#array[0],
			"vod_name":title,
			"vod_pic":logo,
			"type_name":"6v电影",
			"vod_year":"",
			"vod_area":"",
			"vod_remarks":"",
			"vod_actor":"",
			"vod_director":"",
			"vod_content":""
		}
		vod['vod_play_from'] = vod_play_from
		vod['vod_play_url'] = vod_play_url
		result = {
			'list':[
				vod
			]
		}
		return result

	def searchContent(self,key,quick):
		headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
			'Host': 'www.66s.cc'
		}

		 data = {
		    "show": "title",
		    "tempid": "1",
		    "tbname": "article",
		    "mid": "1",
		    "dopost": "search",
		    "keyboard": +urllib.parse.quote(key)
		}
		payUrl="https://www.66s.cc/e/search/index.php"
		req=self.post(payUrl,data,headers=headers)
		urlTxt=req.geturl()
		htmlTxt =self.fetch(urlTxt,headers=headers)
		patternTxt='<div class="thumbnail">\s*<a href="(.+)"\s*class="zoom".*?title="(.+?)".*?\n*\s*<img src="(.+?)"'
		pattern = re.compile(patternTxt)
		ListRe=pattern.findall(htmlTxt)
		for vod in ListRe:
			lastVideo = vod[0]
			if len(lastVideo) == 0:
				lastVideo = '_'
			if lastVideo.find(head)<0 and lastVideo!="_":
				lastVideo=head+lastVideo
			soup = re.compile(r'<[^>]+>',re.S)
			title =soup.sub('', vod[1])
			guid = "6v电影"+'###'+title+'###'+lastVideo+'###'+vod[2]
			img = vod[2]
			print(guid)
			videos.append({
				"vod_id":guid,
				"vod_name":title,
				"vod_pic":img,
				"vod_remarks":''
			})
		result = {
			'list':videos
		}
		return result
	def playerContent(self,flag,id,vipFlags):
		result = {}
		rsp = self.fetch(id)
		htmlTxt=rsp.text
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

	config = {
		"player": {},
		"filter": {}
		}
	header = {
		"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36",
		"Origin": "https://www.66s.cc",
		"Referer": "https://www.66s.cc/"
	}

	def localProxy(self,param):
		return [200, "video/MP2T", action, ""]