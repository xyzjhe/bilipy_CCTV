#coding=utf-8
#!/usr/bin/python
import sys
sys.path.append('..') 
from base.spider import Spider
import base64
import re
from urllib import request, parse
import urllib
import urllib.request

class Spider(Spider):  # 元类 默认的元类 type
	def getName(self):
		return "西瓜影视"
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
			"电影": "55",
			"连续剧": "72",
			"动漫": "78",
			"综艺": "80",
			"哔哩哔哩": "82"
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
		videos=[]
		types=tid
		captions=''#字母='/letter/'+extend['captions']
		url='https://www.xiguazx.com/index.php/vod/show/id/{0}{2}/page/{1}.html'.format(types,pg,captions)
		
		htmlTxt=self.webReadFile(urlStr=url,header=self.header)
		
		videos=self.get_list(html=htmlTxt,patternTxt=r'<div class="module-item-pic">\s*\n*\s*<a href="(?P<url>.+?)" title="(?P<title>.+?)" >\s*\n*\s*<i class="icon-play"></i>\s*\n*\s*</a>\s*\n*\s*<img class="lazy lazyloaded"\s*\n*\s*data-src="(?P<img>.+?)"')
		
		listCount=len(videos)
		pagecount=self.get_RegexGetText(Text=htmlTxt,RegexText=r'<a href="/index.php/vod/show/id/'+types+'/page/(\d+?).html" class="page-number page-next" title="尾页">尾页</a>',Index=1)
		#print(pagecount)
		if pagecount=='':
			pagecount=999
		result['list'] = videos
		result['page'] = pg
		result['pagecount'] =pg if listCount<1 else int(pagecount)
		result['limit'] = listCount
		result['total'] = 99999
		return result

	def detailContent(self,array):		
		result = {}
		aid = array[0].split('###')
		title = aid[0]#片名
		urlId = ''+aid[1]#URL
		logo = aid[2]#封面
		year=''#年份
		area=''
		actor=''
		director=''
		content=''
		vodItems=[]
		typeName=''
		vod_play_from=[]#线路
		vod_play_url=[]#剧集

		htmlTxt=self.webReadFile(urlStr=urlId,header=self.header)
		vod_play_from=self.get_RegexGetTextLine(Text=htmlTxt,RegexText=r'<div class="module-tab-item tab-item" data-dropdown-value="(.+?)"><span>.+?</span><small>\d+?</small></div>',Index=1)
		
		if len(vod_play_from)<1:
			return  {'list': []}
		circuit=self.get_lineList(Txt=htmlTxt,mark=r' <div class="sort-item" id="sort-item',after='</div>')
		#print(circuit)
		for v in circuit:
			vodItems = self.get_EpisodesList(html=v,RegexText=' <a href="(?P<url>.+?)" title=".+?">(?P<title>.+?)</a>')
			joinStr = "#".join(vodItems)
			vod_play_url.append(joinStr)
			#print(vod_play_url)
		typeName=self.get_RegexGetText(Text=htmlTxt,RegexText=r'<br/>◎类　　别　(.+?)<br/>',Index=1)
		year=self.get_RegexGetText(Text=htmlTxt,RegexText=r'<br/>◎年　　代　([0-9]{4})<br/>',Index=1)
		area=self.get_RegexGetText(Text=htmlTxt,RegexText=r'<br/>◎产　　地　(.+?)<br/>',Index=1)
		actor=self.get_RegexGetText(Text=htmlTxt,RegexText=r'<br/>◎演　　员　(.+?)◎',Index=1)
		director=self.get_RegexGetText(Text=htmlTxt,RegexText=r'<br/>◎导　　演　(.+?)◎',Index=1)
		content=self.get_RegexGetText(Text=htmlTxt,RegexText=r'◎简　　介(.+?)<img',Index=1)
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
		vod['vod_play_from'] =  "$$$".join(vod_play_from)
		vod['vod_play_url'] = "$$$".join(vod_play_url)
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

		data="show=title&tempid=1&tbname=article&mid=1&dopost=search&submit=&keyboard="+urllib.parse.quote(key)
		payUrl="https://www.66s.cc/e/search/index.php"
		req = request.Request(url=payUrl, data=bytes(data, encoding='utf8'),headers=headers, method='POST')
		response = request.urlopen(req)
		urlTxt=response.geturl()
		response = urllib.request.urlopen(urlTxt)
		htmlTxt=response.read().decode('utf-8')
		videos = self.get_list(html=htmlTxt,patternTxt=r'<div class="thumbnail">\s*\n*\s*<a href="(?P<url>.+?)" class="zoom" rel="bookmark" title="(?P<title>.+?)">\s*\n*\s*<img src="(?P<img>.+?)" alt=".*?"\s*/>\s*</a>\s*\n*\s*</div>\s*\n*\s* <div class="article">')
		result = {
			'list':videos
		}
		return result
	
	def playerContent(self,flag,id,vipFlags):
		result = {}
		parse=0
		url=""
		htmlTxt=self.webReadFile(urlStr=id,header=self.header)
		m3u8Line=self.get_RegexGetTextLine(Text=htmlTxt,RegexText=r'url":"(\w+?)",',Index=1)
		if len(m3u8Line)>0:
			url=m3u8Line[0].replace("/","")
			url=str(base64.b64decode(url),'utf-8')
			url=urllib.parse.unquote(url)
		if url.find('.m3u8')>1:
			parse=0
		else:
			url=id
		result["parse"] = parse
		result["playUrl"] =""
		result["url"] = url
		result["header"] = ''
		return result
	def localProxy(self,param):
		pass
	config = {
		"player": {},
		"filter": {
		"dianshiju":[
		{"key":"cat","name":"类型","value":[{"n":"全部","v":"dianshiju"},{"n":"国剧","v":"guoju"},{"n":"日韩剧","v":"rihanju"},{"n":"欧美剧","v":"oumeiju"}]},
		]
		}
		}
	header = {
		"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36",
		"Host": "www.xiguazx.com",
		"Referer": "https://www.xiguazx.com/"
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
		head="https://www.xiguazx.com"
		for vod in ListRe:
			url = vod.group('url')
			title =self.removeHtml(txt=vod.group('title'))
			img =vod.group('img')
			#renew=vod.group('renew')
			if len(url) == 0:
				continue
			if len(img)<5:
				img='https://www.xiguazx.com/template/mxone/mxstatic/image/loading.gif'
			#print(title)
			videos.append({
				"vod_id":"{0}###{1}###{2}".format(title,head+url,img),
				"vod_name":title,
				"vod_pic":img,
				"vod_remarks":""
			})
		Re=pattern = re.compile('<div class="module-item-caption">\s*\n*\s*<span>(.+?)</span>', re.M|re.S)
		List=Re.findall(html)
		if len(List)==len(videos):
			for i in range(0,len(List)):
				videos[i]['vod_remarks']=List[i]
		return videos
	#删除html标签
	def removeHtml(self,txt):
		soup = re.compile(r'<[^>]+>',re.S)
		txt =soup.sub('', txt)
		return txt.replace("&nbsp;"," ")