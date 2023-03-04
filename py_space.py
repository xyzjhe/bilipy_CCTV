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
			"个人收藏": "Collection"
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
		rsp = self.fetch('http://my.ie.2345.com/onlinefav/web/getAllData?action=getData&id=21492773&s=&d=Fri%20Mar%2003%202023%2008:45:08%20GMT+0800%20(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)',headers=self.header)
		htmlTxt = rsp.text
		videos = self.get_list(html=htmlTxt)
		result['list'] = videos
		result['page'] = pg
		result['pagecount'] = 1
		result['limit'] = 90
		result['total'] = 999999
		return result
	def detailContent(self,array):
		result = {}
		aid = array[0].split('###')
		if aid[1].find("http")<0:
			return result
		tid = aid[0]
		logo = aid[2]
		url = aid[1]
		title = aid[0]
		if url == '_':
			return result
		vodItems = [title+"$"+url]
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
		vod['vod_play_from'] = "线路"
		vod['vod_play_url'] = "#".join(vodItems)
		result = {
			'list':[
				vod
			]
		}
		print(result)
		return result

	def searchContent(self,key,quick):
		result = {
			'list':[]
		}
		return result
	def playerContent(self,flag,id,vipFlags):
		result = {}
		header= {
			"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3947.100 Mobile Safari/537.36"
		}
		result["parse"] = 2
		result["playUrl"] =""
		result["url"] = id
		result["header"] =''
		return result
	def get_playUrlMethodOne(self,html):
		#自定义函数时self参数是必要的,调用时self参数留空
		pattern =re.search( r'<div class="video"><iframe.+?src="(.+?)"></iframe></div>', html, re.M|re.I).group(1)
		if len(pattern)<4:
			return ""
		rsp = self.fetch(pattern)
		htmlTxt=rsp.text
		head=re.search( r'(https{0,1}://.+?)/', pattern, re.M|re.I).group(1)
		if len(head)<4:
			return ""
		url=re.search( r'var\smain\s*=\s*"(.+?)"', htmlTxt, re.M|re.I).group(1)
		url=head+url
		return url
	def get_collection_xg(html):
		videoList = []
		pattern = re.compile(r'title="(.+?)"\s*href="(.+?&amp;)".+? src="(.+?)"')
		ListRe=pattern.findall(html)
		for video in ListRe:
			videoList.append(video[0]+"$https://www.ixigua.com"+video[1].replace('&amp;' , '&'))
		return videoList
	def webReadFile(self,urlStr):
		if urlStr.find("http")<0:
			return ""
		req = urllib.request.Request(url=urlStr, headers=self.header)
		html = urllib.request.urlopen(req).read().decode('utf-8')
		return html
	def get_UrlParameter(self,parameter):
		aid =parameter.split('###')
		for t in aid:
			if t.find("http")>-1 and t.find("html")>-1:
				return t	
		return "https://www.ixigua.com/"	
	def get_list(self,html):
		patternTxt=r'<a href=\\"(http.+?)\\" title=\\"(.+?)\\" target=\\"_blank\\">(.+?)</a>'
		pattern = re.compile(patternTxt)
		ListRe=pattern.findall(html)
		img ='http://photo.16pic.com/00/78/41/16pic_7841675_b.jpg'
		videos = []
		i=0
		for vod in ListRe:
			lastVideo = vod[0]
			title =vod[1]
			
			if len(lastVideo) == 0:
				lastVideo = '_'
			videos.append({
				"vod_id":"{0}###{1}###{2}".format(title,lastVideo,img),
				"vod_name":title,
				"vod_pic":img,
				"vod_remarks":''
			})
		res = [i for n, i in enumerate(videos) if i not in videos[:n]]
		videos = res
		return videos
	config = {
		"player": {},
		"filter": {}
		}
	header = {
		"Referer": 'http://my.ie.2345.com/onlinefav/web/',
		'User-Agent':'my.ie.2345.com',
		'Cookie':'uUiD=35752164629621148571735; name_ie=%2534013%2528023%2522320%2526143%2520154; I=i%3D90475631%26u%3D88890231%26n%3D%25C0%25B6%25BA%25A3%25B5%25D8%25D0%25C7%25C8%25CB%26m%3D0%26t%3D1675499574.1711300%26s%3D6a22a64feb086a03715e47d4cc3e8a29%26v%3D1.1; sData=6392F231FBE75023D053CEFE20A81E6EE43333BF6FF9CD4610BA32AB109E43FD1742EBAAA408F5EB45E7E1A10A40174BC8EE73651C7AD84AC5840AEA48B014F46FE421C992A7799DBF763B0E743AC8716814F0237BC8F8CC62FCF9F8A283040ADD791FBDD3470D699AA43B70F9886350F57021D6DB5E7B8E001ABEFE70C38424; site_str_flag=2; need_modify_name=0; skin=0; theme=0; ggbd=0'
	}

	def localProxy(self,param):
		return [200, "video/MP2T", action, ""]