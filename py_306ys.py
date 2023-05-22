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
			"电视剧": "2",
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
		self.header['referer']='https://www.360kan.com/dianying/list?rank=rankhot&cat=&year=&area=&act=&pageno={0}'.format('2' if pg=='1' else int(pg)-1)
		htmlTxt=self.webReadFile(urlStr=Url,header=self.header)
		videos=self.get_list(html=htmlTxt,types=tid)
		listCount=len(videos)
		result['list'] = videos
		result['page'] = pg
		result['pagecount'] =pg if listCount<34 else int(pg)+1
		result['limit'] = listCount
		result['total'] = 99999
		return result
	def get_list(self,html,types):
		jRoot = json.loads(html)
		if jRoot['errno']=='0':
			return []
		videos = []
		data=jRoot['data']
		print(data)
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
				"vod_remarks":vod['comment']
			})
		return videos
	def detailContent(self,array):
		result = {}
		aid = array[0].split('###')
		tid = aid[0]
		logo = aid[3]
		url = aid[2]
		title = aid[1]
		vodItems=[]
		vod_play_from=['线路',]
		if tid=='play':
			vodItems = [title+"$"+url]
		elif tid=='List':
			id=self.get_RegexGetText(Text=url,RegexText=r'https{0,1}://(tv\.|www\.){0,1}(.+?)\.',Index=2)
			reTxt=''
			for t in self.ReStr:
				if t['name']==id:
					reTxt=t
					break
			if reTxt!='':
				htmlTxt=self.webReadFile(urlStr=url,header=self.header)
				line=self.get_RegexGetTextLine(Text=htmlTxt,RegexText=reTxt['line'],Index=1)
				vod_play_from=[t for t in line]
				circuit=self.get_lineList(Txt=htmlTxt,mark=reTxt['circuit'],after=reTxt['after'])
				#测试到此
				for t in circuit:
					ListRe=re.finditer(reTxt['pattern'], t, re.M|re.S)
					videos = []
					for vod in ListRe:#/vodplay/50548-1-1/
						url = vod.group('url').replace('">','')
						EpisodeTitle =vod.group('title')
						videos.append(EpisodeTitle+"$"+reTxt['url']+url)
					joinStr = "#".join(videos)
					vodItems.append(joinStr)
				#array[0]="{0}###{1}###{2}###{3}".format(tid,title,url,logo)
		elif tid=='weather':
			vodItems = [title+"$"+url]
		else:
			pass
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
	def get_list(self,html):
		patternTxt=r'<a href=\\"(http.+?)\\" title=\\"(.+?)\\" target=\\"_blank\\">(.+?)</a>'
		pattern = re.compile(patternTxt)
		ListRe=pattern.findall(html)
		img ='http://photo.16pic.com/00/78/41/16pic_7841675_b.jpg'
		videos = []
		i=0
		tdi=''
		for vod in ListRe:
			lastVideo = vod[0]
			title =vod[1]
			if title.find('_List')>1:
				tdi='List'
				title=title[0:len(title)-5]
			else:
				tdi='play'
			if len(lastVideo) == 0:
				continue
			videos.append({
				"vod_id":"{0}###{1}###{2}###{3}".format(tdi,title,lastVideo,img),
				"vod_name":title,
				"vod_pic":img,
				"vod_remarks":''
			})
		res = [i for n, i in enumerate(videos) if i not in videos[:n]]
		videos = res
		return videos
	def get_list_B(self,jsonTxt):
		videos=[]
		jRoot = json.loads(jsonTxt)
		if jRoot['code']!=0:
			return videos
		jo = jRoot['data']
		vodList = jo['list']
		rooms=jo['rooms']
		for vod in vodList:
			url =vod['room_id']
			title =vod['title']
			img=vod['keyframe']
			remarks=vod['uname']
			if len(img)<3:
				img='https://www.baidu.com/link?url=w4owbtzM4I-UZp_1mOG3XAfrgl20sGkgnjZDyVglrgGRk9g2S3TpFA0Sh9E0YqsJ&wd=&eqid=f583e14d00056df100000003642e34bd'
			vod_id="{0}###{1}###{2}".format(title,url,img)
			videos.append({
				"vod_id":vod_id,
				"vod_name":title,
				"vod_pic":img,
				"vod_remarks":remarks
			})
		return videos
	def get_m3u8Url_B(self,jsonTxt):
		videos=[]
		jRoot = json.loads(jsonTxt)
		if jRoot['code']!=0:
			return videos
		jo = jRoot['data']
		room_id=jo['room_id']
		playurl=jo['playurl_info']
		playurl=playurl['playurl']
		desc=playurl['g_qn_desc']
		descMass={}
		for x in desc:
			descMass[x['qn']]=x['desc']
		stream=playurl['stream']
		urlM3u8=[]
		for vod in stream:
			formatJson=vod['format']
			if len(formatJson)<1:
				continue
			for x in formatJson:
				codec=x['codec']
				format_name=x['format_name']
				for x1 in codec:
					qn=x1['current_qn']
					url=x1['base_url']
					host=x1['url_info'][0]['host']
					extra=x1['url_info'][0]['extra']
					urlM3u8.append({
						'Url':url,
						'host':host,
						'qn':qn,
						'extra':extra,
						'format_name':format_name
						})
		if len(urlM3u8)>0:
			for x in urlM3u8:
				url=x['host']+x['Url']+x['extra']
				title=descMass.get(x['qn'])+"["+x['format_name'].replace("fmp4","m3u8")+"]"
				videos.append(title+"$"+url)
		if len(videos)<1:
			idTxt='platform=web&quality=4_{0}'.format(room_id)
			ids = idTxt.split("_")
			Url = 'https://api.live.bilibili.com/room/v1/Room/playUrl?cid=%s&%s'%(ids[1],ids[0])
			rsp = self.fetch(Url,headers=self.header)
			htmlTxt = rsp.text
			jRoot = json.loads(htmlTxt)
			if jRoot['code']!=0:
				return videos
			jo = jRoot['data']
			ja = jo['durl']
			quality=jo['quality_description']
			url = ''
			if len(ja) > 0:
				url1 = ja[0]['url']
				title=quality[0]['desc']
				videos.append(title+"$"+url1)
		return videos
	config = {
		"player": {},
		"filter": {}
		}
	header = {
		"Referer": 'http://my.ie.2345.com/onlinefav/web/',
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
		"Host":'my.ie.2345.com',
		'Cookie':'uUiD=35752164629621148571735; name_ie=%2534013%2528023%2522320%2526143%2520154; I=i%3D90475631%26u%3D88890231%26n%3D%25C0%25B6%25BA%25A3%25B5%25D8%25D0%25C7%25C8%25CB%26m%3D0%26t%3D1675499574.1711300%26s%3D6a22a64feb086a03715e47d4cc3e8a29%26v%3D1.1; sData=6392F231FBE75023D053CEFE20A81E6EE43333BF6FF9CD4610BA32AB109E43FD1742EBAAA408F5EB45E7E1A10A40174BC8EE73651C7AD84AC5840AEA48B014F46FE421C992A7799DBF763B0E743AC8716814F0237BC8F8CC62FCF9F8A283040ADD791FBDD3470D699AA43B70F9886350F57021D6DB5E7B8E001ABEFE70C38424; site_str_flag=2; need_modify_name=0; skin=0; theme=0; ggbd=0'
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
