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
			"电视剧": "电视剧",
			"动画片": "动画片",
			"纪录片": "纪录片",
			"特别节目": "特别节目",
			"节目大全":"节目大全",
			"直播":"直播"
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
		month = ""#月
		year = ""#年
		area=''#地区
		channel=''#频道
		datafl=''#类型
		letter=''#字母
		if tid=='动画片':
			id=urllib.parse.quote(tid)
			if 'datadq-area' in extend.keys():
				area=urllib.parse.quote(extend['datadq-area'])
			if 'dataszm-letter' in extend.keys():
				letter=extend['dataszm-letter']
			if 'datafl-sc' in extend.keys():
				datafl=urllib.parse.quote(extend['datafl-sc'])
			url='https://api.cntv.cn/list/getVideoAlbumList?channelid=CHAL1460955899450127&area={0}&sc={4}&fc={1}&letter={2}&p={3}&n=24&serviceId=tvcctv&topv=1&t=json'.format(area,id,letter,pg,datafl)
		elif tid=='纪录片':
			id=urllib.parse.quote(tid)
			if 'datapd-channel' in extend.keys():
				channel=urllib.parse.quote(extend['datapd-channel'])
			if 'datafl-sc' in extend.keys():
				datafl=urllib.parse.quote(extend['datafl-sc'])
			if 'datanf-year' in extend.keys():
				year=extend['datanf-year']
			if 'dataszm-letter' in extend.keys():
				letter=extend['dataszm-letter']
			url='https://api.cntv.cn/list/getVideoAlbumList?channelid=CHAL1460955924871139&fc={0}&channel={1}&sc={2}&year={3}&letter={4}&p={5}&n=24&serviceId=tvcctv&topv=1&t=json'.format(id,channel,datafl,year,letter,pg)
		elif tid=='电视剧':
			id=urllib.parse.quote(tid)
			if 'datafl-sc' in extend.keys():
				datafl=urllib.parse.quote(extend['datafl-sc'])
			if 'datanf-year' in extend.keys():
				year=extend['datanf-year']
			if 'dataszm-letter' in extend.keys():
				letter=extend['dataszm-letter']
			url='https://api.cntv.cn/list/getVideoAlbumList?channelid=CHAL1460955853485115&area={0}&sc={1}&fc={2}&year={3}&letter={4}&p={5}&n=24&serviceId=tvcctv&topv=1&t=json'.format(area,datafl,id,year,letter,pg)
		elif tid=='特别节目':
			id=urllib.parse.quote(tid)
			if 'datapd-channel' in extend.keys():
				channel=urllib.parse.quote(extend['datapd-channel'])
			if 'datafl-sc' in extend.keys():
				datafl=urllib.parse.quote(extend['datafl-sc'])
			if 'dataszm-letter' in extend.keys():
				letter=extend['dataszm-letter']
			url='https://api.cntv.cn/list/getVideoAlbumList?channelid=CHAL1460955953877151&channel={0}&sc={1}&fc={2}&bigday=&letter={3}&p={4}&n=24&serviceId=tvcctv&topv=1&t=json'.format(channel,datafl,id,letter,pg)
		elif tid=='节目大全':
			month = ""
			year = ""
			if 'month' in extend.keys():
				month = extend['month']
			if 'year' in extend.keys():
				year = extend['year']
			if year == '':
				month = ''
			prefix = year + month
			extend['p'] = pg
			filterMap = {
				"fl":"",
				"fc":"",
				"cid":"",
				"p":"1"
			}
			suffix = ""
			for key in filterMap.keys():
				if key in extend.keys():
					filterMap[key] = extend[key]
				suffix = suffix + '&' + key + '=' + filterMap[key]
			url = 'https://api.cntv.cn/lanmu/columnSearch?{0}&n=20&serviceId=tvcctv&t=json'.format(suffix)		
		else:
			url = 'https://tv.cctv.com/epg/index.shtml'

		videos=[]
		htmlText =self.webReadFile(urlStr=url,header=self.header)
		if tid=='节目大全':
			index=htmlText.rfind(');')
			if index>-1:
				htmlText=htmlText[3:index]
				videos =self.get_list1(html=htmlText,tid=tid)
		elif tid=='直播':
			videos =self.get_list_live(html=htmlText,tid=tid)
		else:
			videos =self.get_list(html=htmlText,tid=tid)
		#print(videos)
		
		result['list'] = videos
		result['page'] = pg
		result['pagecount'] = 9999
		result['limit'] = 90
		result['total'] = 999999
		return result
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
		"filter": {
		"电视剧":[
		{"key":"datafl-sc","name":"类型","value":[{"n":"全部","v":""},{"n":"谍战","v":"谍战"},{"n":"悬疑","v":"悬疑"},{"n":"刑侦","v":"刑侦"},{"n":"历史","v":"历史"},{"n":"古装","v":"古装"},{"n":"武侠","v":"武侠"},{"n":"军旅","v":"军旅"},{"n":"战争","v":"战争"},{"n":"喜剧","v":"喜剧"},{"n":"青春","v":"青春"},{"n":"言情","v":"言情"},{"n":"偶像","v":"偶像"},{"n":"家庭","v":"家庭"},{"n":"年代","v":"年代"},{"n":"革命","v":"革命"},{"n":"农村","v":"农村"},{"n":"都市","v":"都市"},{"n":"其他","v":"其他"}]},
		{"key":"datadq-area","name":"地区","value":[{"n":"全部","v":""},{"n":"中国大陆","v":"中国大陆"},{"n":"中国香港","v":"香港"},{"n":"美国","v":"美国"},{"n":"欧洲","v":"欧洲"},{"n":"泰国","v":"泰国"}]},
		{"key":"datanf-year","name":"年份","value":[{"n":"全部","v":""},{"n":"2023","v":"2023"},{"n":"2022","v":"2022"},{"n":"2021","v":"2021"},{"n":"2020","v":"2020"},{"n":"2019","v":"2019"},{"n":"2018","v":"2018"},{"n":"2017","v":"2017"},{"n":"2016","v":"2016"},{"n":"2015","v":"2015"},{"n":"2014","v":"2014"},{"n":"2013","v":"2013"},{"n":"2012","v":"2012"},{"n":"2011","v":"2011"},{"n":"2010","v":"2010"},{"n":"2009","v":"2009"},{"n":"2008","v":"2008"},{"n":"2007","v":"2007"},{"n":"2006","v":"2006"},{"n":"2005","v":"2005"},{"n":"2004","v":"2004"},{"n":"2003","v":"2003"},{"n":"2002","v":"2002"},{"n":"2001","v":"2001"},{"n":"2000","v":"2000"},{"n":"1999","v":"1999"},{"n":"1998","v":"1998"},{"n":"1997","v":"1997"}]},
		{"key":"dataszm-letter","name":"字母","value":[{"n":"全部","v":""},{"n":"A","v":"A"},{"n":"C","v":"C"},{"n":"E","v":"E"},{"n":"F","v":"F"},{"n":"G","v":"G"},{"n":"H","v":"H"},{"n":"I","v":"I"},{"n":"J","v":"J"},{"n":"K","v":"K"},{"n":"L","v":"L"},{"n":"M","v":"M"},{"n":"N","v":"N"},{"n":"O","v":"O"},{"n":"P","v":"P"},{"n":"Q","v":"Q"},{"n":"R","v":"R"},{"n":"S","v":"S"},{"n":"T","v":"T"},{"n":"U","v":"U"},{"n":"V","v":"V"},{"n":"W","v":"W"},{"n":"X","v":"X"},{"n":"Y","v":"Y"},{"n":"Z","v":"Z"},{"n":"0-9","v":"0-9"}]}
		],
		"动画片":[
		{"key":"datafl-sc","name":"类型","value":[{"n":"全部","v":""},{"n":"亲子","v":"亲子"},{"n":"搞笑","v":"搞笑"},{"n":"冒险","v":"冒险"},{"n":"动作","v":"动作"},{"n":"宠物","v":"宠物"},{"n":"体育","v":"体育"},{"n":"益智","v":"益智"},{"n":"历史","v":"历史"},{"n":"教育","v":"教育"},{"n":"校园","v":"校园"},{"n":"言情","v":"言情"},{"n":"武侠","v":"武侠"},{"n":"经典","v":"经典"},{"n":"未来","v":"未来"},{"n":"古代","v":"古代"},{"n":"神话","v":"神话"},{"n":"真人","v":"真人"},{"n":"励志","v":"励志"},{"n":"热血","v":"热血"},{"n":"奇幻","v":"奇幻"},{"n":"童话","v":"童话"},{"n":"剧情","v":"剧情"},{"n":"夺宝","v":"夺宝"},{"n":"其他","v":"其他"}]},
		{"key":"datadq-area","name":"地区","value":[{"n":"全部","v":""},{"n":"中国大陆","v":"中国大陆"},{"n":"美国","v":"美国"},{"n":"欧洲","v":"欧洲"}]},
		{"key":"dataszm-letter","name":"字母","value":[{"n":"全部","v":""},{"n":"A","v":"A"},{"n":"C","v":"C"},{"n":"E","v":"E"},{"n":"F","v":"F"},{"n":"G","v":"G"},{"n":"H","v":"H"},{"n":"I","v":"I"},{"n":"J","v":"J"},{"n":"K","v":"K"},{"n":"L","v":"L"},{"n":"M","v":"M"},{"n":"N","v":"N"},{"n":"O","v":"O"},{"n":"P","v":"P"},{"n":"Q","v":"Q"},{"n":"R","v":"R"},{"n":"S","v":"S"},{"n":"T","v":"T"},{"n":"U","v":"U"},{"n":"V","v":"V"},{"n":"W","v":"W"},{"n":"X","v":"X"},{"n":"Y","v":"Y"},{"n":"Z","v":"Z"},{"n":"0-9","v":"0-9"}]}
		],
		"纪录片":[
		{"key":"datapd-channel","name":"频道","value":[{"n":"全部","v":""},{"n":"CCTV{1 综合","v":"CCTV{1 综合"},{"n":"CCTV{2 财经","v":"CCTV{2 财经"},{"n":"CCTV{3 综艺","v":"CCTV{3 综艺"},{"n":"CCTV{4 中文国际","v":"CCTV{4 中文国际"},{"n":"CCTV{5 体育","v":"CCTV{5 体育"},{"n":"CCTV{6 电影","v":"CCTV{6 电影"},{"n":"CCTV{7 国防军事","v":"CCTV{7 国防军事"},{"n":"CCTV{8 电视剧","v":"CCTV{8 电视剧"},{"n":"CCTV{9 纪录","v":"CCTV{9 纪录"},{"n":"CCTV{10 科教","v":"CCTV{10 科教"},{"n":"CCTV{11 戏曲","v":"CCTV{11 戏曲"},{"n":"CCTV{12 社会与法","v":"CCTV{12 社会与法"},{"n":"CCTV{13 新闻","v":"CCTV{13 新闻"},{"n":"CCTV{14 少儿","v":"CCTV{14 少儿"},{"n":"CCTV{15 音乐","v":"CCTV{15 音乐"},{"n":"CCTV{17 农业农村","v":"CCTV{17 农业农村"}]},
		{"key":"datafl-sc","name":"类型","value":[{"n":"全部","v":""},{"n":"人文历史","v":"人文历史"},{"n":"人物","v":"人物"},{"n":"军事","v":"军事"},{"n":"探索","v":"探索"},{"n":"社会","v":"社会"},{"n":"时政","v":"时政"},{"n":"经济","v":"经济"},{"n":"科技","v":"科技"}]},
		{"key":"datanf-year","name":"年份","value":[{"n":"全部","v":""},{"n":"2023","v":"2023"},{"n":"2022","v":"2022"},{"n":"2021","v":"2021"},{"n":"2020","v":"2020"},{"n":"2019","v":"2019"},{"n":"2018","v":"2018"},{"n":"2017","v":"2017"},{"n":"2016","v":"2016"},{"n":"2015","v":"2015"},{"n":"2014","v":"2014"},{"n":"2013","v":"2013"},{"n":"2012","v":"2012"},{"n":"2011","v":"2011"},{"n":"2010","v":"2010"},{"n":"2009","v":"2009"},{"n":"2008","v":"2008"}]},
		{"key":"dataszm-letter","name":"字母","value":[{"n":"全部","v":""},{"n":"A","v":"A"},{"n":"C","v":"C"},{"n":"E","v":"E"},{"n":"F","v":"F"},{"n":"G","v":"G"},{"n":"H","v":"H"},{"n":"I","v":"I"},{"n":"J","v":"J"},{"n":"K","v":"K"},{"n":"L","v":"L"},{"n":"M","v":"M"},{"n":"N","v":"N"},{"n":"O","v":"O"},{"n":"P","v":"P"},{"n":"Q","v":"Q"},{"n":"R","v":"R"},{"n":"S","v":"S"},{"n":"T","v":"T"},{"n":"U","v":"U"},{"n":"V","v":"V"},{"n":"W","v":"W"},{"n":"X","v":"X"},{"n":"Y","v":"Y"},{"n":"Z","v":"Z"},{"n":"0-9","v":"0-9"}]}
		],
		"特别节目":[
		{"key":"datapd-channel","name":"频道","value":[{"n":"全部","v":""},{"n":"CCTV{1 综合","v":"CCTV{1 综合"},{"n":"CCTV{2 财经","v":"CCTV{2 财经"},{"n":"CCTV{3 综艺","v":"CCTV{3 综艺"},{"n":"CCTV{4 中文国际","v":"CCTV{4 中文国际"},{"n":"CCTV{5 体育","v":"CCTV{5 体育"},{"n":"CCTV{6 电影","v":"CCTV{6 电影"},{"n":"CCTV{7 国防军事","v":"CCTV{7 国防军事"},{"n":"CCTV{8 电视剧","v":"CCTV{8 电视剧"},{"n":"CCTV{9 纪录","v":"CCTV{9 纪录"},{"n":"CCTV{10 科教","v":"CCTV{10 科教"},{"n":"CCTV{11 戏曲","v":"CCTV{11 戏曲"},{"n":"CCTV{12 社会与法","v":"CCTV{12 社会与法"},{"n":"CCTV{13 新闻","v":"CCTV{13 新闻"},{"n":"CCTV{14 少儿","v":"CCTV{14 少儿"},{"n":"CCTV{15 音乐","v":"CCTV{15 音乐"},{"n":"CCTV{17 农业农村","v":"CCTV{17 农业农村"}]},
		{"key":"datafl-sc","name":"类型","value":[{"n":"全部","v":""},{"n":"全部","v":"全部"},{"n":"新闻","v":"新闻"},{"n":"经济","v":"经济"},{"n":"综艺","v":"综艺"},{"n":"体育","v":"体育"},{"n":"军事","v":"军事"},{"n":"影视","v":"影视"},{"n":"科教","v":"科教"},{"n":"戏曲","v":"戏曲"},{"n":"青少","v":"青少"},{"n":"音乐","v":"音乐"},{"n":"社会","v":"社会"},{"n":"公益","v":"公益"},{"n":"其他","v":"其他"}]},
		{"key":"dataszm-letter","name":"字母","value":[{"n":"全部","v":""},{"n":"A","v":"A"},{"n":"C","v":"C"},{"n":"E","v":"E"},{"n":"F","v":"F"},{"n":"G","v":"G"},{"n":"H","v":"H"},{"n":"I","v":"I"},{"n":"J","v":"J"},{"n":"K","v":"K"},{"n":"L","v":"L"},{"n":"M","v":"M"},{"n":"N","v":"N"},{"n":"O","v":"O"},{"n":"P","v":"P"},{"n":"Q","v":"Q"},{"n":"R","v":"R"},{"n":"S","v":"S"},{"n":"T","v":"T"},{"n":"U","v":"U"},{"n":"V","v":"V"},{"n":"W","v":"W"},{"n":"X","v":"X"},{"n":"Y","v":"Y"},{"n":"Z","v":"Z"},{"n":"0-9","v":"0-9"}]}
		],
		"节目大全":[{"key":"cid","name":"频道","value":[{"n":"全部","v":""},{"n":"CCTV-1综合","v":"EPGC1386744804340101"},{"n":"CCTV-2财经","v":"EPGC1386744804340102"},{"n":"CCTV-3综艺","v":"EPGC1386744804340103"},{"n":"CCTV-4中文国际","v":"EPGC1386744804340104"},{"n":"CCTV-5体育","v":"EPGC1386744804340107"},{"n":"CCTV-6电影","v":"EPGC1386744804340108"},{"n":"CCTV-7国防军事","v":"EPGC1386744804340109"},{"n":"CCTV-8电视剧","v":"EPGC1386744804340110"},{"n":"CCTV-9纪录","v":"EPGC1386744804340112"},{"n":"CCTV-10科教","v":"EPGC1386744804340113"},{"n":"CCTV-11戏曲","v":"EPGC1386744804340114"},{"n":"CCTV-12社会与法","v":"EPGC1386744804340115"},{"n":"CCTV-13新闻","v":"EPGC1386744804340116"},{"n":"CCTV-14少儿","v":"EPGC1386744804340117"},{"n":"CCTV-15音乐","v":"EPGC1386744804340118"},{"n":"CCTV-16奥林匹克","v":"EPGC1634630207058998"},{"n":"CCTV-17农业农村","v":"EPGC1563932742616872"},{"n":"CCTV-5+体育赛事","v":"EPGC1468294755566101"}]},{"key":"fc","name":"分类","value":[{"n":"全部","v":""},{"n":"新闻","v":"新闻"},{"n":"体育","v":"体育"},{"n":"综艺","v":"综艺"},{"n":"健康","v":"健康"},{"n":"生活","v":"生活"},{"n":"科教","v":"科教"},{"n":"经济","v":"经济"},{"n":"农业","v":"农业"},{"n":"法治","v":"法治"},{"n":"军事","v":"军事"},{"n":"少儿","v":"少儿"},{"n":"动画","v":"动画"},{"n":"纪实","v":"纪实"},{"n":"戏曲","v":"戏曲"},{"n":"音乐","v":"音乐"},{"n":"影视","v":"影视"}]},{"key":"fl","name":"字母","value":[{"n":"全部","v":""},{"n":"A","v":"A"},{"n":"B","v":"B"},{"n":"C","v":"C"},{"n":"D","v":"D"},{"n":"E","v":"E"},{"n":"F","v":"F"},{"n":"G","v":"G"},{"n":"H","v":"H"},{"n":"I","v":"I"},{"n":"J","v":"J"},{"n":"K","v":"K"},{"n":"L","v":"L"},{"n":"M","v":"M"},{"n":"N","v":"N"},{"n":"O","v":"O"},{"n":"P","v":"P"},{"n":"Q","v":"Q"},{"n":"R","v":"R"},{"n":"S","v":"S"},{"n":"T","v":"T"},{"n":"U","v":"U"},{"n":"V","v":"V"},{"n":"W","v":"W"},{"n":"X","v":"X"},{"n":"Y","v":"Y"},{"n":"Z","v":"Z"}]},{"key":"year","name":"年份","value":[{"n":"全部","v":""},{"n":"2022","v":"2022"},{"n":"2021","v":"2021"},{"n":"2020","v":"2020"},{"n":"2019","v":"2019"},{"n":"2018","v":"2018"},{"n":"2017","v":"2017"},{"n":"2016","v":"2016"},{"n":"2015","v":"2015"},{"n":"2014","v":"2014"},{"n":"2013","v":"2013"},{"n":"2012","v":"2012"},{"n":"2011","v":"2011"},{"n":"2010","v":"2010"},{"n":"2009","v":"2009"},{"n":"2008","v":"2008"},{"n":"2007","v":"2007"},{"n":"2006","v":"2006"},{"n":"2005","v":"2005"},{"n":"2004","v":"2004"},{"n":"2003","v":"2003"},{"n":"2002","v":"2002"},{"n":"2001","v":"2001"},{"n":"2000","v":"2000"}]},{"key":"month","name":"月份","value":[{"n":"全部","v":""},{"n":"12","v":"12"},{"n":"11","v":"11"},{"n":"10","v":"10"},{"n":"09","v":"09"},{"n":"08","v":"08"},{"n":"07","v":"07"},{"n":"06","v":"06"},{"n":"05","v":"05"},{"n":"04","v":"04"},{"n":"03","v":"03"},{"n":"02","v":"02"},{"n":"01","v":"01"}]}]
		}
		}
	header = {
		"Referer": 'http://my.ie.2345.com/onlinefav/web/',
		'User-Agent':'my.ie.2345.com',
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
	#-----------------------------------------------自定义函数-----------------------------------------------
	#访问网页
	def webReadFile(self,urlStr,header):
		html=''
		req=urllib.request.Request(url=urlStr)#,headers=header
		with  urllib.request.urlopen(req)  as response:
			html = response.read().decode('utf-8')
		return html
	#判断网络地址是否存在
	def TestWebPage(self,urlStr,header):
		html=''
		req=urllib.request.Request(url=urlStr,method='HEAD')#,headers=header
		with  urllib.request.urlopen(req)  as response:
			html = response.getcode () 
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
	def get_EpisodesList(self,jsonList):
		videos=[]
		for vod in jsonList:
			url = vod['guid']
			title =vod['title']
			if len(url) == 0:
				continue
			videos.append(title+"$"+url)
		return videos
	#取集数
	def get_EpisodesList_re(self,htmlTxt,patternTxt):
		ListRe=re.finditer(patternTxt, htmlTxt, re.M|re.S)
		videos=[]
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
	def get_list(self,html,tid):
		jRoot = json.loads(html)
		videos = []
		data=jRoot['data']
		if data is None:
			return []

		jsonList=data['list']
		#print(jsonList)
		for vod in jsonList:
			url = vod['url']
			title =vod['title']
			img=vod['image']
			id=vod['id']
			if vod.get('brief')==True:
				brief=vod['brief']
			else:
				brief=''
			if vod.get('year')==True:
				year=vod['year']
			else:
				year='  '
			if len(url) == 0:
				continue
			guid="{0}###{1}###{2}###{3}###{4}###{5}###{6}".format(tid,title,url,img,id,year,brief)
			videos.append({
				"vod_id":guid,
				"vod_name":title,
				"vod_pic":img,
				"vod_remarks":''
			})
		#print(videos)
		return videos
	def get_list1(self,html,tid):
		#return
		jRoot = json.loads(html)

		videos = []
		data=jRoot['response']
		if data is None:
			return []

		jsonList=data['docs']
		#print(jsonList)
		for vod in jsonList:
			id = vod['lastVIDE']['videoSharedCode']
			title =vod['column_name']
			url=vod['column_website']
			img=vod['column_logo']
			year=vod['column_playdate']
			brief=vod['column_brief']
			if len(url) == 0:
				continue
			guid="{0}###{1}###{2}###{3}###{4}###{5}###{6}".format(tid,title,url,img,id,year,brief)
			videos.append({
				"vod_id":guid,
				"vod_name":title,
				"vod_pic":img,
				"vod_remarks":''
			})
		#print(videos)
		return videos
	#删除html标签
	def removeHtml(self,txt):
		soup = re.compile(r'<[^>]+>',re.S)
		txt =soup.sub('', txt)
		return txt.replace("&nbsp;"," ")
	#取m3u8
	def get_m3u8(self,urlTxt):
		url = "https://vdn.apps.cntv.cn/api/getHttpVideoInfo.do?pid={0}".format(urlTxt)
		html=self.webReadFile(urlStr=url,header=self.header)
		jo =json.loads(html)
		link = jo['hls_url'].strip()
		html = self.webReadFile(urlStr=link,header=self.header)
		content = html.strip()
		arr = content.split('\n')
		urlPrefix = self.get_RegexGetText(Text=link,RegexText='(http[s]?://[a-zA-z0-9.]+)/',Index=1)
		subUrl = arr[-1].split('/')
		subUrl[3] = '1200'
		subUrl[-1] = '1200.m3u8'
		hdUrl = urlPrefix + '/'.join(subUrl)

		url = urlPrefix + arr[-1]

		hdRsp = self.TestWebPage(urlStr=hdUrl,header=self.header)
		if hdRsp == 200:
			url = hdUrl
		else:
			url=''
		return url
	#取直播地址
	def get_list_live(self,html,tid):
		ListRe=re.finditer('<li( class="first cur")*?><img src="(?P<src>.+?)" title="(?P<title>.+?)" /></li>', html, re.M|re.S)
		videos=[]
		id=''
		brief=''
		year='  '
		for vod in ListRe:
			img='https:'+vod.group('src')
			title =vod.group('title')
			url = 'https://tv.cctv.com/live/'+title
			if title=='cctvchild':
				url = 'https://tv.cctv.com/live/cctv14'
			guid="{0}###{1}###{2}###{3}###{4}###{5}###{6}".format(tid,title,url,img,id,year,brief)
			videos.append({
				"vod_id":guid,
				"vod_name":title,
				"vod_pic":img,
				"vod_remarks":''
			})
			#print(url)
		return videos
	#搜索
	def get_list_search(self,html,tid):
		jRoot = json.loads(html)
		jsonList=jRoot['list']
		videos=[]
		for vod in jsonList:
			url = vod['urllink']
			title =self.removeHtml(txt=vod['title'])
			img=vod['imglink']
			id=vod['id']
			brief=vod['channel']
			year=vod['uploadtime']
			if len(url) == 0:
				continue
			guid="{0}###{1}###{2}###{3}###{4}###{5}###{6}".format(tid,title,url,img,id,year,brief)
			videos.append({
				"vod_id":guid,
				"vod_name":title,
				"vod_pic":img,
				"vod_remarks":brief
			})
		return videos
