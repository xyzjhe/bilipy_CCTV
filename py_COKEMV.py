#coding=utf-8
#!/usr/bin/python
import sys
sys.path.append('..')
from base.spider import Spider
import base64
import math
import json
import requests
import urllib
from urllib import request, parse
import urllib.request
import re
#https://cokemv.me/vodshow/1--------2---.html
class Spider(Spider):
	def getName(self):
		return "COKEMV"
	def init(self,extend=""):
		pass
	def isVideoFormat(self,url):
		pass
	def manualVideoCheck(self):
		pass
	def homeContent(self,filter):
		result = {}
		cateManual = {
			"电影": "1",
			"剧集": "2",
			"动漫": "3",
			"综艺": "29",
			"抖音电影": "34",
			"新片快递": "35"
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
		rsp = self.fetch('https://cokemv.me/')
		htmlTxt = rsp.text
		videos = self.get_list(html=htmlTxt)
		result = {
			'list': videos
		}
		return result

	def categoryContent(self,tid,pg,filter,extend):
		result = {}
		types=tid
		if 'types' in extend.keys():
			types=urllib.parse.quote(extend['types']) if extend['types']!='' else ''#类型
		area=''
		if 'area' in extend.keys():
			area=urllib.parse.quote(extend['area']) if extend['area']!='' else ''
		content=''
		if 'content' in extend.keys():
			content=urllib.parse.quote(extend['content']) if extend['content']!='' else ''
		time=''
		if 'time' in extend.keys():
			time=urllib.parse.quote(extend['time']) if extend['time']!='' else ''
		language=''
		if 'language' in extend.keys():
			language=urllib.parse.quote(extend['language']) if extend['language']!='' else ''
		letter=''
		if 'letter' in extend.keys():
			letter=urllib.parse.quote(extend['letter']) if extend['letter']!='' else ''
		url = 'https://cokemv.me/vodshow/{0}-{1}-time-{2}-{4}-{5}---{6}---{3}.html'.format(types,area,content,time,language,letter,pg)
		rsp = self.fetch(url)
		htmlTxt=rsp.text
		videos = self.get_list(html=htmlTxt)
		pag=self.get_RegexGetText(Text=htmlTxt,RegexText=r'<a href=".+?-([0-9]+?)---.html" class="page-link page-next" title="尾页">尾页</a>',Index=1)
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
		Url='https://cokemv.me{0}'.format(idUrl)
		rsp = self.fetch(Url)
		htmlTxt = rsp.text
		line=self.get_RegexGetTextLine(Text=htmlTxt,RegexText=r'data-dropdown-value="(.+?)"><span>.+?</span>',Index=1)
		if len(line)<1:
			return  {'list': []}
		circuit=self.get_lineList(Txt=htmlTxt)
		playFrom = []
		videoList=[]
		pattern = re.compile(r'<a class="module-play-list-link" href="(.+?)" title="(.+?)"><span>.+?</span></a>')
		for v in circuit:
			ListRe=pattern.findall(v)
			vodItems = []
			for value in ListRe:
				vodItems.append(value[1]+"$"+value[0])
			joinStr = "#".join(vodItems)
			videoList.append(joinStr)
		playFrom=[t for t in line]
		vod_play_from='$$$'.join(playFrom)
		vod_play_url = "$$$".join(videoList)
		typeName=self.get_RegexGetText(Text=htmlTxt,RegexText=r'<a href="/vodshow.+?-\.html">(.+?)</a><span class="slash">',Index=1)
		year=self.get_RegexGetText(Text=htmlTxt,RegexText=r'href="/vodshow.+?[0-9]{4}\.html">([0-9]{4})</a></div>',Index=1)
		area=self.get_RegexGetText(Text=htmlTxt,RegexText=r'<a href=.+?-\.html">(.+?)</a></',Index=1)
		act=self.get_RegexGetText(Text=htmlTxt,RegexText=r'主演：(.+?)</div>',Index=1)
		dir=self.get_RegexGetText(Text=htmlTxt,RegexText=r'导演：(.+?)</div>',Index=1)
		cont=self.get_RegexGetText(Text=htmlTxt,RegexText=r'<p>(.+?)</p>',Index=1)
		vod = {
			"vod_id": array[0],
			"vod_name": title,
			"vod_pic": pic,
			"type_name": typeName,
			"vod_year": year,
			"vod_area": self.removeHtml(txt=area),
			"vod_remarks": '',
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
		result = {
				'list': []
			}
		return result

	def playerContent(self,flag,id,vipFlags):
		result = {}
		Url='https://cokemv.me{0}'.format(id)
		rsp = self.fetch(Url)
		htmlTxt = rsp.text
		playUrl=Url
		parse=1
		m3u8Line=self.get_RegexGetTextLine(Text=htmlTxt,RegexText=r'url":"(.+?\.m3u8)"',Index=1)
		if len(m3u8Line)>0:
			playUrl="https://cokemv.me"+m3u8Line[0].replace("\\","")
			parse=0
		if playUrl.count('https:')>1 and len(m3u8Line)>0:
			playUrl=m3u8Line[0].replace("\\","")
		if self.get_RegexGetText(Text=id,RegexText=r'-([0-9]{1,2})-[0-9]+?',Index=1)=='1' or playUrl.find('.m3u8')<1:
			playUrl='https://cokemv.me{0}'.format(id)
			parse=1
		result["parse"] = parse
		result["playUrl"] = ''
		result["url"] = playUrl
		result["header"] = ''
		return result
	def get_RegexGetText(self,Text,RegexText,Index):
		returnTxt=""
		Regex=re.search(RegexText, Text, re.M|re.S)
		if Regex is None:
			returnTxt=""
		else:
			returnTxt=Regex.group(Index)
		return returnTxt	
	def get_RegexGetTextLine(self,Text,RegexText,Index):
		returnTxt=[]
		pattern = re.compile(RegexText)
		ListRe=pattern.findall(Text)
		if len(ListRe)<1:
			return returnTxt
		for value in ListRe:
			returnTxt.append(value)	
		return returnTxt
	def get_playlist(self,Text,headStr,endStr):
		circuit=""
		origin=Text.find(headStr)
		if origin>8:
			end=Text.find(endStr,origin)
			circuit=Text[origin:end]
		return circuit
	def removeHtml(self,txt):
		soup = re.compile(r'<[^>]+>',re.S)
		txt =soup.sub('', txt)
		return txt.replace("&nbsp;"," ")
	def get_webReadFile(self,urlStr):
		headers = {
			'Referer':urlStr,
			'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
			'Host': 'cokemv.me'
		}
		req = urllib.request.Request(url=urlStr, headers=headers)
		html = urllib.request.urlopen(req).read().decode('utf-8')
		return html
	def get_list(self,html):
		patternTxt=r'<a href="(.+?)" title="(.+?)" class="module-poster-item module-item">'
		pattern = re.compile(patternTxt)
		ListRe=pattern.findall(html)
		imgPattern = re.compile('data-original="(.+?)"')
		imgListRe=imgPattern.findall(html)
		videos = []
		i=0
		if len(imgListRe)!=len(ListRe):
			return videos
		for vod in ListRe:
			url = vod[0]
			title =vod[1]
			img =imgListRe[i]
			if len(url) == 0:
				url = '_'
			videos.append({
				"vod_id":"{0}###{1}###{2}".format(title,url,img),
				"vod_name":title,
				"vod_pic":img,
				"vod_remarks":''
			})
			i=i+1
		return videos
	def get_lineList(self,Txt):
		circuit=[]
		origin=Txt.find('<div class="module-play-list">')
		while origin>8:
			end=Txt.find('</div>',origin)
			circuit.append(Txt[origin:end])
			origin=Txt.find('<div class="module-play-list">',end)
		return circuit
	config = {
		"player": {},
		"filter": {
		"1":[#电影
		{"key":"types","name":"类型","value":[{"n":"全部","v":"1"},{"n":"爱情片","v":"6"},{"n":"喜剧片","v":"7"},{"n":"动作片","v":"8"},{"n":"科幻片","v":"9"},{"n":"冒险片","v":"30"},{"n":"恐怖片","v":"10"},{"n":"惊悚片","v":"11"},{"n":"犯罪片","v":"12"},{"n":"武侠片","v":"31"},{"n":"动画片","v":"33"},{"n":"悬疑片","v":"20"},{"n":"剧情片","v":"21"},{"n":"奇幻片","v":"22"},{"n":"战争片","v":"23"}]},
		#分隔
		{"key":"content","name":"剧情","value":[{"n":"全部","v":""},{"n":"喜剧","v":"喜剧"},{"n":"爱情","v":"爱情"},{"n":"恐怖","v":"恐怖"},{"n":"动作","v":"动作"},{"n":"科幻","v":"科幻"},{"n":"剧情","v":"剧情"},{"n":"战争","v":"战争"},{"n":"警匪","v":"警匪"},{"n":"犯罪","v":"犯罪"},{"n":"动画","v":"动画"},{"n":"奇幻","v":"奇幻"},{"n":"武侠","v":"武侠"},{"n":"冒险","v":"冒险"},{"n":"枪战","v":"枪战"},{"n":"恐怖","v":"恐怖"},{"n":"悬疑","v":"悬疑"},{"n":"惊悚","v":"惊悚"},{"n":"经典","v":"经典"},{"n":"青春","v":"青春"},{"n":"文艺","v":"文艺"},{"n":"古装","v":"古装"},{"n":"历史","v":"历史"},{"n":"微电影","v":"微电影"},{"n":"农村","v":"农村"},{"n":"儿童","v":"儿童"},{"n":"网络电影","v":"网络电影"},{"n":"运动","v":"运动"}]},
		#分隔
		{"key":"area","name":"地区","value":[{"n":"全部","v":""},{"n":"中国大陆","v":"中国大陆"},{"n":"韩国","v":"韩国"},{"n":"中国香港","v":"香港"},{"n":"中国台湾","v":"台湾"},{"n":"日本","v":"日本"},{"n":"美国","v":"美国"},{"n":"英国","v":"英国"},{"n":"泰国","v":"泰国"},{"n":"新加坡","v":"新加坡"},{"n":"加拿大","v":"加拿大"},{"n":"其他","v":"其他"}]},
		#分隔
		{"key":"time","name":"年份","value":[{"n":"全部","v":""},{"n":"2022","v":"2022"},{"n":"2021","v":"2021"},{"n":"2020","v":"2020"},{"n":"2019","v":"2019"},{"n":"2018","v":"2018"},{"n":"2017","v":"2017"},{"n":"2016","v":"2016"},{"n":"2015","v":"2015"},{"n":"2014","v":"2014"},{"n":"2013","v":"2013"},{"n":"2012","v":"2012"},{"n":"2011","v":"2011"},{"n":"2010","v":"2010"}]},
		#分隔
		{"key":"language","name":"语言","value":[{"n":"全部","v":""},{"n":"国语","v":"国语"},{"n":"英语","v":"英语"},{"n":"粤语","v":"粤语"},{"n":"闽南话","v":"闽南语"},{"n":"韩语","v":"韩语"},{"n":"日语","v":"日语"},{"n":"法语","v":"法语"},{"n":"德语","v":"德语"},{"n":"其它","v":"其它"}]},
		#分隔
		{"key":"letter","name":"字母","value":[{"n":"全部","v":""},{"n":"A","v":"A"},{"n":"C","v":"C"},{"n":"E","v":"E"},{"n":"F","v":"F"},{"n":"G","v":"G"},{"n":"H","v":"H"},{"n":"I","v":"I"},{"n":"J","v":"J"},{"n":"K","v":"K"},{"n":"L","v":"L"},{"n":"M","v":"M"},{"n":"N","v":"N"},{"n":"O","v":"O"},{"n":"P","v":"P"},{"n":"Q","v":"Q"},{"n":"R","v":"R"},{"n":"S","v":"S"},{"n":"T","v":"T"},{"n":"U","v":"U"},{"n":"V","v":"V"},{"n":"W","v":"W"},{"n":"X","v":"X"},{"n":"Y","v":"Y"},{"n":"Z","v":"Z"},{"n":"0-9","v":"0-9"}]}
		],
		#分隔
		"2":[
		{"key":"types","name":"类型","value":[{"n":"全部","v":"2"},{"n":"大陆剧","v":"13"},{"n":"韩国剧","v":"14"},{"n":"日本剧","v":"15"},{"n":"港剧","v":"16"},{"n":"欧美剧","v":"32"},{"n":"台湾剧","v":"24"},{"n":"泰国剧","v":"25"},{"n":"纪录片","v":"26"}]},
		#分隔
		{"key":"content","name":"剧情","value":[{"n":"全部","v":""},{"n":"大陆剧","v":"大陆剧"},{"n":"韩国剧","v":"韩国剧"},{"n":"日本剧","v":"日本剧"},{"n":"港剧","v":"港剧"},{"n":"欧美剧","v":"欧美剧"},{"n":"台湾剧","v":"台湾剧"},{"n":"泰国剧","v":"泰国剧"},{"n":"纪录片","v":"记录片"}]},
		#分隔
		{"key":"area","name":"地区","value":[{"n":"全部","v":""},{"n":"中国大陆","v":"中国大陆"},{"n":"韩国","v":"韩国"},{"n":"中国香港","v":"中国香港"},{"n":"中国台湾","v":"中国台湾"},{"n":"日本","v":"日本"},{"n":"美国","v":"美国"},{"n":"英国","v":"英国"},{"n":"泰国","v":"泰国"},{"n":"新加坡","v":"新加坡"},{"n":"加拿大","v":"加拿大"},{"n":"其他","v":"其他"}]},
		#分隔
		{"key":"time","name":"年份","value":[{"n":"全部","v":""},{"n":"2022","v":"2022"},{"n":"2021","v":"2021"},{"n":"2020","v":"2020"},{"n":"2019","v":"2019"},{"n":"2018","v":"2018"},{"n":"2017","v":"2017"},{"n":"2016","v":"2016"},{"n":"2015","v":"2015"},{"n":"2014","v":"2014"},{"n":"2013","v":"2013"},{"n":"2012","v":"2012"},{"n":"2011","v":"2011"},{"n":"2010","v":"2010"},{"n":"2009","v":"2009"},{"n":"2008","v":"2008"},{"n":"2007","v":"2007"},{"n":"2006","v":"2006"},{"n":"2005","v":"2005"},{"n":"2004","v":"2004"}]},
		#分隔
		{"key":"language","name":"语言","value":[{"n":"全部","v":""},{"n":"国语","v":"国语"},{"n":"英语","v":"英语"},{"n":"粤语","v":"粤语"},{"n":"闽南话","v":"闽南语"},{"n":"韩语","v":"韩语"},{"n":"日语","v":"日语"},{"n":"其它","v":"其它"}]},
		#分隔
		{"key":"letter","name":"字母","value":[{"n":"全部","v":""},{"n":"A","v":"A"},{"n":"C","v":"C"},{"n":"E","v":"E"},{"n":"F","v":"F"},{"n":"G","v":"G"},{"n":"H","v":"H"},{"n":"I","v":"I"},{"n":"J","v":"J"},{"n":"K","v":"K"},{"n":"L","v":"L"},{"n":"M","v":"M"},{"n":"N","v":"N"},{"n":"O","v":"O"},{"n":"P","v":"P"},{"n":"Q","v":"Q"},{"n":"R","v":"R"},{"n":"S","v":"S"},{"n":"T","v":"T"},{"n":"U","v":"U"},{"n":"V","v":"V"},{"n":"W","v":"W"},{"n":"X","v":"X"},{"n":"Y","v":"Y"},{"n":"Z","v":"Z"},{"n":"0-9","v":"0-9"}]}
		],
		#分隔
		"3":[
		{"key":"types","name":"类型","value":[{"n":"全部","v":"3"},{"n":"国产动漫","v":"27"},{"n":"日本动漫","v":"28"}]},
		#分隔
		{"key":"content","name":"剧情","value":[{"n":"全部","v":""},{"n":"情感","v":"情感"},{"n":"科幻","v":"科幻"},{"n":"热血","v":"热血"},{"n":"推理","v":"推理"},{"n":"搞笑","v":"搞笑"},{"n":"冒险","v":"冒险"},{"n":"萝莉","v":"萝莉"},{"n":"校园","v":"校园"},{"n":"动作","v":"动作"},{"n":"机战","v":"机战"},{"n":"运动","v":"运动"},{"n":"战争","v":"战争"},{"n":"少年","v":"少年"},{"n":"少女","v":"少女"},{"n":"社会","v":"社会"},{"n":"原创","v":"原创"},{"n":"亲子","v":"亲子"},{"n":"益智","v":"益智"},{"n":"励志","v":"励志"},{"n":"其他","v":"其他"}]},
		#分隔
		{"key":"area","name":"地区","value":[{"n":"全部","v":""},{"n":"中国大陆","v":"中国大陆"},{"n":"韩国","v":"韩国"},{"n":"中国香港","v":"香港"},{"n":"中国台湾","v":"台湾"},{"n":"日本","v":"日本"},{"n":"泰国","v":"泰国"},{"n":"其他","v":"其他"}]},
		#分隔
		{"key":"time","name":"年份","value":[{"n":"全部","v":""},{"n":"2022","v":"2022"},{"n":"2021","v":"2021"},{"n":"2020","v":"2020"},{"n":"2019","v":"2019"},{"n":"2018","v":"2018"},{"n":"2017","v":"2017"},{"n":"2016","v":"2016"},{"n":"2015","v":"2015"},{"n":"2014","v":"2014"},{"n":"2013","v":"2013"},{"n":"2012","v":"2012"},{"n":"2011","v":"2011"},{"n":"2010","v":"2010"},{"n":"2009","v":"2009"},{"n":"2008","v":"2008"},{"n":"2007","v":"2007"},{"n":"2006","v":"2006"},{"n":"2005","v":"2005"},{"n":"2004","v":"2004"}]},
		#分隔
		{"key":"language","name":"语言","value":[{"n":"全部","v":""},{"n":"国语","v":"国语"},{"n":"英语","v":"英语"},{"n":"粤语","v":"粤语"},{"n":"闽南话","v":"闽南语"},{"n":"韩语","v":"韩语"},{"n":"日语","v":"日语"},{"n":"其它","v":"其它"}]},
		#分隔
		{"key":"letter","name":"字母","value":[{"n":"全部","v":""},{"n":"A","v":"A"},{"n":"C","v":"C"},{"n":"E","v":"E"},{"n":"F","v":"F"},{"n":"G","v":"G"},{"n":"H","v":"H"},{"n":"I","v":"I"},{"n":"J","v":"J"},{"n":"K","v":"K"},{"n":"L","v":"L"},{"n":"M","v":"M"},{"n":"N","v":"N"},{"n":"O","v":"O"},{"n":"P","v":"P"},{"n":"Q","v":"Q"},{"n":"R","v":"R"},{"n":"S","v":"S"},{"n":"T","v":"T"},{"n":"U","v":"U"},{"n":"V","v":"V"},{"n":"W","v":"W"},{"n":"X","v":"X"},{"n":"Y","v":"Y"},{"n":"Z","v":"Z"},{"n":"0-9","v":"0-9"}]}
		],
		#分隔
		"29":[
		#分隔
		{"key":"area","name":"地区","value":[{"n":"全部","v":""},{"n":"中国大陆","v":"中国大陆"},{"n":"韩国","v":"韩国"},{"n":"中国香港","v":"中国香港"},{"n":"中国台湾","v":"中国台湾"},{"n":"日本","v":"日本"},{"n":"美国","v":"美国"},{"n":"加拿大","v":"加拿大"},{"n":"泰国","v":"泰国"},{"n":"英国","v":"英国"},{"n":"新加坡","v":"新加坡"},{"n":"其他","v":"其他"}]},
		#分隔
		{"key":"time","name":"年份","value":[{"n":"全部","v":""},{"n":"2022","v":"2022"},{"n":"2021","v":"2021"},{"n":"2020","v":"2020"},{"n":"2019","v":"2019"},{"n":"2018","v":"2018"},{"n":"2017","v":"2017"},{"n":"2016","v":"2016"},{"n":"2015","v":"2015"},{"n":"2014","v":"2014"},{"n":"2013","v":"2013"},{"n":"2012","v":"2012"},{"n":"2011","v":"2011"},{"n":"2010","v":"2010"}]},
		#分隔
		{"key":"language","name":"语言","value":[{"n":"全部","v":""},{"n":"国语","v":"国语"},{"n":"英语","v":"英语"},{"n":"粤语","v":"粤语"},{"n":"闽南话","v":"闽南语"},{"n":"韩语","v":"韩语"},{"n":"日语","v":"日语"},{"n":"其它","v":"其它"}]},
		#分隔
		{"key":"letter","name":"字母","value":[{"n":"全部","v":""},{"n":"A","v":"A"},{"n":"C","v":"C"},{"n":"E","v":"E"},{"n":"F","v":"F"},{"n":"G","v":"G"},{"n":"H","v":"H"},{"n":"I","v":"I"},{"n":"J","v":"J"},{"n":"K","v":"K"},{"n":"L","v":"L"},{"n":"M","v":"M"},{"n":"N","v":"N"},{"n":"O","v":"O"},{"n":"P","v":"P"},{"n":"Q","v":"Q"},{"n":"R","v":"R"},{"n":"S","v":"S"},{"n":"T","v":"T"},{"n":"U","v":"U"},{"n":"V","v":"V"},{"n":"W","v":"W"},{"n":"X","v":"X"},{"n":"Y","v":"Y"},{"n":"Z","v":"Z"},{"n":"0-9","v":"0-9"}]}
		]
		}
		}
	header = {
		"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36",
		'Host': 'cokemv.me',
		"Referer": "http://cokemv.me/"
		}

	def localProxy(self,param):
		return [200, "video/MP2T", action, ""]
