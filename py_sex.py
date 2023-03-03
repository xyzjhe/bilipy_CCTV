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
		return "新视觉影视"
	def init(self,extend=""):
		pass
	def isVideoFormat(self,url):
		pass
	def manualVideoCheck(self):
		pass
	def homeContent(self,filter):
		result = {}
		cateManual = {
			"亚洲": "uncd",
			"国产": "madou",
			"欧美": "oua",
			"动漫": "hmmcg"
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
		url = 'https://159i22.cc/video/{0}/{1}.html'.format(tid,pg)
		rsp = self.fetch(url)
		htmlTxt=rsp.text
		videos = self.get_list(html=htmlTxt)
		pag=self.get_RegexGetText(Text=htmlTxt,RegexText=r'-(\d+?)---.html"\sclass="page-link page-next"\stitle="尾页">',Index=1)
		if pag=="":
			pag=999
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
		if aid[1].find("http")<0:
			return result
		logo = aid[2]
		url = aid[1]
		title = aid[0]
		if url == '_':
			return result
		vodItems = [title+"$"+url]
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
		patternTxt=r'<a href="(.+?)" rel="bookmark">(.+?)</a>'
		pattern = re.compile(patternTxt)
		ListRe=pattern.findall(html)
		URLpattern = re.compile(r"url: '(.+?)',\r\n.*pic:'(.+?)'")
		URLListRe=URLpattern.findall(html)
		i=0
		videos = []
		for vod in URLListRe:
			lastVideo = vod[0]
			title =ListRe[i]
			img =vod[1]
			if len(lastVideo) == 0:
				lastVideo = '_'
			videos.append({
				"vod_id":title+"###"+lastVideo+"###"+img,
				"vod_name":title,
				"vod_pic":img,
				"vod_remarks":''
			})
			i=i+1
		return videos
	def get_lineList(self,Txt,mark,after):
		circuit=[]
		origin=Txt.find(mark)
		while origin>8:
			end=Txt.find(after,origin)
			circuit.append(Txt[origin:end])
			origin=Txt.find(mark,end)
		return circuit
	config = {
		"player": {},
		"filter": {}
	}
	header = {
		"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36",
		'Host': '159i22.cc'
	}

	def localProxy(self,param):
		return [200, "video/MP2T", action, ""]
