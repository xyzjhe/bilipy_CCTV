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
import ssl
class Spider(Spider):
	def getName(self):
		return "卡通站"
	def init(self,extend=""):
		pass
	def isVideoFormat(self,url):
		pass
	def manualVideoCheck(self):
		pass
	def homeContent(self,filter):
		result = {}
		cateManual = {
			"国产动画": "30",
			"日韩动画": "3",
			"国语动画": "1",
			"粤语动画": "2",
			"动漫电影": "4",
			"海外动画": "28"
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
		result = {}
		return result

	def categoryContent(self,tid,pg,filter,extend):
		result = {}
		url = 'http://ktkkt.top/frim/index{0}-{1}.html'.format(tid,pg)
		htmlTxt = self.get_webReadFile(urlStr=url)
		videos = self.get_list(html=htmlTxt)
		result['list'] = videos
		result['page'] = pg
		result['pagecount'] = 10
		result['limit'] = 99
		result['total'] = 99
		return result

	def detailContent(self,array):
		aid = array[0]
		url = 'http://ktkkt.top/movie/{0}.html'.format(aid)
		rsp = self.fetch(url)
		html = rsp.text
		line=self.get_RegexGetTextLine(Text=html,RegexText=r'<a href="#(playlist[1-9]{1,8})"\s*.+?=".+?">(.+?)</a>',Index=1)
		circuit=[]
		for i in line:
			circuit.append(self.get_playlist(Text=html,headStr='id="'+i[0],endStr="</div>"))
		playFrom = []
		videoList=[]
		pattern = re.compile(r'<li class="col.+"><a class=".+" href="(.+?)">(.+?)</a></li>')
		for v in circuit:
			ListRe=pattern.findall(v)
			vodItems = []
			for value in ListRe:
				vodItems.append(value[1]+"$"+value[0])
			joinStr = "#".join(vodItems)
			videoList.append(joinStr)
		playFrom=[t[1] for t in line]
		vod_play_from='$$$'.join(playFrom)
		vod_play_url = "$$$".join(videoList)
		title=self.get_RegexGetText(Text=html,RegexText=r'class="title">(.+?)</',Index=1)
		pic=self.get_RegexGetText(Text=html,RegexText=r'data-original="(.+?)"',Index=1)
		typeName=self.get_RegexGetText(Text=html,RegexText=r'<a href=".+?-----------/">(.+?)</a>',Index=1)
		year=self.get_RegexGetText(Text=html,RegexText=r'<a href=".+?[0-9]{4}/">([0-9]{4}.*?)</a>',Index=1)
		area=self.get_RegexGetText(Text=html,RegexText=r'地区：</span><a href=".+?/">(.*?)</a>',Index=1)
		act=self.get_RegexGetText(Text=html,RegexText=r'<span class="text-muted">主演：(.*?)</p>',Index=1)
		dir=self.get_RegexGetText(Text=html,RegexText=r'<span class="text-muted">导演：(.*?)</p>',Index=1)
		cont=self.get_RegexGetText(Text=html,RegexText=r'简介：</span>(.*?)"',Index=1)
		print(cont)
		vod = {
			"vod_id": aid,
			"vod_name": title,
			"vod_pic": pic,
			"type_name": typeName,
			"vod_year": year,
			"vod_area": area,
			"vod_remarks": '',
			"vod_actor": self.removeHtml(txt=act),
			"vod_director": self.removeHtml(txt=dir),
			"vod_content": cont
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
		retry = 10
		header = {
			"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"}
		while retry:
			try:
				session = requests.session()
				img = session.get('https://ikan6.vip/index.php/verify/index.html?', headers=header).content
				code = session.post('https://api.nn.ci/ocr/b64/text', data=base64.b64encode(img).decode()).text
				res = session.post(url=f"https://ikan6.vip/index.php/ajax/verify_check?type=search&verify={code}",
								   headers=header).json()
				if res["msg"] == "ok":
					return session
			except Exception as e:
				print(e)
			finally:
				retry = retry - 1

	def searchContent(self,key,quick):
		result = {
				'list': []
			}

		return result

	def playerContent(self,flag,id,vipFlags):
		result = {}
		header = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
			"Referer": "https://ikan6.vip/"
		}
		url = 'https://ikan6.vip/{0}'.format(id)
		rsp = self.fetch(url)
		cookie = rsp.cookies
		info = json.loads(self.regStr(reg=r'var player_data=(.*?)</script>', src=rsp.text))
		string = info['url'][8:len(info['url'])]
		substr = base64.b64decode(string).decode('UTF-8')
		str = substr[8:len(substr) - 8]
		if 'Ali' in info['from']:
			url = 'https://cms.ikan6.vip/ali/nidasicaibudaowozaina/nicaibudaowozaina.php?url={0}'.format(str)
		else:
			url = 'https://cms.ikan6.vip/nidasicaibudaowozaina/nicaibudaowozaina.php?url={0}'.format(str)
		rsp = self.fetch(url, headers=header, cookies=cookie)
		randomurl = self.regStr(reg=r"getrandom\(\'(.*?)\'", src=rsp.text)
		pstring = randomurl[8:len(randomurl)]
		psubstr = base64.b64decode(pstring).decode('UTF-8')
		purl = urllib.parse.unquote(psubstr[8:len(psubstr) - 8])
		result["parse"] = 0
		result["playUrl"] = ''
		result["url"] = purl
		result["header"] = ''
		return result
	def get_RegexGetText(self,Text,RegexText,Index):
		returnTxt="null"
		Regex=re.search(RegexText, Text, re.M|re.I)
		if Regex is None:
			returnTxt="null"
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
			'Host': 'www.ktkkt2.com'
		}
		ssl._create_default_https_context = ssl._create_unverified_context#全局取消证书验证
		req = urllib.request.Request(url=urlStr, headers=headers)
		html = urllib.request.urlopen(req).read().decode('utf-8')
		#print(len(html))
		return html
	def get_list(self,html):
		patternTxt=r'<a class="myui-vodlist.*?"\s*href="(.+?)" title="(.+?)"\s*data-original="(.+?)">'
		pattern = re.compile(patternTxt)
		ListRe=pattern.findall(html)
		videos = []
		for vod in ListRe:
			lastVideo = vod[0]
			title =vod[1]
			img =vod[2]
			if len(lastVideo) == 0:
				lastVideo = '_'
			videos.append({
				"vod_id":lastVideo,
				"vod_name":title,
				"vod_pic":img,
				"vod_remarks":''
			})
		return videos
	config = {
		"player": {},
		"filter": {}
	}
	header = {}

	def localProxy(self,param):
		action = {
			'url':'',
			'header':'',
			'param':'',
			'type':'string',
			'after':''
		}
		return [200, "video/MP2T", action, ""]
