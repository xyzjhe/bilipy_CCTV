#coding=utf-8
#!/usr/bin/python
import sys
sys.path.append('..') 
from base.spider import Spider
import json
import time
import base64
import re

class Spider(Spider):  # Ԫ�� Ĭ�ϵ�Ԫ�� type
	def getName(self):
		return "6v��Ӱ"
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
			"����50��": "qian50m",
			"����Ƭ": "donghuapian",
			"�ƻ�Ƭ": "kehuanpian",
			"����Ƭ": "aiqingpian",
			"����Ƭ": "dongzuopian",
			"ϲ��Ƭ": "xijupian",
			"�ֲ�Ƭ": "kongbupian",
			"����Ƭ": "juqingpian",
			"ս��Ƭ": "zhanzhengpian",
			"��¼Ƭ": "jilupian",
			"���Ӿ�": "dianshiju",
			"��  ��": "ZongYi"
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
		url=""
		patternTxt=""
		head="https://www.66s.cc"
		if tid=="qian50m":
			url="https://www.66s.cc/qian50m.html"
		else:
			url="https://www.66s.cc/{0}/".format(tid)
			patternTxt=r'<div class="thumbnail">\s*<a href="(.+)".*?title="(.+?)".*?\n*\s*<img src="(.+?)"'
			if pg>1:
				url=url+"index_{0}.html".format(pg)
		suffix = ""
		rsp = self.fetch(url)
		htmlTxt=rsp.text
		pattern = re.compile(patternTxt)
		ListRe=pattern.findall(htmlTxt)
		videos = []
		for vod in ListRe:
		lastVideo = vod[0]
		if len(lastVideo) == 0:
			lastVideo = '_'
		guid = vod[1]+'###'+lastVideo+'###'+vod[2]
		title = vod[0]
		img = vod[1]
		videos.append({
			"vod_id":guid,
			"vod_name":title,
			"vod_pic":img,
			"vod_remarks":''
		})
		result['list'] = videos
		result['page'] = pg
		result['pagecount'] = 9999
		result['limit'] = 90
		result['total'] = 999999
		return result
	def detailContent(self,array):
		aid = array[0].split('###')
		if aid[2].find("http")<0:
			return {}
		tid = aid[0]
		logo = aid[3]
		lastVideo = aid[2]
		title = aid[1]
		date = aid[0]
		if lastVideo == '_':
			return {}
		rsp = self.fetch(lastVideo)
		htmlTxt=rsp.text
		column_id = ""
		videoList = []
		patternTxt=r"'title':\s*'(.+?)',\n{0,1}\s*'img':\s*'(.+?)',\n{0,1}\s*'brief':\s*'(.+?)',\n{0,1}\s*'url':\s*'(.+?)'"
		titleIndex=0
		UrlIndex=3
		if tid=="���Ӿ�" or tid=="��¼Ƭ":
			patternTxt=r"'title':\s*'(.+?)',\n{0,1}\s*'brief':\s*'(.+?)',\n{0,1}\s*'img':\s*'(.+?)',\n{0,1}\s*'url':\s*'(.+?)'"
			titleIndex=0
			UrlIndex=3
		elif tid=="�ر��Ŀ":
			patternTxt=r'class="tp1"><a\s*href="(https://.+?)"\s*target="_blank"\s*title="(.+?)"></a></div>'
			titleIndex=1
			UrlIndex=0
			#https://api.cntv.cn/NewVideo/getVideoListByAlbumIdNew?id=VIDA3YcIusJ9mh4c9mw5XHyx230113&serviceId=tvcctv//���ڷ�ʽ��ͬ��ʱ����
		pattern = re.compile(patternTxt)
		ListRe=pattern.findall(htmlTxt)
		for value in ListRe:
			videoList.append(value[titleIndex]+"$"+value[UrlIndex])
		if len(videoList) == 0:
			return {}
		vod = {
			"vod_id":array[0],
			"vod_name":title,
			"vod_pic":logo,
			"type_name":tid,
			"vod_year":date,
			"vod_area":"",
			"vod_remarks":date,
			"vod_actor":"",
			"vod_director":column_id,
			"vod_content":aid[4]
		}
		vod['vod_play_from'] = 'CCTV'
		vod['vod_play_url'] = "#".join(videoList)
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

		result["parse"] = 0
		result["playUrl"] = ''
		result["url"] = url
		result["header"] = ''
		return result

	config = {
		"player": {},
		"filter": {"CCTV":[{"key":"cid","name":"Ƶ��","value":[{"n":"ȫ��","v":""},{"n":"CCTV-1�ۺ�","v":"EPGC1386744804340101"},{"n":"CCTV-2�ƾ�","v":"EPGC1386744804340102"},{"n":"CCTV-3����","v":"EPGC1386744804340103"},{"n":"CCTV-4���Ĺ���","v":"EPGC1386744804340104"},{"n":"CCTV-5����","v":"EPGC1386744804340107"},{"n":"CCTV-6��Ӱ","v":"EPGC1386744804340108"},{"n":"CCTV-7��������","v":"EPGC1386744804340109"},{"n":"CCTV-8���Ӿ�","v":"EPGC1386744804340110"},{"n":"CCTV-9��¼","v":"EPGC1386744804340112"},{"n":"CCTV-10�ƽ�","v":"EPGC1386744804340113"},{"n":"CCTV-11Ϸ��","v":"EPGC1386744804340114"},{"n":"CCTV-12����뷨","v":"EPGC1386744804340115"},{"n":"CCTV-13����","v":"EPGC1386744804340116"},{"n":"CCTV-14�ٶ�","v":"EPGC1386744804340117"},{"n":"CCTV-15����","v":"EPGC1386744804340118"},{"n":"CCTV-16����ƥ��","v":"EPGC1634630207058998"},{"n":"CCTV-17ũҵũ��","v":"EPGC1563932742616872"},{"n":"CCTV-5+��������","v":"EPGC1468294755566101"}]},{"key":"fc","name":"����","value":[{"n":"ȫ��","v":""},{"n":"����","v":"����"},{"n":"����","v":"����"},{"n":"����","v":"����"},{"n":"����","v":"����"},{"n":"����","v":"����"},{"n":"�ƽ�","v":"�ƽ�"},{"n":"����","v":"����"},{"n":"ũҵ","v":"ũҵ"},{"n":"����","v":"����"},{"n":"����","v":"����"},{"n":"�ٶ�","v":"�ٶ�"},{"n":"����","v":"����"},{"n":"��ʵ","v":"��ʵ"},{"n":"Ϸ��","v":"Ϸ��"},{"n":"����","v":"����"},{"n":"Ӱ��","v":"Ӱ��"}]},{"key":"fl","name":"��ĸ","value":[{"n":"ȫ��","v":""},{"n":"A","v":"A"},{"n":"B","v":"B"},{"n":"C","v":"C"},{"n":"D","v":"D"},{"n":"E","v":"E"},{"n":"F","v":"F"},{"n":"G","v":"G"},{"n":"H","v":"H"},{"n":"I","v":"I"},{"n":"J","v":"J"},{"n":"K","v":"K"},{"n":"L","v":"L"},{"n":"M","v":"M"},{"n":"N","v":"N"},{"n":"O","v":"O"},{"n":"P","v":"P"},{"n":"Q","v":"Q"},{"n":"R","v":"R"},{"n":"S","v":"S"},{"n":"T","v":"T"},{"n":"U","v":"U"},{"n":"V","v":"V"},{"n":"W","v":"W"},{"n":"X","v":"X"},{"n":"Y","v":"Y"},{"n":"Z","v":"Z"}]},{"key":"year","name":"���","value":[{"n":"ȫ��","v":""},{"n":"2022","v":"2022"},{"n":"2021","v":"2021"},{"n":"2020","v":"2020"},{"n":"2019","v":"2019"},{"n":"2018","v":"2018"},{"n":"2017","v":"2017"},{"n":"2016","v":"2016"},{"n":"2015","v":"2015"},{"n":"2014","v":"2014"},{"n":"2013","v":"2013"},{"n":"2012","v":"2012"},{"n":"2011","v":"2011"},{"n":"2010","v":"2010"},{"n":"2009","v":"2009"},{"n":"2008","v":"2008"},{"n":"2007","v":"2007"},{"n":"2006","v":"2006"},{"n":"2005","v":"2005"},{"n":"2004","v":"2004"},{"n":"2003","v":"2003"},{"n":"2002","v":"2002"},{"n":"2001","v":"2001"},{"n":"2000","v":"2000"}]},{"key":"month","name":"�·�","value":[{"n":"ȫ��","v":""},{"n":"12","v":"12"},{"n":"11","v":"11"},{"n":"10","v":"10"},{"n":"09","v":"09"},{"n":"08","v":"08"},{"n":"07","v":"07"},{"n":"06","v":"06"},{"n":"05","v":"05"},{"n":"04","v":"04"},{"n":"03","v":"03"},{"n":"02","v":"02"},{"n":"01","v":"01"}]}]}
	}
	header = {
		"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36",
		"Origin": "https://tv.cctv.com",
		"Referer": "https://tv.cctv.com/"
	}

	def localProxy(self,param):
		return [200, "video/MP2T", action, ""]
  