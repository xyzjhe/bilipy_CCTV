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
		return "555电影"
	def init(self,extend=""):
		pass
	def isVideoFormat(self,url):
		pass
	def manualVideoCheck(self):
		pass
	def homeContent(self,filter):
		result = {}
		cateManual = {
			"电影": "1",
			"连续剧": "2",
			"综艺": "3",
			"动漫": "4",
			"福利":"124"
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
		rsp = self.fetch('https://www.5dy6.cc/')
		htmlTxt = rsp.text
		videos = self.get_list(html=htmlTxt)
		result = {
			'list': videos
		}
		return result

	def categoryContent(self,tid,pg,filter,extend):
		result = {}
		url = 'https://www.5dy6.cc/vodshow/{0}--------{1}---.html'.format(tid,pg)
		rsp = self.fetch(url,headers=self.header)
		htmlTxt=rsp.text
		videos = self.get_list(html=htmlTxt)
		pag=self.get_RegexGetText(Text=htmlTxt,RegexText=r'<a href="/vodshow/\d+?--------(.+?)---.html" class="page-link page-next" title="尾页">尾页</a>',Index=1)
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
		aid = array[0].split('###')
		idUrl=aid[1]
		title=aid[0]
		pic=aid[2]
		Url='https://www.5dy6.cc{0}'.format(idUrl)
		rsp = self.fetch(Url,headers=self.header)
		htmlTxt=rsp.text	
		line=self.get_RegexGetTextLine(Text=htmlTxt,RegexText=r'ata-dropdown-value="(.+?)">(.+?)</div>',Index=1)
		playFrom = []
		videoList=[]
		vodItems = []
		if len(line)>0:
			circuit=self.get_lineList(Txt=htmlTxt,mark=r'<div class="module-play-list">',after='</div>')
			pattern = re.compile(r'href="(.+?)" title="(.+?)">')
			for v in circuit:
				ListRe=pattern.findall(v)
				vodItems=[]
				for value in ListRe:
					vodItems.append(value[1]+"$"+value[0])
					joinStr = "#".join(vodItems)
				videoList.append(joinStr)
					
			
		playFrom=[t[0] for t in line]
		vod_play_from='$$$'.join(playFrom)
		vod_play_url = "$$$".join(videoList)
		title=aid[0]
		pic=aid[2]
		typeName=self.get_RegexGetText(Text=htmlTxt,RegexText=r'<div class="module-info-tag-link">(.+)</div>',Index=1)
		year=self.get_RegexGetText(Text=htmlTxt,RegexText=r'href="/vodshow/\d+?-----------\d{4}.html">(\d{4})</a>',Index=1)
		area=self.get_RegexGetText(Text=htmlTxt,RegexText=r'<div class="module-info-tag-link">(.+)</div>',Index=1)
		act=self.get_RegexGetText(Text=htmlTxt,RegexText=r'主演：</span>(.+?)</a>',Index=1)
		dir=self.get_RegexGetText(Text=htmlTxt,RegexText=r'导演：</span>(.+?)</a>',Index=1)
		cont=self.get_RegexGetText(Text=htmlTxt,RegexText=r'<div class="module-info-introduction-content show-desc".*?>(.+?)</div>',Index=1)
		rem=""#self.get_RegexGetText(Text=htmlTxt,RegexText=r'语言：</span>(.+?)<span class="split_line">',Index=1)
		vod = {
			"vod_id": array[0],
			"vod_name": title,
			"vod_pic": pic,
			"type_name":removeHtml(txt=typeName),
			"vod_year": removeHtml(txt=year),
			"vod_area": area,
			"vod_remarks": rem,
			"vod_actor":removeHtml(txt=act),
			"vod_director":removeHtml(txt=dir),
			"vod_content": removeHtml(txt=cont)
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
		Url='https://www.5dy6.cc/vodsearch/-------------.html?wd='.format(urllib.parse.quote(key))
		rsp = self.fetch(Url)
		htmlTxt = rsp.text
		videos = self.get_list(html=htmlTxt)
		result = {
				'list': videos
			}
		return result

	def playerContent(self,flag,id,vipFlags):
		result = {}
		Url='https://www.5dy6.cc{0}'.format(id)
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
			'Host': 'www.ikmjw.com'
		}
		req = urllib.request.Request(url=urlStr, headers=headers)
		html = urllib.request.urlopen(req).read().decode('utf-8')
		return html
	def get_list(self,html):
		patternTxt=r'<a href="(.+?)"\s*title="(.+?)"\s*class="module-poster-item module-item">(\r|\n|\r\n)\s*<div class="module-item-cover">(\r|\n|\r\n)\t+?<div class="module-item-note">(.+?)</div>'
		pattern = re.compile(patternTxt)
		ListRe=pattern.findall(html)
		PicPattern = re.compile(r'<img class="lazy lazyload" data-original="(.+?)"')
		PicListRe=PicPattern.findall(html)
		videos = []
		for i in range(0, len(ListRe)):
			url = ListRe[i][0]
			title =ListRe[i][1]
			img =PicListRe[i]
			if len(url) == 0:
				url = '_'
			if len(img) == 0:
				img='https://t1.szrtcpa.com/2022/08/01/ac6f199bfdf7c.gif'
			videos.append({
				"vod_id":"{0}###{1}###{2}".format(title,url,img),
				"vod_name":title,
				"vod_pic":img,
				"vod_remarks":''
			})
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
		'Host': 'www.5dy6.cc'
	}

	def localProxy(self,param):
		return [200, "video/MP2T", action, ""]
