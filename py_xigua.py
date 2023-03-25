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
		return "西瓜视频(个人中心)"
	def init(self,extend=""):
		pass
	def isVideoFormat(self,url):
		pass
	def manualVideoCheck(self):
		pass
	def homeContent(self,filter):
		result = {}
		cateManual = {
			"电视剧":"dianshiju",
			"电影":"dianying",
			"动漫":"dongman",
			"纪录片":"jilupian",
			"少儿":"shaoer",
			"综艺":"zongyi"

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
		rsp = self.fetch('http://www.ikmjw.com/')
		htmlTxt = rsp.text
		videos = self.get_list(html=htmlTxt)
		result = {
			'list': videos
		}
		return result

	def categoryContent(self,tid,pg,filter,extend):
		result = {}
		idTxt='电视剧'
		url = 'https://www.ixigua.com/api/cinema/filterv2/albums'
		if tid=='dianying':
			idTxt='电影'
		elif tid=='zongyi':
			idTxt='综艺'
		elif tid=='dianshiju':
			idTxt='电视剧'
		elif tid=='dongman':
			idTxt='动漫'
		elif tid=='jilupian':
			idTxt='纪录片'
		elif tid=='shaoer':
			idTxt='少儿'	
		offset=0 if int(pg)<2 else 18*int(pg)
		self.header['Referer']='https://www.ixigua.com/cinema/filter/'.format(tid)
		data=r'{"pinyin":"'+tid+'","filters":{"type":"'+idTxt+'","area":"全部地区","tag":"全部类型","sort":"综合排序","paid":"全部资费"},"offset":'+str(offset)+',"limit":18}'
		req = request.Request(url=url, data=bytes(data, encoding='utf8'),headers=self.header, method='POST')
		response = request.urlopen(req)
		urlTxt=response.read().decode('utf-8')
		videos= self.get_list_videoGroup_json(jsonTxt=urlTxt)
		numvL = len(videos)
		result['list'] = videos
		result['page'] = pg
		result['pagecount'] = pg if int(numvL)<17 else int(pg)+1
		result['limit'] = numvL
		result['total'] = numvL
		return result

	def detailContent(self,array):
		result = {}
		aid = array[0].split('###')
		key = aid[1]
		title = aid[0]
		act=aid[2]
		logo = aid[3]
		if len(key)<4:
			return result
		Url='https://www.ixigua.com/api/albumv2/details?albumId={0}'.format(key)
		rsp = self.fetch(Url,headers=self.header)
		htmlTxt = rsp.text
		typeName=''
		area=''
		dir=''
		cont=''
		videoList=[]
		if htmlTxt.find('playlist')>2:
			jRoot = json.loads(htmlTxt)
			if jRoot['code']!=200:
				return result
			jo = jRoot['data']
			jsonList=jo['playlist']
			if jsonList is not None:
				for value in jsonList:
					vipControl=value['vipControl']
					vip='true' if len(vipControl)>0 else 'false'
					id="{0}${1}_{2}".format(value['title'],value['episodeId'],vip)
					videoList.append(id)
			playFrom=[v for v in jo['albumInfo']['tagList']]
			typeName='/'.join(playFrom)
			playFrom=[v for v in jo['albumInfo']['areaList']]
			area='/'.join(playFrom)
			playFrom=[v['name'] for v in jo['albumInfo']['directorList']]
			dir='/'.join(playFrom)
			cont=jo['albumInfo']['intro']
		else:
			videoList= [title+"$https://www.ixigua.com/{0}?logTag=55abe18cfb733871bb04".format(key)]
		vod = {
			"vod_id":array[0],
			"vod_name":title,
			"vod_pic":logo,
			"type_name":typeName,
			"vod_year":'',
			"vod_area":area,
			"vod_remarks":"",
			"vod_actor":'',
			"vod_director":dir,
			"vod_content":cont
		}
		vod['vod_play_from'] = '西瓜'
		vod['vod_play_url'] = "#".join(videoList)
		result = {
			'list':[
				vod
			]
		}
		return result

	def verifyCode(self):
		pass

	def searchContent(self,key,quick):
		Url='http://www.ikmjw.com/ppyssearch.html?wd={0}&submit='.format(urllib.parse.quote(key))
		rsp = self.fetch(Url)
		htmlTxt = rsp.text
		videos = self.get_list(html=htmlTxt)
		result = {
				'list': videos
			}
		return result

	def playerContent(self,flag,id,vipFlags):
		result={}
		UrlId=id.split('_')
		Url='https://www.ixigua.com/{0}'.format(UrlId[0])
		jx=1 if UrlId[1]=='true' else 0
		parse=1 if jx=='1' else 0
		result["parse"] = parse
		result["jx"] = jx
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
	def get_webReadFile(self,urlStr):
		headers = {
			'Referer':urlStr,
			'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
			'Host': 'www.ikmjw.com'
		}
		req = urllib.request.Request(url=urlStr, headers=headers)
		html = urllib.request.urlopen(req).read().decode('utf-8')
		return html
	def get_list(self,html):
		result={}
		jRoot = json.loads(html)
		if jRoot['code']!=200:
			return result
		jo = jRoot['data']['channelFeed']
		vodList = jo['Data']
		if len(vodList)<1:
			return result
		videos=[]
		for vod in vodList:
			data=vod['data']
			if len(data)<1:
				continue
			url =vod['key']
			title =data['title']
			img =vod['data'].get('image_url') 
			maxTime=vod['maxTime']
			if img is None:
				img =data['coverList'][0].get('url')
			if len(url) == 0:
				continue
			#maxTime###标题###地址###封面
			vod_id="{0}###{1}###{2}###{3}".format(maxTime,title,url,img)
			videos.append({
				"vod_id":vod_id,
				"vod_name":title,
				"vod_pic":img,
				"vod_remarks":''
			})
		res = [i for n, i in enumerate(videos) if i not in videos[:n]]
		videos = res
		return videos
	def get_list_videoGroup_json(self,jsonTxt):
		result={}
		jRoot = json.loads(jsonTxt)
		if jRoot['code']!=200:
			return result
		jo = jRoot['data']
		vodList = jo['albumList']
		if len(vodList)<1:
			return result
		videos=[]
		img='_'
		artist='_'
		for vod in vodList:
			url =vod['albumId']
			title =vod['title']
			imgList =vod.get('coverList') 
			if len(imgList)>0:
				img=imgList[0]['url']
			remarks=vod['subTitle']
			artistList=vod.get('actorList') 
			if artistList is not None:
				artistList=artistList if len(artistList)<5 else artistList[0:4]
				artist='/'.join(artistList)
			if len(title)==0:
				continue
			#标题###地址###演员###封面
			vod_id="{0}###{1}###{2}###{3}".format(title,url,artist,img)
			videos.append({
				"vod_id":vod_id,
				"vod_name":title,
				"vod_pic":img,
				"vod_remarks":remarks
			})
		return videos
	def get_lineList(self,Txt,mark,after):
		circuit=[]
		origin=Txt.find(mark)
		while origin>8:
			end=Txt.find(after,origin)
			circuit.append(Txt[origin:end])
			origin=Txt.find(mark,end)
		return circuit
	def get_EpisodesList(self,jsonList):
		vodItems=[]
		for value in jsonList:
			vodItems.append(value['title']+"$"+'https://www.ixigua.com/{0}?logTag=55abe18cfb733871bb04'.format(value['episodeId']))
		return vodItems
	config = {
		"player": {},
		"filter": {}
	}
	header = {
		"Cookie":"MONITOR_WEB_ID=45c3b6ab-7ad4-4805-b971-5962d1d6909a; s_v_web_id=verify_lev3h43l_rrTPrFDG_ztWQ_4ugg_8WBA_yGVYsXlVyoBh; passport_csrf_token=80e0efe90bc8bd6681a896dd90cd08cc; passport_csrf_token_default=80e0efe90bc8bd6681a896dd90cd08cc; sid_guard=54266b282adf9c8dbb69f9cc37342191%7C1678002757%7C3024000%7CSun%2C+09-Apr-2023+07%3A52%3A37+GMT; uid_tt=3c0e8cb286ad3de4d95252bb7d5e0fc6; uid_tt_ss=3c0e8cb286ad3de4d95252bb7d5e0fc6; sid_tt=54266b282adf9c8dbb69f9cc37342191; sessionid=54266b282adf9c8dbb69f9cc37342191; sessionid_ss=54266b282adf9c8dbb69f9cc37342191; sid_ucp_v1=1.0.0-KDQ5MzZiMjFhZjBkODU1MjRiZDMxNThkMzhlNDExYWUwMTY5NTNlZTkKFQjL2cnx9AIQxZSRoAYYGCAMOAhABRoCaGwiIDU0MjY2YjI4MmFkZjljOGRiYjY5ZjljYzM3MzQyMTkx; ssid_ucp_v1=1.0.0-KDQ5MzZiMjFhZjBkODU1MjRiZDMxNThkMzhlNDExYWUwMTY5NTNlZTkKFQjL2cnx9AIQxZSRoAYYGCAMOAhABRoCaGwiIDU0MjY2YjI4MmFkZjljOGRiYjY5ZjljYzM3MzQyMTkx; odin_tt=b9c6f308ba52ea67e84bbbb1024c5071bd43a8f9d3497ff8a336c5e8817236caad3e164515580da83f5a1e4a06a3fab0; __ac_signature=_02B4Z6wo00f01Ktz.lQAAIDBSo2v2RT8BmSrUfrAAE7L2ueb1h-CroqOkPYbaRIeEXRo4R54VWHBZuGMQa5lzlf.ijuXpSsSFdusaGnHj5Ro3JyJCPMcTlPk9Fzj0RPKPk3LCZJ1GmV34nYRe4; support_webp=true; support_avif=false; csrf_session_id=275ef26f7fdf33c95da9f03b9ac611a5; tt_scid=gUK2TRTHs4pYCo-hadXfF.Wjghm2O-.0Cyiy.DGfxytfVrUY-KptBB4prgcFsqqD97d6; ttwid=1%7CCueNR-HU9tGVF30WaiFCjXDxh0FUXoXsZr-cIb9Dogg%7C1679469911%7C2162c32be8a2a1eb373391fcb0d61ec0f684fc7f156dce997de6a4625c0608e8; msToken=e-9KuEl6xQfyp-QconAVI1oSUsTWd_zCP31LrWs8QzVZqlwb4q9PN2gVGAKcb3TWHGauqavlSZ5RNkdCSzHjRyUfrPAawZ5LKXDNZQFkVN6Oi_lnfAiSDPgs4q8Kf6Y7; ixigua-a-s=3",
		"Referer": 'https://www.ixigua.com/cinema/filter/dianshiju/',
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
		'Host': 'www.ixigua.com',
		'Accept': 'application/json, text/plain, */*',
		'x-secsdk-csrf-token': '000100000001db13c92a327d9db47823c4f782dc02c349c214e04ea5b3bc8054eec1bd6f816b174eacf8235b8e44',
		'tt-anti-token': 'iL5itcx8Te-7529d0098c507a2182a34a68b46aaac6cb20382728cbc3083d40028ed01f5c8a',
		'content-type': 'application/json'	
	}

	def localProxy(self,param):
		return [200, "video/MP2T", action, ""]
