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
			"个人收藏": "Collection",
			"本地文件":"File"
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
		if pg!='1':
			return result
		if tid=='Collection':
			Url='http://my.ie.2345.com/onlinefav/web/getAllData?action=getData&id=21492773&s=&d=Fri%20Mar%2003%202023%2008:45:08%20GMT+0800%20(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)'
			videos = self.get_list(html=self.webReadFile(urlStr=Url,header=self.header))
		elif  tid=='File':
			
		else:
			pass
		result['list'] = videos
		result['page'] = pg
		result['pagecount'] = 1
		result['limit'] = 90
		result['total'] = 999999
		return result
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
		elif tid=='File':
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
		if id.find('www.huya.com')>0:
			headers= {
			'User-Agent':'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 SE 2.X MetaSr 1.0'
		}
		result["parse"] = parse
		result["playUrl"] = ''
		result["url"] = id
		result['jx'] = jx#VIP解析
		result["header"] = headers	
		return result
	def localProxy(self,param):
		return [200, "video/MP2T", action, ""]

	config = {
		"player": {},
		"filter": {}
		}
	header = {
		"Referer": 'http://my.ie.2345.com/onlinefav/web/',
		'User-Agent':'my.ie.2345.com',
		'Cookie':'uUiD=35752164629621148571735; name_ie=%2534013%2528023%2522320%2526143%2520154; I=i%3D90475631%26u%3D88890231%26n%3D%25C0%25B6%25BA%25A3%25B5%25D8%25D0%25C7%25C8%25CB%26m%3D0%26t%3D1675499574.1711300%26s%3D6a22a64feb086a03715e47d4cc3e8a29%26v%3D1.1; sData=6392F231FBE75023D053CEFE20A81E6EE43333BF6FF9CD4610BA32AB109E43FD1742EBAAA408F5EB45E7E1A10A40174BC8EE73651C7AD84AC5840AEA48B014F46FE421C992A7799DBF763B0E743AC8716814F0237BC8F8CC62FCF9F8A283040ADD791FBDD3470D699AA43B70F9886350F57021D6DB5E7B8E001ABEFE70C38424; site_str_flag=2; need_modify_name=0; skin=0; theme=0; ggbd=0'
	}
	#------------------------------------自定义函数-------------------------------------
	def webReadFile(self,urlStr,header):
		req = urllib.request.Request(url=urlStr,headers=header)#,headers=header
		html = urllib.request.urlopen(req).read().decode('utf-8')
		#print(Host)
		return html	
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
				"vod_tag": "folder",
				"vod_remarks":''
			})
		res = [i for n, i in enumerate(videos) if i not in videos[:n]]
		videos = res
		return videos