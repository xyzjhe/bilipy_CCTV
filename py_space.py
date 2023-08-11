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
from xml.etree.ElementTree import fromstring, ElementTree as et

class Spider(Spider):  # 元类 默认的元类 type
	def getName(self):
		return "蓝海地星人的空间"
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
			"个人收藏": "Collection",
			"天气预报":"weather"
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
		if pg!='1':
			return result
		if tid=='Collection':
			Url='http://my.ie.2345.com/onlinefav/web/getAllData?action=getData&id=21492773&s=&d=Fri%20Mar%2003%202023%2008:45:08%20GMT+0800%20(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)'
			videos = self.custom_list(html=self.custom_webReadFile(urlStr=Url,header=self.header))
		elif  tid=='weather':
			Url = 'http://www.weather.com.cn/pubm/video_lianbo_2021.htm'
			htmlTxt=self.custom_webReadFile(urlStr=Url)
			if len(htmlTxt)>13:
				htmlTxt=htmlTxt[11:htmlTxt.rfind(')')]
				videos = self.get_list_weather(html=htmlTxt)
		else:
			pass
		result['list'] = videos
		result['page'] = pg
		result['pagecount'] = 1
		result['limit'] = 90
		result['total'] = 999999
		return result
	rule={}#规则
	def detailContent(self,array):
		result = {}
		aid = array[0].split('###')
		tid = aid[0]
		logo = aid[3]
		url = aid[2]
		title = aid[1]
		vodItems=[]
		vod_play_from=['线路',]
		vod_play_url=[]
		if tid=='weather':
			vodItems = [title+"$"+url]
			joinStr = "#".join(vodItems)
			vod_play_url.append(joinStr)
		elif tid=='play':
			vodItems = [title+"$"+url]
			joinStr = "#".join(vodItems)
			vod_play_url.append(joinStr)
		elif tid=='List':
			ruleName=self.custom_RegexGetText(Text=url,RegexText='https*://(w{3}\.){0,1}(.*?)(\.{0,1}/|$)',Index=2)
			self.rule=self.custom_getRule(ruleName=ruleName)
			if self.rule=={}:
				return result
			htmlTxt=self.custom_webReadFile(urlStr=url)
			line=self.custom_txtLineList(Text=htmlTxt,RegexText=self.rule['lineExpression'],Index=2)
			if len(line)<1:
				return result
			vod_play_from=[t.replace('&nbsp;','') for t in line]
			circuit=self.custom_lineList(Txt=htmlTxt,mark=self.rule['circuitFront'],after=self.rule['circuitAfter'])
			for v in circuit:
				vodItems = self.custom_EpisodesList(html=v,RegexText=self.rule['EpisodeExpression'])
				joinStr = "#".join(vodItems)
				vod_play_url.append(joinStr)
		else:
			pass
		if self.rule!={}:
			if len(self.rule['coverExpression'])>3:
				temporary=self.custom_RegexGetText(Text=htmlTxt,RegexText=self.rule['coverExpression'],Index=1)
				if temporary!="":
					logo=temporary
			if len(self.rule['contentExpression'])>3:
				content=self.custom_RegexGetText(Text=htmlTxt,RegexText=self.rule['contentExpression'],Index=1)
			array[0]='List###{0}###{1}###{2}'.format(title,url,logo)
		else:
			content=''
			area=''
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
			"vod_content":str(content)
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
		jx=self.custom_ifJx(urlTxt=id)
		if jx==1:
			parse=1
		if self.custom_RegexGetText(Text=id,RegexText=r'(\.mp4)',Index=1)!='':
			parse=0
		if id.find('www.huya.com')>0:
			headers= {
			'User-Agent':'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 SE 2.X MetaSr 1.0'
		}
		result["parse"] = 0
		result["playUrl"] =''
		result["url"] = id
		result['jx'] = jx#VIP解析
		result["header"] = headers	
		return result

	config = {
		"player": {},
		"filter": {}
		}
	header = {
		"Referer": 'http://my.ie.2345.com/onlinefav/web/',
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
		"Host":'my.ie.2345.com',
		'Cookie':'uUiD=35752164629621148571735; name_ie=%2534013%2528023%2522320%2526143%2520154; I=i%3D90475631%26u%3D88890231%26n%3D%25C0%25B6%25BA%25A3%25B5%25D8%25D0%25C7%25C8%25CB%26m%3D0%26t%3D1687503738.46911300%26s%3Df8147ba8a21ae867edc8960a27b871a8%26v%3D1.1; sData=6392F231FBE75023D053CEFE20A81E6EE43333BF6FF9CD4610BA32AB109E43FD1742EBAAA408F5EB45E7E1A10A40174B3802B9DA7D3442844AF0093D9E87A22744FA8126F42C9C2BC1B8F88566586F8556548AEDF5FA99D898E168F5ECC2CF17B9FB0D45E3ADFF35BDDF77EF6BEBCDBF059ABFE942766D87F75CBBA205FD695F; site_str_flag=2; need_modify_name=0; skin=0; theme=0; ggbd=0'
	}
	def localProxy(self,param):
		return [200, "video/MP2T", action, ""]
#-----------------------------------------------自定义函数-----------------------------------------------
		#正则取文本
	def custom_RegexGetText(self,Text,RegexText,Index):
		returnTxt=""
		Regex=re.search(RegexText, Text, re.M|re.S)
		if Regex is None:
			returnTxt=""
		else:
			returnTxt=Regex.group(Index)
		return returnTxt	
	#分类取结果
	def custom_list(self,html):
		patternTxt=r'<a href=\\"(http.+?)\\" title=\\"(.+?)\\" target=\\"_blank\\">(.+?)</a>'
		pattern = re.compile(patternTxt)
		ListRe=pattern.findall(html)
		img ='http://photo.16pic.com/00/78/41/16pic_7841675_b.jpg'
		videos = []
		i=0
		for vod in ListRe:
			lastVideo = vod[0]
			title =vod[1]
			if title.find('L-')==0:
				tid='List'
				title=title[2:]
			else:
				tid='play'
			if len(lastVideo) == 0:
				continue
			videos.append({
				"vod_id":"{0}###{1}###{2}###{3}".format(tid,title,lastVideo,img),
				"vod_name":title,
				"vod_pic":img,
				"vod_remarks":''
			})
		res = [i for n, i in enumerate(videos) if i not in videos[:n]]
		videos = res
		return videos
		#访问网页
	def custom_webReadFile(self,urlStr,header=None,codeName='utf-8'):
		html=''
		if header==None:
			header={
				"Referer":urlStr,
				'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
				"Host":self.custom_RegexGetText(Text=urlStr,RegexText='https*://(.*?)(/|$)',Index=1)
			}
		req=urllib.request.Request(url=urlStr,headers=header)#,headers=header
		with  urllib.request.urlopen(req)  as response:
			html = response.read().decode(codeName)
		return html
	#判断是否要调用vip解析
	def custom_ifJx(self,urlTxt):
		Isjiexi=0
		RegexTxt=r'(youku.com|v.qq|bilibili|iqiyi.com)'
		if self.custom_RegexGetText(Text=urlTxt,RegexText=RegexTxt,Index=1)!='':
			Isjiexi=1
		return Isjiexi
	#取集数
	def custom_EpisodesList(self,html,RegexText):
		ListRe=re.finditer(RegexText, html, re.M|re.S)
		videos = []
		head=self.rule['UrlFront']
		for vod in ListRe:
			url = vod.group('url')
			title =vod.group('title')
			if len(url) == 0:
				continue
			videos.append(title+"$"+head+url)
		return videos
	#取剧集区
	def custom_lineList(self,Txt,mark,after):
		circuit=[]
		origin=Txt.find(mark)
		while origin>8:
			end=Txt.find(after,origin)
			circuit.append(Txt[origin:end])
			origin=Txt.find(mark,end)
		return circuit	
	#正则取文本,返回数组	
	def custom_txtLineList(self,Text,RegexText,Index):
		returnTxt=[]
		pattern = re.compile(RegexText, re.M|re.S)
		ListRe=pattern.findall(Text)
		if len(ListRe)<1:
			return returnTxt
		for value in ListRe:
			returnTxt.append(value)	
		return returnTxt
	#天气
	def get_list_weather(self,html):
		jRoot = json.loads(html)
		if jRoot['message']!='success':
			return []
		videos = []
		jsonList=jRoot['data']
		img ="http://i.i8tq.com/video/202010191603094992701_83.jpg"
		for vod in jsonList:
			url = vod['url']
			title =vod['title']
			if len(url) == 0:
				continue
			guid="{0}###{1}###{2}###{3}".format('weather',title,url,img)
			print(guid)
			videos.append({
				"vod_id":guid,
				"vod_name":title,
				"vod_pic":img,
				"vod_remarks":vod['updateTime']
			})
		return videos
	# 取自定义规则
	def custom_getRule(self,ruleName):
		xmlTxt=self.custom_webReadFile(urlStr="https://agit.ai/lanhaidixingren/Tvbox/raw/branch/master/custom.xml")
		# xmlTxt=self.readFile(filePath='custom.xml')
		ruleList={}
		tree = et(fromstring(xmlTxt))
		root = tree.getroot()
		if ruleName=='':
			return ruleList
		for vod in root:
			if vod.attrib['Name']!=ruleName:
				continue
			for v in vod:
				ruleList[v.tag]=str(base64.b64decode(v.attrib['value']),'utf-8')
		return ruleList