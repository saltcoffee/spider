# -*- coding:utf-8 -*-
# author: guagua
# date:2013.12.1

import urllib
import urllib2
import re
import cookielib
import time

class LoginDouban(object):
	"""docstring for ClassName""" 
	def __init__(self, email, password):
		#super(ClassName, self).__init__()
		#self.response = response
		self.url = 'http://www.douban.com/accounts/login'
		cookie = cookielib.CookieJar()
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
		self.data = {
				"form_email":email,
				"form_password":password,
				"source":"index_nav"
		}

		head = {
			"Connection":'keep-alive',
			"HOST":'www.douban.com',
			"Referer":'http://www.baidu.com/',
			"User_Agent":'Mozilla/5.0 (Windows NT 6.1; rv:25.0) Gecko/20100101 Firefox/25.0'
		}

		req = urllib2.Request(self.url)


		for  item in head:
			req.add_header(item, head[item])

		self.response = self.opener.open(req, urllib.urlencode(self.data))

	def login_douban(self):
		if self.response.geturl() == self.url:
		    html = self.response.read()

		    regex = re.compile(r'<img id="captcha_image" src="(.+?)" alt="captcha" class="captcha_image"/>')
		    imgurl = regex.findall(html)

		    res = urllib.urlretrieve(imgurl[0], 'gg.jpg')
		    #获取captcha-id参数
		    captcha = re.search('<input type="hidden" name="captcha-id" value="(.+?)"/>' ,html)
		    if captcha:
		        vcode=raw_input('请输入图片上的验证码：')
		        self.data["captcha-solution"] = vcode
		        self.data["captcha-id"] = captcha.group(1)
		        self.data["user_login"] = "登录"
		        #验证码
		        self.response = self.opener.open(self.url, urllib.urlencode(self.data))
		        #登录成功
		        if self.response.geturl() == "http://www.douban.com/":
		            print 'login success !'
	
	def post_douban(self):
		html = self.response.read()
		#print html
		ckcode = re.findall(r'<a href="http://www.douban.com/accounts/logout\?.+ck=(.*?)">', html)
		#print ckcode
		#print type(ckcode[0])
		content = raw_input("我说:")
		dic = {
			"ck":ckcode[0],
			"comment":content
		}

		self.response = self.opener.open("http://www.douban.com/?", urllib.urlencode(dic))
		if self.response.geturl() == "http://www.douban.com/":
		    print 'post success !'

		#print self.response.read()


	'''小组话题抢沙发'''
	def sofa(self):
		self.response = self.opener.open("http://www.douban.com/group/hangzhou/#topics")
		#print repo
		html = self.response.read()
		#print html
		ckcode = re.findall(r'<a href="http://www.douban.com/accounts/logout\?.+ck=(.*?)">', html)
		print ckcode
        
		#regextopicid = re.compile(r'<a class="" title=.+ href="http://www.douban.com/group/topic/(.*?)/">.+</a>')
		#topicid = re.findall(r'<a href="http://www.douban.com/group/topic/(.*?)/" title="[^\"]+" class="">[^<]+</a>', html)
		#print topicid

		#regexnum = re.compile(r'<td nowrap="nowrap" class=""></td>')
		#count = regexnum.findall(html)
		
		topicid_and_count = re.findall(r'<a href="http://www.douban.com/group/topic/(.*?)/" title="[^\"]+" class="">[^<]+</a>[^<]+</td>[^<]+<td nowrap="nowrap"><a href="[^\"]+" class="">[^<]+</a></td>[^<]+<td nowrap="nowrap" class="">(.*?)</td>', html, re.DOTALL)

		# print len(count)
		# print len(topicid)
		#print len(topicid_and_count)
		#print topicid_and_count


		topics = {
			"ck":ckcode[0],
			"rv_comment":"哦。",
			"start":"0",
			"submit_btn":"加上去"
		}

		for item in topicid_and_count:
			if item[1] == '':
				self.opener.open("http://www.douban.com/group/topic/" + item[0] + "/add_comment#last?", urllib.urlencode(topics))

##这里要填写话题的ID			
				            

email = raw_input("Email:")
password = raw_input("Password:")
m = LoginDouban(email, password)
m.login_douban()
#m.post_douban()
#while (True):
m.sofa()
        #time.sleep(10)
