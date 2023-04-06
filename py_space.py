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
			"B站直播":"B"
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
		Url='http://my.ie.2345.com/onlinefav/web/getAllData?action=getData&id=21492773&s=&d=Fri%20Mar%2003%202023%2008:45:08%20GMT+0800%20(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)'
		headers1=self.header
		if tid=='B':
			ts=str(int(time.time())*1000)
			Url='https://api.live.bilibili.com/xlive/web-ucenter/v1/xfetter/GetWebList?page=1&page_size=10&_='+ts
			headers1= {
				"Referer": 'https://www.bilibili.com/',
				'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
				'Host': 'api.live.bilibili.com',
				'cookie':'LIVE_BUVID=AUTO2616462757465937; fingerprint=77c85d9ff313891ec90a199813ae4113; CURRENT_QUALITY=64; CURRENT_BLACKGAP=1; blackside_state=0; fingerprint3=b9d652f66e003973ba5e01bdfd8721f7; hit-dyn-v2=1; b_ut=5; nostalgia_conf=-1; rpdid=|(u))ul)ukR~0JuYYmkl~kRu; i-wanna-go-back=-1; buvid_fp_plain=undefined; buvid_fp=77c85d9ff313891ec90a199813ae4113; buvid3=3693BDBE-2B47-E988-B3C2-204329BE615328103infoc; b_nut=1677837728; _uuid=6CC54C6D-2FAF-4DDC-B2B3-77468A910363B36562infoc; bp_video_offset_671023938=779182113663483900; SESSDATA=33fcc227%2C1695808020%2C713b2%2A31; bili_jct=f6d2e39f6a74593ef4e02e6bf206351b; DedeUserID=321534564; DedeUserID__ckMd5=4cf4212075f2f1eb; bp_video_offset_321534564=779812314217971800; CURRENT_FNVAL=4048; bp_t_offset_321534564=780280852185612341; buvid4=2E8D615F-F1D9-B7AD-63C2-1C9A145C98D117909-022030512-5ZCNRwNsIx1ENAcLMkU%2FQg%3D%3D; hit-new-style-dyn=1; b_lsid=C91089B16_18754630CC9'
			}
		rsp = self.fetch(Url,headers=headers1)
		if tid=='B':
			videos=self.get_list_B(jsonTxt=rsp.text)
		else:
			videos = self.get_list(html=rsp.text)
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
		logo = aid[2]
		url = aid[1]
		title = aid[0]
		vodItems=[]
		vod_play_from='线路'
		if url.find('http')<0:
			vodItems = [title+"$"+url]
		else:
			Url='https://api.live.bilibili.com/xlive/web-room/v2/index/getRoomPlayInfo?room_id={0}&no_playurl=0&mask=1&qn=0&platform=web&protocol=0,1&format=0,2&codec=0,1'.format(url)
			headers1= {
				"Referer": 'https://www.bilibili.com/',
				'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
				'Host': 'api.live.bilibili.com',
				'cookie':'LIVE_BUVID=AUTO2616462757465937; fingerprint=77c85d9ff313891ec90a199813ae4113; CURRENT_QUALITY=64; CURRENT_BLACKGAP=1; blackside_state=0; fingerprint3=b9d652f66e003973ba5e01bdfd8721f7; hit-dyn-v2=1; b_ut=5; nostalgia_conf=-1; rpdid=|(u))ul)ukR~0JuYYmkl~kRu; i-wanna-go-back=-1; buvid_fp_plain=undefined; buvid_fp=77c85d9ff313891ec90a199813ae4113; buvid3=3693BDBE-2B47-E988-B3C2-204329BE615328103infoc; b_nut=1677837728; _uuid=6CC54C6D-2FAF-4DDC-B2B3-77468A910363B36562infoc; bp_video_offset_671023938=779182113663483900; SESSDATA=33fcc227%2C1695808020%2C713b2%2A31; bili_jct=f6d2e39f6a74593ef4e02e6bf206351b; DedeUserID=321534564; DedeUserID__ckMd5=4cf4212075f2f1eb; bp_video_offset_321534564=779812314217971800; CURRENT_FNVAL=4048; bp_t_offset_321534564=780280852185612341; buvid4=2E8D615F-F1D9-B7AD-63C2-1C9A145C98D117909-022030512-5ZCNRwNsIx1ENAcLMkU%2FQg%3D%3D; hit-new-style-dyn=1; b_lsid=C91089B16_18754630CC9'
			}
			rsp = self.fetch(Url,headers=headers1)
			vodItems=self.get_m3u8Url_B(jsonTxt=rsp.text)
			vod_play_from='直播'
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
		vod['vod_play_from'] = vod_play_from
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
		headers = {
			'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'
		}
		jx=self.ifJx(urlTxt=id)
		parse=1
		if flag=='直播':
			parse=0
			jx=0
		result["parse"] = parse
		result["playUrl"] = ''
		result["url"] = id
		result['jx'] = jx#VIP解析
		result["header"] = headers	
		return result
	def ifJx(self,urlTxt):
		Isjiexi=0
		RegexTxt=r'(youku.com|v.qq|bilibili|iqiyi.com|xigua.com)'
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
				url=x['host']+x['Url'].replace("?","")
				title=descMass.get(x['qn'])+"["+x['format_name'].replace("fmp4","m3u8")+"]"
				videos.append(title+"$"+url)
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