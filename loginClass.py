# -*- coding:utf-8 -*-
# author: guagua
# date:2013.12.1

import urllib
import urllib2
import re
import cookielib
import time

class LoginDouban(object):
	"""docstring for ClassName""" m
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
		self.response = self.opener.open(self.url, urllib.urlencode(self.data))

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

email = raw_input("Email:")
password = raw_input("Password:")
m = LoginDouban(email, password)
m.login_douban()
