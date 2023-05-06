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
		return "酷客影院"
	def init(self,extend=""):
		pass
	def isVideoFormat(self,url):
		pass
	def manualVideoCheck(self):
		pass
	def homeContent(self,filter):
		result = {}
		cateManual = {
			"电影": "dianying",
			"电视剧": "lianxuju",
			"综艺": "zongyi",
			"动漫": "dongman"
			#,"美女写真":"wuyejuchang"
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
		rsp = self.fetch('http://www.meheme.com/')
		htmlTxt = rsp.text
		videos = self.get_list(html=htmlTxt)
		result = {
			'list': videos
		}
		return result

	def categoryContent(self,tid,pg,filter,extend):
		result = {}
		classification=tid
		if 'classification' in extend.keys():
			classification=extend['classification']
		url='http://www.meheme.com/vodshow/{0}--------{1}---.html'.format(classification,pg)
		rsp = self.fetch(url)
		htmlTxt = rsp.text
		videos = self.get_list(html=htmlTxt,lkt=classification)
		pag=self.get_RegexGetText(Text=htmlTxt,RegexText=r'-(\d+?)---.html"\sclass="page-link page-next"\stitle="尾页">',Index=1)
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
		result={}
		url='http://www.meheme.com{0}'.format(idUrl)
		rsp = self.fetch(url)
		htmlTxt = rsp.text
		line=self.get_RegexGetTextLine(Text=htmlTxt,RegexText=r'class="active"\salt="(.+?)"\srel="nofollow">',Index=1)
		if len(line)<1:
			return result
		playFrom = []
		videoList=[]
		vodItems = []
		playFrom=['无资源']
		if len(line)>0:
			circuit=self.get_lineList(Txt=htmlTxt,mark=r'<ul class="content_playlist clearfix">',after='</div>')
			playFrom=[self.removeHtml(txt=t) for t in line]
			pattern = re.compile(r'<li><a href="(/.+?)" rel="nofollow">(.+?)</a></li>')
			for v in circuit:
				ListRe=pattern.findall(v)
				vodItems = []
				for value in ListRe:
					vodItems.append(value[1]+"$"+value[0])
				joinStr = "#".join(vodItems)
				videoList.append(joinStr)

		vod_play_from='$$$'.join(playFrom)
		vod_play_url = "$$$".join(videoList)
		typeName=self.get_RegexGetText(Text=htmlTxt,RegexText=r'类型：</span>(.+?)<span class="split_line">',Index=1)
		year=self.get_RegexGetText(Text=htmlTxt,RegexText=r'上映：</span>(.+?)<span class="split_line">',Index=1)
		area=self.get_RegexGetText(Text=htmlTxt,RegexText=r'地区：</span>(.+?)<span class="split_line">',Index=1)
		act=self.get_RegexGetText(Text=htmlTxt,RegexText=r'主演：</span>(.+?)<span class="split_line">',Index=1)
		dir=self.get_RegexGetText(Text=htmlTxt,RegexText=r'导演：</span>(.+?)<span class="split_line">',Index=1)
		cont=self.get_RegexGetText(Text=htmlTxt,RegexText=r'<div class="content_desc context clearfix"><span>(.+?)</span></div>',Index=1)
		rem=self.get_RegexGetText(Text=htmlTxt,RegexText=r'语言：</span>(.+?)<span class="split_line">',Index=1)

		vod = {
			"vod_id": array[0],
			"vod_name": title,
			"vod_pic": pic,
			"type_name":self.removeHtml(txt=typeName),
			"vod_year": self.removeHtml(txt=year),
			"vod_area": area,
			"vod_remarks": rem,
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
		Url='http://www.meheme.com/vodsearch/-------------.html?wd={0}&submit='.format(urllib.parse.quote(key))
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
		Url='http://www.meheme.com{0}'.format(id)
		rsp = self.fetch(Url)
		htmlTxt = rsp.text
		m3u8Line=self.get_RegexGetTextLine(Text=htmlTxt,RegexText=r'url":"(h.+?)",',Index=1)
		if len(m3u8Line)>0:
			Url=m3u8Line[0].replace("/","")
		if Url.find('.m3u8')<1:
			parse=0
			Url='http://www.meheme.com{0}'.format(id)
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
			'Host': 'www.kukemv.com'
		}
		req = urllib.request.Request(url=urlStr, headers=headers)
		html = urllib.request.urlopen(req).read().decode('utf-8')
		return html
	def get_list(self,html,lkt):
		patternTxt=r'<a class="vodlist_thumb lazyload" href="(.+?)" title="(.+?)" data-original="(.+?)"'
		pattern = re.compile(patternTxt)
		ListRe=pattern.findall(html)
		videos = []
		for vod in ListRe:
			url = vod[0]
			title =lkt+vod[1]
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
		"filter": {
		"dianying":[
		{"key":"classification","name":"分类","value":[{"n":"全部","v":"dianying"},{"n":"动作片","v":"dongzuopian"}]}

		#分隔
		]


		#分隔
		}
		}
	header = {
		"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36",
		'Host': 'www.kukemv.com'
	}

	def localProxy(self,param):
		return [200, "video/MP2T", action, ""]
