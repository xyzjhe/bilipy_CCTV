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
		return "Auete影视"
	def init(self,extend=""):
		pass
	def isVideoFormat(self,url):
		pass
	def manualVideoCheck(self):
		pass
	def homeContent(self,filter):
		result = {}
		cateManual = {
			"电影3": "Movie",
			"电视剧": "Tv",
			"综艺": "Zy",
			"动漫": "Dm",
			"其它":"qita",
			"音乐Mv": "Music"
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
		htmlTxt = self.get_webReadFile(urlStr='https://auete.com/')
		videos = self.get_list(html=htmlTxt)
		result = {
			'list': videos
		}
		return result

	def categoryContent(self,tid,pg,filter,extend):
		result = {}
		url='https://auete.com/{0}/index{1}.html'.format(tid,pg)
		htmlTxt = self.get_webReadFile(urlStr=url)
		numvL = len(videos)
		result['list'] = videos
		result['page'] = pg
		result['pagecount'] = 9999
		result['limit'] = numvL
		result['total'] = numvL
		return result

	def detailContent(self,array):
		aid = array[0].split('###')
		idUrl=aid[1]
		title=aid[0]
		pic=aid[2]
		result={}
		url='https://auete.com{0}'.format(idUrl)
		rsp = self.fetch(url)
		htmlTxt = rsp.text
		line=self.get_RegexGetTextLine(Text=htmlTxt,RegexText=r'<h2 class=".+?"><i class=".+?"></i>((.+?)<small><span style=".+?">(.+?))</span></small></h2>',Index=1)
		playFrom = []
		videoList=[]
		vodItems = []
		playFrom='无资源'
		if len(line)>0:
			circuit=self.get_lineList(Txt=htmlTxt,mark=r'<div id="player_list"',after='</div>')
			playFrom=[self.removeHtml(txt=t[1]) for t in line]
			pattern = re.compile(r'<a class="btn btn-orange"\s*title="(.+?)" href="(.+?)"')
			for v in circuit:
				ListRe=pattern.findall(v)
				vodItems = []
				for value in ListRe:
					vodItems.append(value[0]+"$"+value[1])
				joinStr = "#".join(vodItems)
				videoList.append(joinStr)
		
		vod_play_from='$$$'.join(playFrom)
		vod_play_url = "$$$".join(videoList)
		typeName=self.get_RegexGetText(Text=htmlTxt,RegexText=r'◎影片分类:(.+?)</p>',Index=1)
		year=self.get_RegexGetText(Text=htmlTxt,RegexText=r'◎上映年份:(.+?)</p>',Index=1)
		area=self.get_RegexGetText(Text=htmlTxt,RegexText=r'◎影片地区:(.+?)</p>',Index=1)
		act=self.get_RegexGetText(Text=htmlTxt,RegexText=r'◎影片主演:(.+?)</p>',Index=1)
		dir=self.get_RegexGetText(Text=htmlTxt,RegexText=r'◎影片导演:(.+?)</p>',Index=1)
		cont=self.get_RegexGetText(Text=htmlTxt,RegexText=r'◎影片简介:(.+?)<div',Index=1)
		rem=self.get_RegexGetText(Text=htmlTxt,RegexText=r'◎影片语言:(.+?)</p>',Index=1)

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
		Url='https://auete.com{0}'.format(id)
		rsp = self.fetch(Url)
		htmlTxt = rsp.text
		m3u8Line=self.get_RegexGetTextLine(Text=htmlTxt,RegexText=r'base64decode\("(.+?)"\)',Index=1)
		if len(m3u8Line)>0:
			strTxt=base64.b64decode(m3u8Line[0])
			strTxt=self.get_RegexGetText(Text=str(strTxt),RegexText=r"'{0,1}(http.+?\.m3u8)'{0,1}'",Index=1)
			Url=strTxt.replace("/","")
			if Url.find('(.m3u8')>1 or Url.find('(.mp4')>1:
				parse=0 
			else:
				Url='https://auete.com{0}'.format(id)
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
			'Host': 'auete.com'
		}
		req = urllib.request.Request(url=urlStr, headers=headers)
		html = urllib.request.urlopen(req).read().decode('utf-8')
		return html
	def get_list(self,html):
		patternTxt=r'data-tid="\d+?"><a\s*href="(.+?)"\s*class="pic"\s*target="_blank"><img\s*src="/img.php\?url=(.+?)"\s*alt="(.+?)"'
		pattern = re.compile(patternTxt)
		ListRe=pattern.findall(html)
		videos = []
		for vod in ListRe:
			url = vod[0]
			title =vod[2]
			img =vod[1]
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
		"filter": {}
	}
	header = {
		"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36",
		'Host': 'auete.com'
	}

	def localProxy(self,param):
		return [200, "video/MP2T", action, ""]
