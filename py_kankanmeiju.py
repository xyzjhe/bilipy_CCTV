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
import time

class Spider(Spider):  # 元类 默认的元类 type
	def getName(self):
		return "看看美剧"
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
			"美剧": "1",
			"其他剧": "10",
			"动漫": "15",
			"排行榜":"46"
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
		classification=tid
		#if 'classification' in extend.keys():
			#classification=extend['classification']
		url='https://www.kankanmeiju.com/vodlist/{0}_{1}.html'.format(classification,pg)
		htmlTxt = self.webReadFile(urlStr=url,header=self.header)
		
		videos = self.get_list(html=htmlTxt,patternTxt=r'<a class="link" href="(?P<url>.+?)" title="(?P<title>.+?)"><div class="pic"><div class="img"><img class="lazy" data-original="(?P<img>.+?)" src=".+?" alt=".+?"><span class="over"></span><span class="ico player-ico"></span><span class="state"><span class="bg2"></span><span class="ico lzpng ztpng">(?P<brief>.+?)</span>')
		
		pag=self.get_RegexGetText(Text=htmlTxt,RegexText=r'<a href="/vodlist/\d+?_\d+?.html">\.\.(\d+?)</a>',Index=1)
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
		result = {}
		aid = array[0].split('###')
		tid = aid[0]
		logo = aid[3]
		url = aid[2]
		title = aid[1]
		vodItems=[]
		vod_play_from=['线路',]
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
		vod['vod_play_from'] =  "$$$".join(vod_play_from)
		vod['vod_play_url'] = "$$$".join(vodItems)
		result = {
			'list':[
				vod
			]
		}
		return result
	def get_lineList(self,Txt,mark,after):
		circuit=[]
		origin=Txt.find(mark)
		while origin>8:
			end=Txt.find(after,origin)
			circuit.append(Txt[origin:end])
			origin=Txt.find(mark,end)
		return circuit	
	def searchContent(self,key,quick):
		result = {
			'list':[]
		}
		return result
	def playerContent(self,flag,id,vipFlags):
		result = {}
		headers = {
			'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'
		}
		parse=1
		jx=self.ifJx(urlTxt=id)
		if jx==1:
			parse=1
		if self.get_RegexGetText(Text=id,RegexText=r'(\.mp4)',Index=1)!='':
			parse=0
		result["parse"] = 0
		result["playUrl"] =''
		result["url"] = 'tvbox-xg:ftp://a.gbl.114s.com:20320/0502/银河护卫队3-2023_HD中英双字IMAX版.mp4'
		result['jx'] = jx#VIP解析
		result["header"] = headers	
		return result
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
	#是否是vip解析
	def ifJx(self,url):
		Isjiexi=0
		RegexTxt=r'(youku.com|v.qq|bilibili|iqiyi.com|tv.cctv|c(c|n)tv|v.pptv|mgtv.com)'
		if self.get_RegexGetText(Text=url,RegexText=RegexTxt,Index=1)!='':
			Isjiexi=1
		return Isjiexi

	def localProxy(self,param):
		return [200, "video/MP2T", action, ""]
