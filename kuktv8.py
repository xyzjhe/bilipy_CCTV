#coding=utf-8
#!/usr/bin/python
import sys
sys.path.append('..') 
from base.spider import Spider
import time
import base64
import re
from urllib import request, parse
import urllib
import urllib.request
import base64

class Spider(Spider):  # 元类 默认的元类 type
	def getName(self):
		return "酷客影院"
	def __init__(self,extend=""):
		print("============{0}============".format(extend))
		pass
	def isVideoFormat(self,url):
		pass
	def manualVideoCheck(self):
		pass
	def homeContent(self,filter):
		result = {}
		cateManual = {
			"电视剧": "dianshiju",
			"电影": "dianying",
			"动漫": "dongmna",
			"综艺":"zongyi",
			"纪录片":"jilupian"
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
		Url='https://www.kuktv8.com/kkys/{0}/page/{1}.html'.format(tid,pg)
		htmlTxt=self.webReadFile(urlStr=Url,header=self.header)
		videos=self.get_list(html=htmlTxt,patternTxt=r'<a class="stui-vodlist__thumb lazyload" href="(?P<url>.+?)" title="(?P<title>.+?)" data-original="(?P<img>.+?)"><span class=".*?"></span><span class=".*?">(?P<renew>.+?)</span></a>')
		listCount=len(videos)
		pagecount=self.get_RegexGetText(Text=htmlTxt,RegexText=r'</li><li><a href=".+?page/(\d+?).html">尾页</a></li>',Index=1)
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
		urlId = aid[1]#URL
		logo = aid[2]#封面
		year=''#年份
		area=''
		actor=''
		director=''
		content=''
		vodItems=[]
		vod_play_from=[]#线路
		vod_play_url=[]#剧集
		html=self.webReadFile(urlStr=urlId,header=self.header)
		line=self.get_RegexGetTextLine(Text=html,RegexText=r'<div class="stui-pannel__head bottom-line active clearfix"><span class="more text-muted pull-right">.*?</span><h3 class="title">(.+?)</h3></div>',Index=1)
		if len(line)<1:
			return  {'list': []}
		circuit=self.get_lineList(Txt=html,mark=r'<ul class="stui-content__playlist column8 clearfix">',after='</ul>')
		vod_play_from=[t for t in line]
		for v in circuit:
			vodItems = self.get_EpisodesList(html=v)
			joinStr = "#".join(vodItems)
			vod_play_url.append(joinStr)

		year=self.get_RegexGetText(Text=html,RegexText=r'更新：(</span>2023-05-24)<',Index=1)
		temporary=self. get_RegexGetTextLine(Text=html,RegexText=r'<a href="/sou/area/.*?.html" target="_blank">(.*?)</a>',Index=1)
		area=" ".join(temporary)
		temporary=self. get_RegexGetTextLine(Text=html,RegexText=r'<a href="/sou/actor/.+?" target="_blank">(.+?)</a>',Index=1)
		actor=" ".join(temporary)
		temporary=self. get_RegexGetTextLine(Text=html,RegexText=r'<a href="/sou/director/.+?" target="_blank">(.+?)</a>',Index=1)
		director=" ".join(temporary)
		content=self. get_RegexGetText(Text=html,RegexText=r'<p class="col-pd">(.*?)</p>',Index=1)
		vod = {
			"vod_id":array[0],
			"vod_name":title,
			"vod_pic":logo,
			"type_name":'',
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
		key=urllib.parse.quote(key)
		url='https://www.kuktv8.com/sou.html?wd={0}&submit='.format(key)
		html=self.webReadFile(urlStr=url,header=self.header)
		videos=self.get_list(html=html,patternTxt=r'<a class=".+?" href="(?P<url>.+?)" title="(?P<title>.+?)" data-original="(?P<img>.+?)"><span class=".+?"></span><span class=".+?">(?P<renew>.+?)</span></a>')
		#print(len(videos))
		result = {
			'list':videos
		}
		return result
	
	def playerContent(self,flag,id,vipFlags):
		result = {}
		headers = {
			'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'
		}
		Url=id
		jx=0
		parse=1
		htmlTxt =self.webReadFile(urlStr=Url,header=self.header)
		m3u8Line=self.get_RegexGetTextLine(Text=htmlTxt,RegexText=r'url":"(\w+?)",',Index=1)
		if len(m3u8Line)>0:
			Url=m3u8Line[0].replace("/","")
			Url=str(base64.b64decode(Url),'utf-8')
			Url=urllib.parse.unquote(Url)
		if Url.find('.m3u8')>1:
			parse=0
			jx=0
		elif Url!='':
			jx=self.ifJx(url=Url)
		else:
			Url=id
		parse=jx
		result["parse"] = parse#1=嗅探,0=播放
		result["playUrl"] = ''
		result["url"] = Url
		result['jx'] = jx#1=VIP解析,0=不解析
		result["header"] = headers	
		return result
	def localProxy(self,param):
		pass
	config = {
		"player": {},
		"filter": {}
		}
	header = {
		"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36",
	    'referer':'https://www.kuktv8.com',
	    'Host':'www.kuktv8.com'
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
	#是否是vip解析
	def ifJx(self,url):
		Isjiexi=0
		RegexTxt=r'(youku.com|v.qq|bilibili|iqiyi.com|tv.cctv|c(c|n)tv|v.pptv)'
		if self.get_RegexGetText(Text=url,RegexText=RegexTxt,Index=1)!='':
			Isjiexi=1
		return Isjiexi
	#搜索取结果
	def get_list_search(self,html):
		jRoot = json.loads(html)
		if jRoot['msg']!='ok':
			return []
		videos = []
		data=jRoot['data']
		if data is None:
			return []
		longData=data['longData']
		if longData is None:
			return []
		jsonList=longData['rows']
		for vod in jsonList:
			url = vod['en_id']
			title =vod['titleTxt']
			img=vod['cover']
			cat_id=vod['cat_id']
			cat_name=vod['cat_name']
			if len(url) == 0:
				continue
			guid="{0}###{1}###{2}###{3}".format(cat_id,title,url,img)
			videos.append({
				"vod_id":guid,
				"vod_name":title,
				"vod_pic":img,
				"vod_remarks":cat_name
			})
		return videos
	#取集数
	def get_EpisodesList(self,html):
		ListRe=re.finditer(r'<li\s*?><a href="(?P<url>.+?)">(?P<title>.+?)</a></li>', html, re.M|re.S)
		videos = []
		for vod in ListRe:
			url = vod.group('url')
			title =vod.group('title')
			if len(url) == 0:
				continue
			videos.append(title+"$"+url)
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
	#取对应线路名
	def get_playlink(self,link):
		linkName={'xigua':'西瓜','douyin':'斗音','leshi':'乐视','youku':'优酷','imgo':'芒果','qiyi':'爱奇艺','qq':'腾讯','huanxi':'搜狐','bilibili1':'B站','cntv':'CCTV','cctv':'CCTV','m1905':'1905电影网'}
		returnName=[]
		for vod in link:
			returnName.append(linkName.get(vod,vod))
		return returnName
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
		for vod in ListRe:
			url = vod.group('url')
			title =vod.group('title')
			img =vod.group('img')
			renew=vod.group('renew')
			if len(url) == 0:
				continue
			if len(img)<5:
				img='https://agit.ai/lanhaidixingren/Tvbox/raw/branch/master/CoverError.png'
			videos.append({
				"vod_id":"{0}###{1}###{2}".format(title,url,img),
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