#coding=utf-8
#!/usr/bin/python
import sys
sys.path.append('..') 
from base.spider import Spider
import json
import os
import base64
import re
from urllib import request, parse
import urllib
import urllib.request
import glob

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

	def homeContent(self, filter):
		result = {}
		cateManual = {
		      "🐉神族九帝":"https://alist.shenzjd.com",
		      "☃百度网盘":"baidu"
		}
		classes = []
		for k in cateManual:
		    classes.append({
		        'type_name': k,
				"type_flag": "1",
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

	ver = ''
	baseurl = ''
	def getVersion(self, gtid):
		param = {
		    "path": '/'
		}
		if gtid.count('/') == 2:
		    gtid = gtid + '/'
		baseurl = re.findall(r"http.*://.*?/", gtid)[0]
		ver = self.fetch(baseurl + 'api/public/settings', param)
		vjo = json.loads(ver.text)['data']
		if type(vjo) is dict:
		    ver = 3
		else:
		    ver = 2
		self.ver = ver
		self.baseurl = baseurl

	def categoryContent(self, tid, pg, filter, extend):
		result = {}
		videos=[]
		if tid.count('https:')<1:
			Path="/" if tid.find('baidu')>-1 else tid
			videos=self.custom_getBaidu(cataloguePath=Path)
		else:
		    videos=self.custom_getAlist(tid=tid)
		result['list'] = videos
		result['page'] = 1
		result['pagecount'] = 1
		result['limit'] = 999
		result['total'] = 999999
		return result

	def detailContent(self, array):
		id = array[0]
		vod=[]
		if id.find('baidu')<0:
			vod=self.custom_getPlay(id=id)
		else:
			vod=self.custom_getBaiduPlay(id=id)
		result = {
		    'list': [
		        vod
		    ]
		}
		return result

	def searchContent(self, key, quick):
		result = {
		    'list': []
		}
		return result

	def playerContent(self, flag, id, vipFlags):
		result = {}
		if flag!='百度网盘':
			result=self.custom_playerContent(id=id)
		else:
			result["parse"] = 1
			result["playUrl"] =""
			result["url"] = 'https://pan.baidu.com/play/video#/video?path=%2F%E5%A4%AA%E7%A9%BA%E4%B9%8B%E6%97%85(VR).mp4&theme=light&from=home&from=pfile'
			result["header"] = self.header
		return result

	config = {
		"player": {},
		"filter": {}
	}
	header = {
		"User-Agent":"Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36",
		"Host": "pan.baidu.com",
		"Referer": "https://pan.baidu.com/",
		"Cookie":"PSTM=1604824989; BIDUPSID=242A986F336B8BBFE138636E5294994A; H_WISE_SIDS_BFESS=110085_127969_179348_184716_189755_190616_191068_191249_192913_194085_194511_194519_194529_195342_196425_197242_197711_197948_197957_198265_199569_200596_200960_200993_201193_201699_202910_203190_203267_203310_203361_203504_204254_204264_204305_204535_204545_204701_204778_204864_204914_205218_205220_205241_205484_205569_205909_206007_206124_206168_206515_206681_206729_206804_206897_206911_207234_207364_207471_207488_207565_207671_207713_207716_207768_207831_207863_207893_207923_208050_208055_208061_208137_208165_208224_208226_208268_208270_208312_208344_208564_208687_208721_208755_208771_208890_209231; BDUSS=nVKWHN1VWthOFpqQXh5Z2J1MHhKVXJQZmptdlAzR3F3d0pHb3d5UTBadEN5MzVqRVFBQUFBJCQAAAAAAQAAAAEAAADbPqk20P7KpdfTMjIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEI-V2NCPldja; BDUSS_BFESS=nVKWHN1VWthOFpqQXh5Z2J1MHhKVXJQZmptdlAzR3F3d0pHb3d5UTBadEN5MzVqRVFBQUFBJCQAAAAAAQAAAAEAAADbPqk20P7KpdfTMjIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEI-V2NCPldja; BAIDUID=19C93899D50089D40967632F72585F67:FG=1; PANWEB=1; BAIDUID_BFESS=19C93899D50089D40967632F72585F67:FG=1; BAIDU_WISE_UID=wapp_1690174987606_165; ZFY=Pb1LsyQ67lTuPaUlz3fY:Aaa9laL:APWj07kMlDgSUAFI:C; csrfToken=g8Inve3QH9GHm6jRG3C9XMSH; STOKEN=2fff6cb0e330e38b04e90169ad03363f2af7f6c38a4b18e6da076728669352c8; Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0=1691129967; Hm_lpvt_7a3960b6f067eb0085b7f96ff5e660b0=1691129967; ab_sr=1.0.1_NjUyODdmYzcyZjk0MzZkNTk2ZGQzNThiMzQxNzM3M2I0NGIxMzNmYmQ1YTFiZDllMjg4ZWMyYjhlODhlNjk5N2NkODQ4ZjZkOTIyZjE1YjRiNTE4Mzg0ZWRkNjAzMjg4OTViZjBlMjI2YTgxZGY5OWYzYTMwZjU5ZDEwMjQ5NmE0N2IwNjU5NWMxY2Q2MTBhMmFmZTgzNzIyNTc5ZTUyZDE5YjE2YzllZTU5MzdiM2I3NzFmNDVlMmE1ZjY2Mzk5; PANPSC=8165459457226291555%3AKkwrx6t0uHBS3vas06GEmOL8WewRDWDPZiRMv5L2Uee%2Bp0%2F6razUKuQ4siUfSkANz81ttRoL0tBKQ4Dasb9%2FZstxnmHe8mH%2FVO0c7TtdgDSlxHihS2mgCRrA%2F7VXeEuWLvxjdeGWe14xHgLtt4aYIueFh%2BdfonnAY8uG8AM%2BY0Ih6uZoP3DwQ3ePlzJEAU4t4oRCM5jrTJ0BDChpkEtqiw%3D%3D; AB_EXPERIMENT=%7B%22PC_SESSION_COOKIE_SWITCH%22%3A%22ON%22%2C%22group_cloud_smallflow%22%3A%22%22%2C%22ORDER_SIX_MONTH_CHECK%22%3A%22ON%22%2C%22group_smallflow%22%3A%22off%22%2C%22CHROME80_SET_COOKIE%22%3A%22ON%22%2C%22group_smallflow_uri%22%3A%22%22%2C%22rccGetChannelInfoSink%22%3A%22ON%22%7D"
	}

	def localProxy(self, param):
		return [200, "video/MP2T", action, ""]
	#------------------------------------自定义函数-------------------------------------
	def custom_webReadFile(self,urlStr,header):
		req = urllib.request.Request(url=urlStr,headers=header)#,headers=header
		html = urllib.request.urlopen(req).read().decode('utf-8')
		#print(Host)
		return html	
	def get_RegexGetText(self,Text,RegexText,Index):
		returnTxt=""
		Regex=re.search(RegexText, Text, re.M|re.S)
		if Regex is None:
			returnTxt=""
		else:
			returnTxt=Regex.group(Index)
		return returnTxt	
	def custom_getAlist(self, tid):
		if tid.count('/') == 2:
			tid = tid + '/'
		nurl = re.findall(r"http.*://.*?/", tid)[0]
		if self.ver == '' or self.baseurl != nurl:
			self.getVersion(tid)
		ver = self.ver
		baseurl = self.baseurl
		if tid.count('/') == 2:
		    tid = tid + '/'
		pat = tid.replace(baseurl,"")
		param = {
		    "path": '/' + pat
		}
		if ver == 2:
		    rsp = self.postJson(baseurl + 'api/public/path', param)
		    jo = json.loads(rsp.text)
		    vodList = jo['data']['files']
		elif ver == 3:
		    rsp = self.postJson(baseurl + 'api/fs/list', param)
		    jo = json.loads(rsp.text)
		    vodList = jo['data']['content']
		videos = []
		for vod in vodList:
		    if ver == 2:
		        img = vod['thumbnail']
		    elif ver == 3:
		        img = vod['thumb']
		    if len(img) == 0:
		        if vod['type'] == 1:
		            img = "http://img1.3png.com/281e284a670865a71d91515866552b5f172b.png"
		    if pat != '':
		        aid = pat + '/'
		    else:
		        aid = pat
		    if vod['type'] == 1:
		        tag = "folder"
		        remark = "文件夹"
		    else:
		        size = vod['size']
		        if size > 1024 * 1024 * 1024 * 1024.0:
		            fs = "TB"
		            sz = round(size / (1024 * 1024 * 1024 * 1024.0), 2)
		        elif size > 1024 * 1024 * 1024.0:
		            fs = "GB"
		            sz = round(size / (1024 * 1024 * 1024.0), 2)
		        elif size > 1024 * 1024.0:
		            fs = "MB"
		            sz = round(size / (1024 * 1024.0), 2)
		        elif size > 1024.0:
		            fs = "KB"
		            sz = round(size / (1024.0), 2)
		        else:
		            fs = "KB"
		            sz = round(size / (1024.0), 2)
		        tag = "file"
		        remark = str(sz) + fs
		    aid = baseurl + aid + vod['name']
		    videos.append({
		        "vod_id":  aid,
		        "vod_name": vod['name'],
		        "vod_pic": img,
		        "vod_tag": tag,
		        "vod_remarks": remark
		    })
		return videos
	def custom_getBaidu(self,cataloguePath):
		CometURL=urllib.parse.quote(cataloguePath)
		urlString = "https://pan.baidu.com/api/list?order=time&desc=1&showempty=0&web=1&page=1&num=100&dir=路径&t=0.5938627068731255&channel=chunlei&web=1&app_id=250528&bdstoken=27a95f9978ba628abcfaf87afb775f80&logid=MkQwNDREOEMyODE5RDRGN0UxNzQ3MTIxQThCQzQ3MkM6Rkc9MQ==&clienttype=0"
		url=urlString.replace('路径',CometURL)
		self.header['Referer']=url
		html=self.custom_webReadFile(urlStr=url,header=self.header)
		jRoot=json.loads(html)
		if jRoot['errno']=='0':
			return []
		videos=[]
		tid='baidu'
		listCollection=jRoot['list']
		for vod in listCollection:
			name=vod['server_filename']
			size=vod['size']
			if int(size)>0:
				remark=self.custom_calculationSize(sizeValue=size)
				tag='file'
				tid='baidu'
				img='https://img0.baidu.com/it/u=2963924144,3361713742&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=500'
			else:
				remark='文件夹'
				tid=''
				tag='folder'
				img='http://img1.3png.com/281e284a670865a71d91515866552b5f172b.png'
			aid=vod['path']
			videos.append({
		        "vod_id":  tid+aid,
		        "vod_name": name,
		        "vod_pic": img,
		        "vod_tag": tag,
		        "vod_remarks": remark
		    })
		return videos
	def custom_calculationSize(self,sizeValue):
		if sizeValue > 1024 * 1024 * 1024 * 1024.0:
			fs = "TB"
			sz = round(sizeValue / (1024 * 1024 * 1024 * 1024.0), 2)
		elif sizeValue > 1024 * 1024 * 1024.0:
			fs = "GB"
			sz = round(sizeValue / (1024 * 1024 * 1024.0), 2)
		elif sizeValue > 1024 * 1024.0:
			fs = "MB"
			sz = round(sizeValue / (1024 * 1024.0), 2)
		elif sizeValue > 1024.0:
			fs = "KB"
			sz = round(sizeValue / (1024.0), 2)
		else:
			fs = "KB"
			sz = round(sizeValue / (1024.0), 2)
		remark = str(sz) + fs
		return remark
	def custom_getPlay(self,id):
		if self.ver == '' or self.baseurl == '':
		    self.getVersion(id)
		ver = self.ver
		baseurl = self.baseurl
		fileName = id.replace(baseurl, "")
		dir = re.findall(r"(.*)/", fileName)[0].replace(baseurl, "")
		dirparam = {
		    "path": '/' + dir,
		    "password": "",
		    "page_num": 1,
		    "page_size": 100
		}
		vod = {
		    "vod_id": fileName,
		    "vod_name": dir,
		    "vod_pic": '',
		    "vod_tag": '',
		    "vod_play_from": "播放",
		}
		if ver == 2:
		    drsp = self.postJson(baseurl + 'api/public/path', dirparam)
		    djo = json.loads(drsp.text)
		    dList = djo['data']['files']
		elif ver == 3:
		    drsp = self.postJson(baseurl + 'api/fs/list', dirparam)
		    djo = json.loads(drsp.text)
		    dList = djo['data']['content']
		playUrl = ''
		for tempd in dList:
		    if 'mp4' in tempd['name'] or 'mkv' in tempd['name'] or 'TS' in tempd['name'] or 'flv' in tempd['name'] or 'rmvb' in tempd['name'] or 'mp3' in tempd['name'] or 'flac' in tempd['name'] or 'wav' in tempd['name']:
		    # 开始匹配视频
		        # 视频名称 name
		        name = tempd['name']
		        # 视频链接 url
		        fname = re.findall(r"(.*)/", fileName)[0] + '/' + name
		        url = baseurl + fname
		        # 开始找字幕 subt
		        vname = re.findall(r"(.*)\.", tempd['name'])[0]
		        vstr = re.findall(r"\'name\': \'(.*?)\'", str(dList))
		        if len(vstr) == 2:
		            suball = vstr
		        else:
		            suball = difflib.get_close_matches(vname, vstr, len(dList), cutoff=0.8)
		        for sub in suball:
		            if sub.endswith(".ass") or sub.endswith(".srt"):
		                subt = '@@@' + baseurl + dir + '/' +sub
		        ifsubt = 'subt' in locals().keys()
		        if ifsubt is False:
		            playUrl = playUrl + '{0}${1}#'.format(name, url)
		        else:
		            playUrl = playUrl + '{0}${1}{2}#'.format(name, url, subt)
		vod['vod_play_url'] = playUrl
		return vod
	def custom_getBaiduPlay(self,id):
		id=id[5:]
		url=urllib.parse.quote(id,safe='')
		url='https://pan.baidu.com/play/video#/video?path={0}&t=-1'.format(url)
		# superiorUrl='/' if id.rfind('/')==0 else id[0:id.rfind('/')]
		fileName=id[id.rfind('/')+1:]
		vod = {
		    "vod_id": id,
		    "vod_name": fileName,
		    "vod_pic": '',
		    "vod_tag": '',
		    "vod_play_from": "百度网盘",
		}
		vod['vod_play_url'] = url
		return vod
	def custom_playerContent(self,id):
		result = {}
		ifsub = '@@@' in id
		if ifsub is True:
		    ids = id.split('@@@')
		    if self.ver == '' or self.baseurl == '':
		        self.getVersion(ids[1])
		    ver = self.ver
		    baseurl = self.baseurl
		    fileName = ids[1].replace(baseurl, "")
		    vfileName = ids[0].replace(baseurl, "")
		    param = {
		        "path": '/' + fileName,
		        "password": "",
		        "page_num": 1,
		        "page_size": 100
		    }
		    vparam = {
		        "path": '/' + vfileName,
		        "password": "",
		        "page_num": 1,
		        "page_size": 100
		    }
		    if ver == 2:
		        rsp = self.postJson(baseurl + 'api/public/path', param)
		        jo = json.loads(rsp.text)
		        vodList = jo['data']['files'][0]
		        subturl = vodList['url']
		        vrsp = self.postJson(baseurl + 'api/public/path', vparam)
		        vjo = json.loads(vrsp.text)
		        vList = vjo['data']['files'][0]
		        url = vList['url']
		    elif ver == 3:
		        rsp = self.postJson(baseurl + 'api/fs/get', param)
		        jo = json.loads(rsp.text)
		        vodList = jo['data']
		        subturl = vodList['raw_url']
		        vrsp = self.postJson(baseurl + 'api/fs/get', vparam)
		        vjo = json.loads(vrsp.text)
		        vList = vjo['data']
		        url = vList['raw_url']
		    if subturl.startswith('http') is False:
		        head = re.findall(r"h.*?:", baseurl)[0]
		        subturl = head + subturl
		    if url.startswith('http') is False:
		        head = re.findall(r"h.*?:", baseurl)[0]
		        url = head + url
		    urlfileName = urllib.parse.quote(fileName)
		    subturl = subturl.replace(fileName, urlfileName)
		    urlvfileName = urllib.parse.quote(vfileName)
		    url = url.replace(vfileName, urlvfileName)
		    result['subt'] = subturl
		else:
		    if self.ver == '' or self.baseurl == '':
		        self.getVersion(id)
		    ver = self.ver
		    baseurl = self.baseurl
		    vfileName = id.replace(baseurl, "")
		    vparam = {
		        "path": '/' + vfileName,
		        "password": "",
		        "page_num": 1,
		        "page_size": 100
		    }
		    if ver == 2:
		        vrsp = self.postJson(baseurl + 'api/public/path', vparam)
		        vjo = json.loads(vrsp.text)
		        vList = vjo['data']['files'][0]
		        url = vList['url']
		    elif ver == 3:
		        vrsp = self.postJson(baseurl + 'api/fs/get', vparam)
		        vjo = json.loads(vrsp.text)
		        vList = vjo['data']
		        url = vList['raw_url']
		    if url.startswith('http') is False:
		        head = re.findall(r"h.*?:", baseurl)[0]
		        url = head + url
		    urlvfileName = urllib.parse.quote(vfileName)
		    url = url.replace(vfileName, urlvfileName)
		result["parse"] = 0
		result["playUrl"] = ''
		result["url"] = url
		result["header"] = {
		    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
		}
		return result