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
		return "酷狗MV"
	def init(self,extend=""):
		pass
	def isVideoFormat(self,url):
		pass
	def manualVideoCheck(self):
		pass
	def homeContent(self,filter):
		result = {}
		cateManual = {
			"新歌推荐": "9",
			"华语精选": "13",
			"日韩精选": "17",
			"欧美精选": "16"
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
		rsp = self.fetch('https://www.ktkkt2.com/')
		htmlTxt = rsp.text
		videos = self.get_list(html=htmlTxt)
		result = {
			'list': videos
		}
		return result

	def categoryContent(self,tid,pg,filter,extend):
		result = {}
		url = 'https://www.kugou.com/mvweb/html/index_{0}_{1}.html'.format(tid,pg)
		rsp = self.fetch(url,headers=self.header)
		htmlTxt=rsp.text
		videos = self.get_list(html=htmlTxt,typeName='MV')
		pag=self.get_RegexGetText(Text=htmlTxt,RegexText=r'<label id="mvNum">(\d+?)</label>',Index=1)
		if pag=="":
			pag=2
		else:
			pag=int(pag)/20
		numvL = len(videos)
		result['list'] = videos
		result['page'] = pg
		result['pagecount'] = int(pag)
		result['limit'] = numvL
		result['total'] = numvL
		return result

	def detailContent(self,array):
		aid = array[0].split('###')
		idUrl=aid[1]
		title=aid[0]
		pic=aid[2]
		vodItems = [title+"$"+url]
		typeName=aid[4]
		vod = {
			"vod_id": array[0],
			"vod_name": title,
			"vod_pic": pic,
			"type_name": typeName,
			"vod_year": '',
			"vod_area": '',
			"vod_remarks": "",
			"vod_actor":  '',
			"vod_director": '',
			"vod_content": ''
		}
		vod['vod_play_from'] = '酷狗'
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
		Url='https://www.ktkkt2.com/search.php?searchword={0}'.format(urllib.parse.quote(key))
		rsp = self.fetch(Url)
		htmlTxt = rsp.text
		videos = self.get_list(html=htmlTxt)
		result = {
				'list': videos
			}
		return result

	def playerContent(self,flag,id,vipFlags):
		result = {}
		parse=1
		Url=id
		result["parse"] = parse
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
	def get_list(self,html,typeName):
		patternTxt=r'<a target="_blank" href="(.+?)" title="(.+?)">'
		pattern = re.compile(patternTxt)
		ListRe=pattern.findall(html)
		patternTxt=r'<img\s*src=".+?"\s*_src="(.+?)"\s*width="\d+?"\s*height="\d+?"\s*/>'
		imgPattern = re.compile(patternTxt)
		imgListRe=imgPattern.findall(html)
		videos = []
		for i in range(0,len(ListRe)):
			url = ListRe[i][0]
			title =ListRe[i][1]
			img =imgListRe[i]
			if len(url) == 0:
				url = '_'
			actor=''
			strLine=title.split('-')
			if len(strLine)>1:
				actor=strLine[0] 
				title=strLine[1]
			videos.append({
				"vod_id":"{0}###{1}###{2}###{3}###{4}".format(title,url,img,actor,typeName),
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
		'Host': 'www.kugou.com',
		"Referer": "https://www.kugou.com/"}

	def localProxy(self,param):
		return [200, "video/MP2T", action, ""]
