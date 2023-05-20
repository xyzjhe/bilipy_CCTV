#coding=utf-8
#!/usr/bin/python
import sys
sys.path.append('..') 
from base.spider import Spider
import json
import re
from urllib import request, parse
import urllib
import urllib.request

class Spider(Spider):  # 元类 默认的元类 type
	def getName(self):
		return "360影视"
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
			"电视剧": "2",
			"电影": "1",
			"动漫": "4",
			"儿童": "25",
			"综艺":"43"
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
		Url='https://api.web.360kan.com/v1/filter/list?catid={0}&rank=rankhot&cat=&year=&area=&act=&size=35&pageno={1}'.format(tid,pg)
		self.header['referer']='https://www.360kan.com/dianying/list?rank=rankhot&cat=&year=&area=&act=&pageno='+'2' if pg=='1' else pg
		rsp = self.fetch(Url, cookies=self.header)
		htmlTxt=rsp.text
		types=[]
		if tid=='1':
			types=['m',tid]
		videos=self.get_list(html=htmlTxt,types=types)
		listCount=len(videos)
		result['list'] = videos
		result['page'] = pg
		result['pagecount'] = 999 if listCount>34 else pg
		result['limit'] = listCount
		result['total'] = 999999
		return result
	def get_list(self,html,types):
		jRoot = json.loads(html)
		if jRoot['msg']!='ok':
			return []
		videos = []
		jsonList=jRoot['data']['movies']
		for vod in jsonList:
			url = vod['id']
			title =vod['title']
			img='https:'+vod['cdncover']
			#print(title)
			if len(url) == 0:
				continue
			guid="{0}###{1}###{2}###{3}".format(types[1],title,url,img)
			videos.append({
				"vod_id":guid,
				"vod_name":title,
				"vod_pic":img,
				"vod_remarks":vod['comment']
			})
		return videos
	def detailContent(self,array):
		result = {}
		aid = array[0].split('###')
		tid=aid[0]#类型id
		title = aid[1]#片名
		urlId = aid[2]#URL
		logo = aid[3]#封面
		vodItems=[]
		vod_play_from=[]#线路
		vod_play_url=[]#剧集
		year=''#年份
		area=''
		actor=''
		director=''
		content=''
		url='https://api.web.360kan.com/v1/detail?cat={0}&id={1}'.format(tid,urlId)
		self.header['referer']='https://www.360kan.com'
		rsp = self.fetch(url, cookies=self.header)
		html=rsp.text
		if html.find('Success')>0:
			jRoot = json.loads(html)
			data=jRoot['data']
			vod_play_from_id=[t for t in data['playlink_sites']]
			vod_play_from=self.get_playlink(vod_play_from_id)
			title=data['title']
			year=data['pubdate']
			area='/'.join([v for v in data['area']])
			actor='/'.join([v for v in data['actor']])
			director='/'.join([v for v in data['director']])
			content=data['description']
			if 'allepidetail' in data:
				allepidetail=data['allepidetail']
				keyName=list(allepidetail.keys())
				if len(keyName[0])>0:
					vodItems=self.get_EpisodesList(html=allepidetail[keyName[0]])
					joinStr = "#".join(vodItems)
					vod_play_url.append(joinStr)
				if len(vodItems)>0:
					del vod_play_from_id[0]
				for x in vod_play_from_id:
				url='https://api.web.360kan.com/v1/detail?cat={2}&id={0}&site={1}'.format(urlId,x,tid)
				rsp = self.fetch(url, cookies=self.header)
				html=rsp.text
				if html.find('Success')<0:
					continue
				jRoot = json.loads(html)
				data=jRoot['data']
				if 'allepidetail' in data:
					allepidetail=data['allepidetail']
					vodItems=self.get_EpisodesList(html=allepidetail[x])
					joinStr = "#".join(vodItems)
					vod_play_url.append(joinStr)
			elif 'playlinksdetail' in data:
				playlinksdetail=data['playlinksdetail']
				keyName=list(playlinksdetail.keys())
				for l in keyName:
					temporary=playlinksdetail[l]
					url=temporary['default_url']
					vodItems.append(title+"$"+url)
				joinStr = "#".join(vodItems)
				vod_play_url.append(joinStr)
				vod_play_from=self.get_playlink(keyName)
		vod = {
			"vod_id":array[0],
			"vod_name":title,
			"vod_pic":logo,
			"type_name":tid,
			"vod_year":year,
			"vod_area":area,
			"vod_remarks":"",
			"vod_actor":actor,
			"vod_director":director,
			"vod_content":content
		}
		vod['vod_play_from'] =  "$$$".join(vod_play_from)
		vod['vod_play_url'] = "$$$".join(vod_play_url)
		result = {
			'list':[
				vod
			]
		}
		return result
	def get_playlink(self,link):
		linkName={'xigua':'西瓜','douyin':'斗音','leshi':'乐视','youku':'优酷','imgo':'芒果','qiyi':'爱奇艺','qq':'腾讯','huanxi':'搜狐','bilibili1':'B站','cntv':'CCTV','cctv':'CCTV','m1905':'1905电影网'}
		returnName=[]
		for vod in link:
			returnName.append(linkName.get(vod,vod))
		return returnName
	def get_EpisodesList(self,html):
		videos = []
		for vod in html:
				url = vod['url']
				title =vod['playlink_num']
				videos.append(title+"$"+url)
		return videos
	def get_RegexGetTextLine(self,Text,RegexText,Index):
		returnTxt=[]
		pattern = re.compile(RegexText, re.M|re.S)
		ListRe=pattern.findall(Text)
		if len(ListRe)<1:
			return returnTxt
		for value in ListRe:
			returnTxt.append(value)	
		return returnTxt
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
		jx=self.ifJx(urlTxt=id)
		parse=jx
		if self.get_RegexGetText(Text=urlTxt,RegexText=r'(cntv|cctv)',Index=1)!='':
			id=self.get_cctv(id)
			parse=0
			jx=0
		result["parse"] = parse
		result["playUrl"] = ''
		result["url"] = id
		result['jx'] = jx#VIP解析
		result["header"] = headers	
		return result
	def get_cctv(self,id):
		result = {}
		rsp = self.fetch(id)
		htmlTxt=rsp.text
		pattern = re.compile(r'var\sguid\s*=\s*"(.+?)";')
		ListRe=pattern.findall(htmlTxt)
		if ListRe==[]:
			return result
		url = "https://vdn.apps.cntv.cn/api/getHttpVideoInfo.do?pid={0}".format(ListRe[0])
		jo = self.fetch(url,headers=self.header).json()
		link = jo['hls_url'].strip()
		rsp = self.fetch(link,headers=self.header)
		content = rsp.text.strip()
		arr = content.split('\n')
		urlPrefix = self.regStr(link,'(http[s]?://[a-zA-z0-9.]+)/')

		subUrl = arr[-1].split('/')
		subUrl[3] = '1200'
		subUrl[-1] = '1200.m3u8'
		hdUrl = urlPrefix + '/'.join(subUrl)

		url = urlPrefix + arr[-1]

		hdRsp = self.fetch(hdUrl,headers=self.header)
		if hdRsp.status_code == 200:
			url = hdUrl
		return url
	def ifJx(self,urlTxt):
		Isjiexi=1
		RegexTxt=r'(cntv|cctv)'
		if self.get_RegexGetText(Text=urlTxt,RegexText=RegexTxt,Index=1)=='':
			Isjiexi=0
		return Isjiexi
	def get_RegexGetText(self,Text,RegexText,Index):
		returnTxt=""
		Regex=re.search(RegexText, Text, re.M|re.S)
		if Regex is None:
			returnTxt=""
		else:
			returnTxt=Regex.group(Index)
		return returnTxt	
	config = {
		"player": {},
		"filter": {}
		}
	header = {
		"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36",
	    'referer':'https://www.360kan.com/dianying/list?rank=rankhot&cat=&year=&area=&act=&pageno=',
	    'Host':'api.web.360kan.com'
	}
	def localProxy(self,param):
		pass