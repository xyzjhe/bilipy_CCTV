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
		return "卡通站"
	def init(self,extend=""):
		pass
	def isVideoFormat(self,url):
		pass
	def manualVideoCheck(self):
		pass
	def homeContent(self,filter):
		result = {}
		cateManual = {
			"国产动画": "30",
			"日韩动画": "3",
			"国语动画": "1",
			"粤语动画": "2",
			"动漫电影": "4",
			"海外动画": "28"
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
		rsp = self.fetch('http://ktkkt.top/')
		htmlTxt = rsp.text
		videos = self.get_list(html=htmlTxt)
		result = {
			'list': videos
		}
		return result

	def categoryContent(self,tid,pg,filter,extend):
		result = {}
		url = 'http://ktkkt.top/frim/index{0}-{1}.html'.format(tid,pg)
		rsp = self.fetch(url)
		htmlTxt=rsp.text
		videos = self.get_list(html=htmlTxt)
		pag=self.get_RegexGetText(Text=htmlTxt,RegexText=r'href="/frim/index1-([0-9]+?).html">尾页</a></li>',Index=1)
		if pag=="":
			pag=999
		numvL = len(videos)
		result['list'] = videos
		result['page'] = pg
		result['pagecount'] = pag
		result['limit'] = numvL
		result['total'] = numvL
		return result

	def detailContent(self,array):
		aid = array[0].split('###')
		idUrl=aid[1]
		title=aid[0]
		pic=aid[2]
		url='http://ktkkt.top{0}'.format(idUrl)
		rsp = self.fetch(url)
		htmlTxt = rsp.text
		line=self.get_RegexGetTextLine(Text=htmlTxt,RegexText=r'<a href="#(playlist[1-9]{1,8})"\s*.+?=".+?">(.+?)</a>',Index=1)
		circuit=[]
		for i in line:
			circuit.append(self.get_playlist(Text=htmlTxt,headStr='id="'+i[0],endStr="</div>"))
		playFrom = []
		videoList=[]
		pattern = re.compile(r"<li><a\stitle='(.+?)'\shref='(.+?)'"+'\starget="_self">(.+?)</a></li>')
		for v in circuit:
			ListRe=pattern.findall(v)
			vodItems = []
			for value in ListRe:
				vodItems.append(value[0]+"$"+value[1])
			joinStr = "#".join(vodItems)
			videoList.append(joinStr)
		playFrom=[t[1] for t in line]
		vod_play_from='$$$'.join(playFrom)
		vod_play_url = "$$$".join(videoList)
		typeName=self.get_RegexGetText(Text=htmlTxt,RegexText=r'分类：</span><a href=".*?">(.*?)</a>',Index=1)
		year=self.get_RegexGetText(Text=htmlTxt,RegexText=r'年份：</span><a\s.+?>([0-9]{4})',Index=1)
		area=self.get_RegexGetText(Text=htmlTxt,RegexText=r'地区：</span><a href=".*?=(.+?)">\1</a>',Index=1)
		act=self.get_RegexGetText(Text=htmlTxt,RegexText=r'主演：</span><a\s*href=("'+"|')"+'.+?("|'+"')>(.+?)</a>",Index=3)
		dir=self.get_RegexGetText(Text=htmlTxt,RegexText=r'导演：</span><a\s*href=("'+"|')"+'.+?("|'+"')>(.+?)</a>",Index=3)
		cont=self.get_RegexGetText(Text=htmlTxt,RegexText=r'<span class="sketch">(.*?)</span>',Index=1)
		vod = {
			"vod_id": array[0],
			"vod_name": title,
			"vod_pic": pic,
			"type_name": typeName,
			"vod_year": year,
			"vod_area": area,
			"vod_remarks": '',
			"vod_actor":  self.removeHtml(txt=act),
			"vod_director": self.removeHtml(txt=dir),
			"vod_content": self.removeHtml(txt=cont)
		}
		vod['vod_play_from'] = vod_play_from
		vod['vod_play_url'] = vod_play_url

		result = {
			'list': [
				vod
			]
		}
		return result

	def verifyCode(self):
		pass

	def searchContent(self,key,quick):
		Url='http://ktkkt.top/search.php?searchword={0}'.format(urllib.parse.quote(key))
		rsp = self.fetch(Url)
		htmlTxt = rsp.text
		videos = self.get_list(html=htmlTxt)
		result = {
				'list': videos
			}
		return result

	def playerContent(self,flag,id,vipFlags):
		result = {}
		Url='http://ktkkt.top{0}'.format(id)
		result["parse"] = 1
		result["playUrl"] = ''
		result["url"] = Url
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
			'Host': 'www.ktkkt2.com'
		}
		req = urllib.request.Request(url=urlStr, headers=headers)
		html = urllib.request.urlopen(req).read().decode('utf-8')
		return html
	def get_list(self,html):
		patternTxt=r'<a class="myui-vodlist.*?"\s*href="(.+?)" title="(.+?)"\s*data-original="(.+?)">'
		pattern = re.compile(patternTxt)
		ListRe=pattern.findall(html)
		videos = []
		for vod in ListRe:
			url = vod[0]
			title =vod[1]
			img =vod[2]
			if len(url) == 0:
				url = '_'
			videos.append({
				"vod_id":"{0}###{1}###{2}".format(title,url,img),
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
		'Host': 'ktkkt.top',
		"Referer": "http://ktkkt.top/"}

	def localProxy(self,param):
		return [200, "video/MP2T", action, ""]
