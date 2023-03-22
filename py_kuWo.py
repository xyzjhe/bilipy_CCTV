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

class Spider(Spider):
	def getName(self):
		return "酷我MV"
	def init(self,extend=""):
		pass
	def isVideoFormat(self,url):
		pass
	def manualVideoCheck(self):
		pass
	def homeContent(self,filter):
		result = {}
		cateManual = {
			"首播": "236682871",
			"华语": "236682731",
			"日韩": "236742444",
			"欧美": "236682735",
			"网络": "236682773",
			"现场": "236742576",
			"热舞": "236682777",
			"伤感": "236742508",
			"剧情": "236742578"
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
		result = {
			'list': []
		}
		return result

	def categoryContent(self,tid,pg,filter,extend):
		result = {}
		url = 'http://www.kuwo.cn/api/www/music/mvList?pid={0}&pn={1}&rn=20'.format(tid,pg)
		self.header['Referer']='http://www.kuwo.cn/mvs'
		rsp = self.fetch(url,headers=self.header)
		htmlTxt=rsp.text
		videos = self.get_list(html=htmlTxt)
		numvL = len(videos)
		result['list'] = videos
		result['page'] = pg
		result['pagecount'] =  pg if numvL<10 else int(pg)+1
		result['limit'] = numvL
		result['total'] = numvL
		return result

	def detailContent(self,array):
		aid = array[0].split('###')
		url=aid[1]
		title=aid[0]
		pic=aid[3]
		artist=aid[2]
		vodItems = [title+"$"+'http://www.kuwo.cn/mvplay/'+url]
		vod = {
			"vod_id": array[0],
			"vod_name": title,
			"vod_pic": pic,
			"type_name": 'Mv',
			"vod_year": '',
			"vod_area": '',
			"vod_remarks": "",
			"vod_actor": artist,
			"vod_director": '',
			"vod_content": ''
		}
		vod['vod_play_from'] = '酷我'
		vod['vod_play_url'] = "#".join(vodItems)

		result = {
			'list': [
				vod
			]
		}
		return result

	def verifyCode(self):
		pass

	def searchContent(self,key,quick):
		key=urllib.parse.quote(key)
		Url='http://www.kuwo.cn/api/www/search/searchMvBykeyWord?key={0}&pn=1&rn=20&httpsStatus=1&reqId=4aa962c0-c633-11ed-a98b-415331bc6c4d'.format(key)
		self.header['Referer']='http://www.kuwo.cn/search/mv?key='+key
		rsp = self.fetch(Url,headers=self.header)
		htmlTxt = rsp.text
		videos = self.get_list(html=htmlTxt)
		result = {
				'list': videos
			}
		return result

	def playerContent(self,flag,id,vipFlags):
		result = {}
		parse=1
		Url=id
		self.header['Referer']='http://www.kuwo.cn'
		rsp = self.fetch(Url)
		htmlTxt = rsp.text
		m3u8Line=self.get_RegexGetTextLine(Text=htmlTxt,RegexText=r'src:"(http.+?mp4)"',Index=1)
		if len(m3u8Line)>0:
			Url=m3u8Line[0].replace('\\u002F',r'/')
		if Url.find('.mp4')<1:
			parse=0
			Url=id
		result["parse"] = parse
		result["playUrl"] = ''
		result["url"] = Url
		result["header"] = ''
		return result
	def get_RegexGetText(self,Text,RegexText,Index):
		returnTxt=""
		Regex=re.search(RegexText, Text, re.M|re.I)
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
	
		req = urllib.request.Request(url=urlStr, headers=headers)
		html = urllib.request.urlopen(req).read().decode('utf-8')
		return html
	def get_list(self,html):
		result={}
		jRoot = json.loads(html)
		if jRoot['code']!=200:
			return result
		jo = jRoot['data']
		vodList = jo['mvlist']
		if len(vodList)<1:
			return result
		videos=[]
		for vod in vodList:
			url =vod['id']
			title =vod['name']
			img =vod['pic']
			remarks=vod['songTimeMinutes']
			artist=vod['artist']
			if len(title)==0:
				continue
			#标题###地址###作者###封面
			vod_id="{0}###{1}###{2}###{3}".format(title,url,artist,img)
			videos.append({
				"vod_id":vod_id,
				"vod_name":title,
				"vod_pic":img,
				"vod_remarks":remarks
			})
		return videos
	config = {
		"player": {},
		"filter": {}
	}
	header = {
		"Cookie":"kw_token=06YETB13BS0E",
		"csrf":"06YETB13BS0E",
		"Referer": 'http://www.kuwo.cn/search/mv?key=',
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
		'Host': 'www.kuwo.cn'
		}
	def localProxy(self,param):
		return [200, "video/MP2T", action, ""]
