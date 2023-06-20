#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
sys.path.append('..') 
import re
from urllib import request, parse
import urllib
import urllib.request
import time
import base64

class Spider(Spider):
	def getName(self):
		return "看看美剧"
	def init(self,extend=""):
		pass
	def isVideoFormat(self,url):
		pass
	def manualVideoCheck(self):
		pass
	def homeContent(self,filter):
		result = {}
		cateManual = {
			"美剧": "1",
			"其他剧": "10",
			"动漫": "15",
			"排行榜":"46"
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
		#if 'classification' in extend.keys():
			#classification=extend['classification']
		url='https://www.kankanmeiju.com/vodlist/{0}_{1}.html'.format(tid,pg)
		htmlTxt =self.webReadFile(urlStr=url,header=self.header)
		
		videos = self.get_list(html=htmlTxt,patternTxt=r'<a class="link" href="(?P<url>.+?)" title="(?P<title>.+?)"><div class="pic"><div class="img"><img class="lazy" data-original="(?P<img>.+?)" src=".+?" alt=".+?"><span class="over"></span><span class="ico player-ico"></span><span class="state"><span class="bg2"></span><span class="ico lzpng ztpng">(?P<brief>.+?)</span>')
		
		pag=999#self.get_RegexGetText(Text=htmlTxt,RegexText=r'<a href="/vodlist/\d+?_\d+?.html">\.\.(\d+?)</a>',Index=1)
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
		htmlTxt = self.webReadFile(urlStr=idUrl,header=self.header)
		
		line=self.get_RegexGetTextLine(Text=htmlTxt,RegexText=r'<li id=".+?" onclick="setTab.+?"><i class=".+?m3u8"></i>(.+?)</li>',Index=1)
		
		if len(line)<1:
			return result
		playFrom = []
		videoList=[]
		vodItems = []
		playFrom=['无资源']
		if len(line)>0:
			circuit=self.get_lineList(Txt=htmlTxt,mark=r'<ul class="playul">',after='</ul>')
			playFrom=[self.removeHtml(txt=t) for t in line]
			

			pattern = re.compile(r"<a title='.+?' href='(.+?)' target=\".*?\">(.+?)</a>")
			for v in circuit:
				ListRe=pattern.findall(v)
				vodItems = []
				for value in ListRe:
					vodItems.append(value[1]+"$"+'https://www.kankanmeiju.com'+value[0])
				joinStr = "#".join(vodItems)
				videoList.append(joinStr)
		vod_play_from='$$$'.join(playFrom)
		vod_play_url = "$$$".join(videoList)
		typeName=self.get_RegexGetText(Text=htmlTxt,RegexText=r'类型：</span>(.*?)</em></dd><dd><em><span>更新：',Index=1)
		temporary=self.get_RegexGetTextLine(Text=htmlTxt,RegexText=r'>([0-9]{4})</a>',Index=1)
		year="/".join(temporary)


		area=self.get_RegexGetText(Text=htmlTxt,RegexText=r'<a href="/search.php\?searchword=.+?">(.+?)</a>',Index=1)
		temporary=self.get_RegexGetTextLine(Text=htmlTxt,RegexText=r"<a href='/search.php\?searchword=.+?'>(.+?)</a>",Index=1)
		act="/".join(temporary)
		temporary=self.get_RegexGetTextLine(Text=htmlTxt,RegexText=r"导演：</span><a href='/search.php\?searchword=.+?'>(.+?)</a>",Index=1)
		dir="/".join(temporary)
		act=act.replace(dir+'/','')
		cont=self.get_RegexGetText(Text=htmlTxt,RegexText=r'<div class="cdes clearfix"><p>(.+?)</p></div>',Index=1)
		rem=self.get_RegexGetText(Text=htmlTxt,RegexText=r'语言：</span>(.+?)</em>',Index=1)
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
		data="searchword="+urllib.parse.quote(key)
		payUrl="https://www.kankanmeiju.com/search.php"
		req = request.Request(url=payUrl, data=bytes(data, encoding='utf8'),headers=self.header, method='POST')
		response = request.urlopen(req)
		htmlTxt = response.read().decode('utf-8')
		videos = self.get_list(html=htmlTxt,patternTxt=r'href="(?P<url>.+?)" title="(?P<title>.+?)"><div class="pic"><div class="img"><img class="lazy" data-original="(?P<img>.+?)" src=".*?" alt=".*?"></div><div class="info"><p class="name">.*?</p><p class="zt">(?P<brief>.+?)</p>')
		result = {
				'list': videos
			}
		return result

	def playerContent(self,flag,id,vipFlags):
		result = {}
		parse=1
		Url=id
		htmlTxt = self.webReadFile(urlStr=Url,header=self.header)
		m3u8Line=self.get_RegexGetTextLine(Text=htmlTxt,RegexText=r'var now="(.+?\.m3u8)"',Index=1)
		if len(m3u8Line)>0:
			Url=m3u8Line[0].replace("\\","")
		if Url.find('.m3u8')<1:
			parse=0
			Url=id
		result["parse"] = parse
		result["playUrl"] = ''
		result["url"] = Url
		result["header"] = ''
		return result	
	
	def localProxy(self,param):
		return [200, "video/MP2T", action, ""]
	config = {
		"player": {},
		"filter": {}
		}
	header = {
		"User-Agent":"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36",
		#'Host': 'www.kankanmeiju.com',
		'referer':'https://www.kankanmeiju.com/'
	}

	#-----------------------------------------------自定义函数-----------------------------------------------
	#访问网页
	def webReadFile(self,urlStr,header):
		html=''
		req=urllib.request.Request(url=urlStr,headers=header)#,headers=header
		with  urllib.request.urlopen(req)  as response:
			html = response.read().decode('utf-8')
		return html
	#正则取文本
	def get_RegexGetText(self,Text,RegexText,Index):
		returnTxt=""
		Regex=re.search(RegexText, Text, re.M|re.S)
		if Regex is None:
			returnTxt=""
		else:
			returnTxt=Regex.group(Index)
		return returnTxt
	#取集数
	def get_EpisodesList(self,html,RegexText):
		ListRe=re.finditer(RegexText, html, re.M|re.S)
		videos = []
		head="https://www.xiguazx.com"
		for vod in ListRe:
			url = vod.group('url')
			title =vod.group('title')
			if len(url) == 0:
				continue
			videos.append(self.removeHtml(txt=title)+"$"+head+url)
			#print(title)
		return videos
	#取剧集区
	def get_lineList(self,Txt,mark,after):
		circuit=[]
		origin=Txt.find(mark)
		while origin>8:
			end=Txt.find(after,origin)
			circuit.append(Txt[origin:end])
			origin=Txt.find(mark,end)
		return circuit	
	#正则取文本,返回数组	
	def get_RegexGetTextLine(self,Text,RegexText,Index):
		returnTxt=[]
		pattern = re.compile(RegexText, re.M|re.S)
		ListRe=pattern.findall(Text)
		if len(ListRe)<1:
			return returnTxt
		for value in ListRe:
			returnTxt.append(value)	
		return returnTxt
	#分类取结果
	def get_list(self,html,patternTxt):
		ListRe=re.finditer(patternTxt, html, re.M|re.S)
		videos = []
		head="https://www.kankanmeiju.com"
		for vod in ListRe:
			url = vod.group('url')
			title =self.removeHtml(txt=vod.group('title'))
			img =vod.group('img')
			if len(url) == 0:
				continue
			if len(img)<5:
				img='https://www.xiguazx.com/template/mxone/mxstatic/image/loading.gif'
			else:
				img='https://www.kankanmeiju.com'+img
			brief=vod.group('brief')
			videos.append({
				"vod_id":"{0}###{1}###{2}".format(title,head+url,img),
				"vod_name":title,
				"vod_pic":img,
				"vod_remarks":brief
			})
		return videos
	#删除html标签
	def removeHtml(self,txt):
		soup = re.compile(r'<[^>]+>',re.S)
		txt =soup.sub('', txt)
		return txt.replace("&nbsp;"," ")
	def get_playlist(self,Text,headStr,endStr):
		circuit=""
		origin=Text.find(headStr)
		if origin>8:
			end=Text.find(endStr,origin)
			circuit=Text[origin:end]
		return circuit