#coding=utf-8
#!/usr/bin/python
import sys
sys.path.append('..') 
from base.spider import Spider
import base64
from urllib import request, parse
import urllib
import urllib.request
import base64
import re
import time
class Spider(Spider):  # 元类 默认的元类 type
	def getName(self):
		return "555电影"
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
			"电影": "1",
			"连续剧":"2",
			"动漫":"4",
			"综艺":"3"
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
		htmlTxt=self.webReadFile(urlStr='https://fskc177.com/',header=self.header)
		videos=self.get_list(html=htmlTxt,patternTxt=r'<a href="(?P<url>.+?)" title="(?P<title>.+?)"\s*\n*\s*class="module-poster-item module-item">\s*\n*\s*<div class="module-item-cover">\s*\n*\s*<div class="module-item-note">(?P<renew>.+?)</div>\s*\n*\s*<div class="module-item-douban">.*?</div>\s*\n*\s*<div class="module-item-pic"><img class="lazy lazyload" data-original="(?P<img>.+?)"')
		
		result = {
			'list':[]
		}
		return result
	def categoryContent(self,tid,pg,filter,extend):
		result = {}
		videos=[]
		classification=''
		url='https://www.555hd4.com/vodshow/{0}--------{1}---.html'.format(tid,pg)
		htmlTxt=self.webReadFile(urlStr=url,header=self.header)
		videos=self.get_list(html=htmlTxt,patternTxt=r'<a href="(?P<url>.+?)" title="(?P<title>.+?)"\s*\n*\s*class="module-poster-item module-item">\s*\n*\s*<div class="module-item-cover">\s*\n*\s*<div class="module-item-note">(?P<renew>.+?)</div>\s*\n*\s*<div class="module-item-douban">.*?</div>\s*\n*\s*<div class="module-item-pic"><img class="lazy lazyload" data-original="(?P<img>.+?)"')
		pagecount=self.get_RegexGetText(Text=htmlTxt,RegexText=r'<a href="/vodshow/\d+?--------(\d+?)---.html" class="page-link page-next" title="尾页">尾页</a>',Index=1)
		if pagecount=='':
			pagecount=999
		result['list'] = videos
		result['page'] = pg
		result['pagecount'] = pagecount
		result['limit'] = 90
		result['total'] = 999999
		return result
	def detailContent(self,array):
		result = {}
		aid = array[0].split('###')
		logo = aid[2]
		url = aid[1]
		title = aid[0]
		vodItems=[]
		vod_play_from=['线路',]
		vod_play_url=[]
		htmlTxt=self.webReadFile(urlStr=url,header=self.header)
		
		vod_play_from=self.get_RegexGetTextLine(Text=htmlTxt,RegexText=r'<div class=".+?" data-dropdown-value="(.+?)"><span>.+?</span><small>\d*?</small></div>',Index=1)
		
		circuit=self.get_lineList(Txt=htmlTxt,mark=r'<div class="module-play-list">',after='</div>')
		for t in circuit:
			vodItems=self.get_EpisodesList(html=t,RegexText=r'<a\s+?class="module-play-list-link" href="(?P<url>.+?)" title=".+?">(?P<title>.+?)</a>')
			joinStr = "#".join(vodItems)
			vod_play_url.append(joinStr)

		temporary=self.get_RegexGetTextLine(Text=htmlTxt,RegexText=r'<a href="/vodshow/\d+?---.+?--------.html">(.+?)</a>',Index=1)
		typeName="/".join(temporary)
		year=self.get_RegexGetText(Text=htmlTxt,RegexText=r'href="/vodshow/\d+?-----------\d{4}.html">(\d{4})</a>',Index=1)
		temporary=self.get_RegexGetTextLine(Text=htmlTxt,RegexText=r'href="/vodshow/\d+?-.+?----------.html">(.+?)</a>',Index=1)
		area="/".join(temporary)#地区
		temporary=self.get_RegexGetTextLine(Text=htmlTxt,RegexText=r'<a href="/vodsearch/-.+?------------.html" target="_blank">(.+?)</a>',Index=1)
		actor="/".join(temporary)#演员
		temporary=self.get_RegexGetTextLine(Text=htmlTxt,RegexText=r'<a href="/vodsearch/-----.+?--------.html" target="_blank">(.+?)</a>',Index=1)
		director="/".join(temporary)#导演
		content=self.get_RegexGetText(Text=htmlTxt,RegexText=r'<p>(.+?)</p>',Index=1)
		vod = {
			"vod_id":array[0],
			"vod_name":title,
			"vod_pic":logo,
			"type_name":typeName,
			"vod_year":self.removeHtml(txt=year),
			"vod_area":self.removeHtml(txt=area),
			"vod_remarks":"",
			"vod_actor":self.removeHtml(txt=actor),
			"vod_director":self.removeHtml(txt=director),
			"vod_content":self.removeHtml(txt=content)
		}
		H=time.strftime("%H", time.localtime())
		if int(H)<22 and typeName.find('伦理')>-1:
			return result
		vod['vod_play_from'] =  "$$$".join(vod_play_from)
		vod['vod_play_url'] = "$$$".join(vod_play_url)
		result = {
			'list':[
				vod
			]
		}
		return result
	def searchContent(self,key,quick):
		Url='https://www.555hd4.com/vodsearch/-------------.html?wd='+urllib.parse.quote(key)
		htmlTxt=self.webReadFile(urlStr=Url,header=self.header)
		videos=self.get_list(html=htmlTxt,patternTxt=r'<a href="(?P<url>.+?)" class="module-card-item-poster">\s*\n*\s*.*\s*\n*\s*<div class=".+?">(?P<renew>.+?)</div>\s*\n*\s*.*\s*\n*\s*<div class="module-item-pic"><img class="lazy lazyload" data-original="(?P<img>.+?)" alt="(?P<title>.+?)"')
		result = {
			'list':videos
		}
		return result
	def playerContent(self,flag,id,vipFlags):
		result = {}
		result["parse"] = 1
		result["playUrl"] = ''
		result["url"] = id
		result["header"] = ''	
		return result
	
	def localProxy(self,param):
		return [200, "video/MP2T", action, ""]
	config = {
		"player": {},
		"filter": {}
		}
	header = {
		"Referer": 'https://www.555hd4.com/',
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
		"Host":'www.555hd4.com'
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
		head="https://fskc177.com"
		for vod in ListRe:
			url = vod.group('url')
			title =vod.group('title')
			if len(url) == 0:
				continue
			videos.append(self.removeHtml(txt=title)+"$"+head+url)
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
		head="https://55dy1.vip"
		for vod in ListRe:
			url = vod.group('url')
			title =self.removeHtml(txt=vod.group('title'))
			img =vod.group('img')
			renew=vod.group('renew')
			if len(url) == 0:
				continue
			if len(img)<5:
				img='https://t1.szrtcpa.com/2022/08/01/ac6f199bfdf7c.gif'
			videos.append({
				"vod_id":"{0}###{1}###{2}".format(title,head+url,img),
				"vod_name":title,
				"vod_pic":img,
				"vod_remarks":renew
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
		RegexTxt=r'(youku.com|v.qq|bilibili|iqiyi.com|tv.cctv|c(c|n)tv|v.pptv)'
		if self.get_RegexGetText(Text=url,RegexText=RegexTxt,Index=1)!='':
			Isjiexi=1
		return Isjiexi