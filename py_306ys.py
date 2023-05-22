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
			"电视剧1": "2",
			"电影": "1",
			"动漫": "4",
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
		result = {
			'list':[]
		}
		return result
	def categoryContent(self,tid,pg,filter,extend):
		result = {}
		videos=[]
		Url='https://api.web.360kan.com/v1/filter/list?catid={0}&rank=rankhot&cat=&year=&area=&act=&size=35&pageno={1}'.format(tid,pg)
		self.header['referer']='https://www.360kan.com/dianying/list?rank=rankhot&cat=&year=&area=&act=&pageno={0}'.format('2' if pg=='1' else 9999)
		htmlTxt=self.webReadFile(urlStr=Url,header=self.header)
		videos=self.get_list(html=htmlTxt,types=tid)
		listCount=len(videos)
		result['list'] = videos
		result['page'] = pg
		result['pagecount'] =999999
		result['limit'] = listCount
		result['total'] = 99999
		return result
	def get_list(self,html,types):
		jRoot = json.loads(html)
		if jRoot['errno']=='0':
			return []
		videos = []
		data=jRoot['data']
		if data is None:
			return []
		jsonList=data['movies']
		for vod in jsonList:
			url = vod['id']
			title =vod['title']
			img='https:'+vod['cdncover']
			if len(url) == 0:
				continue
			guid="{0}###{1}###{2}###{3}".format(types,title,url,img)
			videos.append({
				"vod_id":guid,
				"vod_name":title,
				"vod_pic":img,
				"vod_remarks":''
			})
		return videos
		def detailContent(self,array):		result = {}
		aid = array[0].split('###')
		tid=aid[0]#类型id
		title = aid[1]#片名
		urlId = aid[2]#URL
		logo = aid[3]#封面
		year=''#年份
		area=''
		actor=''
		director=''
		content=''
		vodItems=[]
		vod_play_from=[]#线路
		vod_play_url=[]#剧集
		url='https://api.web.360kan.com/v1/detail?cat={0}&id={1}'.format(tid,urlId)
		self.header['referer']='https://www.360kan.com'
		html=self.webReadFile(urlStr=url,header=self.header)

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
				upinfo=int(data['upinfo'])
				Stepping=49 if upinfo>49 else upinfo-1
				for x in vod_play_from_id:
					starting=1
					end=starting+Stepping
					vodItems=[]

					while len(vodItems)<upinfo:

						url='https://api.web.360kan.com/v1/detail?cat={0}&id={1}&start={2}&end={3}&site={4}'.format(tid,urlId,starting,end,x)
						
						html=self.webReadFile(urlStr=url,header=self.header)
						
						if html.find('Success')<0:
							break
						jRoot = json.loads(html)
						data=jRoot['data']
						if 'allepidetail' in data:
							allepidetail=data['allepidetail']
							temporary=self.get_EpisodesList(html=allepidetail[x])
							for vod in temporary:
								vodItems.append(vod)
						joinStr = "#".join(vodItems)
						vod_play_url.append(joinStr)
						
						if len(temporary)<1:
							break
						starting=end+1
						end+=Stepping
						if end>upinfo:
							end=upinfo						
						#time.sleep(1)
					#print(str(len(vodItems))+x)
			elif 'playlinksdetail' in data:
				playlinksdetail=data['playlinksdetail']
				keyName=[]#list(playlinksdetail.keys())
				for l in keyName:
					temporary=playlinksdetail[l]
					url=temporary['default_url']
					vodItems.append(title+"$"+url)
				joinStr = "#".join(vodItems)
				vod_play_url.append(joinStr)
				vod_play_from=self.get_playlink(keyName)
		
		vod = {
			"vod_id":array,
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
		parse=1
		if self.get_RegexGetText(Text=id,RegexText=r'(\.mp4)',Index=1)!='':
			parse=0
		result["parse"] = parse
		result["playUrl"] = ''
		result["url"] = id
		result['jx'] = jx#VIP解析
		result["header"] = headers	
		return result
	def ifJx(self,urlTxt):
		Isjiexi=0
		RegexTxt=r'(youku.com|v.qq|bilibili|iqiyi.com)'
		if self.get_RegexGetText(Text=urlTxt,RegexText=RegexTxt,Index=1)!='':
			Isjiexi=1
		return Isjiexi
	def get_RegexGetText(self,Text,RegexText,Index):
		returnTxt=""
		Regex=re.search(RegexText, Text, re.M|re.S)
		if Regex is None:
			returnTxt=""
		else:
			returnTxt=Regex.group(Index)
		return returnTxt	
	def webReadFile(self,urlStr,header):
		req = urllib.request.Request(url=urlStr,headers=header)#,headers=header
		html = urllib.request.urlopen(req).read().decode('utf-8')
		#print(Host)
		return html
	config = {
		"player": {},
		"filter": {}
		}
	header = {
		"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36",
	    'referer':'https://www.360kan.com/dianying/list?rank=rankhot&cat=&year=&area=&act=&pageno=2',
	    'Host':'api.web.360kan.com'
	}
	def webReadFile(self,urlStr,header):
		req = urllib.request.Request(url=urlStr,headers=header)#,headers=header
		html = urllib.request.urlopen(req).read().decode('utf-8')
		#print(Host)
		return html
	vod={
		'name':'ikan6',
		'line':'<div class="module-tab-item.+?" data-dropdown-value="(.+?)"><span>.+?</span>.*?</div>',
		'circuit':'module-play-list-base">',
		'after':'</div>',
		'pattern':'<a\sclass="module-play-list-link"\shref="(?P<url>.+?)"\s*title=".+?"><span>(?P<title>.+?)</span></a>',
		'url':'https://ikan6.vip'
	}
	ReStr=[]
	ReStr.append(vod)
	vod={
		'name':'ktkkt2',
		'line':'<h3 class="title"><strong>(.+?)</strong><span class="text-muted pull-mid">',
		'circuit':'<div id="video_list_',
		'after':'</div>',
		'pattern':r"<li><a title=\'.+?\'\shref=\'(?P<url>.+?)\'"+'\starget="_self">(?P<title>.+?)</a></li>',
		'url':'https://www.ktkkt2.com'
	}
	ReStr.append(vod)
	vod={
		'name':'cctv',
		'line':'>(剧集列表)</li>',
		'circuit':'//相关报导',
		'after':' </script>',
		'pattern':r"'title':'(?P<title>.+?)',\r\n\s*'img':'.*?',\r\n\s*'brief':'.*?',\r\n\s*'url':'(?P<url>.+?)'",
		'url':''
	}
	ReStr.append(vod)
	def localProxy(self,param):
		return [200, "video/MP2T", action, ""]
