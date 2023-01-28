#coding=utf-8
#!/usr/bin/python
import sys
sys.path.append('..') 
from base.spider import Spider
import json
import time
import base64

class Spider(Spider):  # Ԫ�� Ĭ�ϵ�Ԫ�� type
	def getName(self):
		return "����Ƭ��"
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
			"���Ӿ�": "1"
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
		jo = self.fetch(url,headers=self.header).json()
		vodList = jo['response']['docs']
		videos = []
		for vod in vodList:
			lastVideo = vod['lastVIDE']['videoSharedCode']
			if len(lastVideo) == 0:
				lastVideo = '_'
			guid = prefix+'###'+vod['column_name']+'###'+lastVideo+'###'+vod['column_logo']
			# guid = prefix+'###'+vod['column_website']+'###'+vod['column_logo']
			title = vod['column_name']
			img = vod['column_logo']
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
		tid = aid[0]
		logo = aid[3]
		lastVideo = aid[2]
		title = aid[1]
		date = aid[0]
		if lastVideo == '_':
			return {}

		lastUrl = 'https://api.cntv.cn/video/videoinfoByGuid?guid={0}&serviceId=tvcctv'.format(lastVideo)
		lastJo = self.fetch(lastUrl,headers=self.header).json()
		topicId = lastJo['ctid']
		url = "https://api.cntv.cn/NewVideo/getVideoListByColumn?id={0}&d={1}&p=1&n=100&sort=desc&mode=0&serviceId=tvcctv&t=json".format(topicId,date)
		jo = self.fetch(url,headers=self.header).json()
		vodList = jo['data']['list']
		videoList = []
		for video in vodList:
			videoList.append(video['title']+"$"+video['guid'])
		if len(videoList) == 0:
			return {}
		if len(date) == 0:
			date = time.strftime("%Y", time.localtime(time.time()))
		vod = {
			"vod_id":array[0],
			"vod_name":date +" "+title,
			"vod_pic":logo,
			"type_name":lastJo['channel'],
			"vod_year":date,
			"vod_area":"",
			"vod_remarks":date,
			"vod_actor":"",
			"vod_director":topicId,
			"vod_content":"��ǰҳ��Ĭ��ֻչʾ����100�ڵ����ݣ����ڷ���ҳ��ѡ����ݺ��·ݽ������ڽ�Ŀ�鿴����ݺ��·ݽ�Ӱ�쵱ǰҳ�����ݣ������������ˡ���ƵĬ�ϲ��ſ��Ի�ȡ�������֡�ʡ�"
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
		url = "https://vdn.apps.cntv.cn/api/getHttpVideoInfo.do?pid={0}".format(id)
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