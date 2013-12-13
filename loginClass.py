# -*- coding:utf-8 -*-
# author: guagua
# date:2013.12.1

import urllib
import urllib2
import re
import cookielib
import time
import random
import threading

class LoginDouban(object):
	"""docstring for ClassName""" 
	def __init__(self, email, password):
		#super(ClassName, self).__init__()
		#self.response = response
		self.url = 'http://www.douban.com/accounts/login'
		#保存cookie
		cookie = cookielib.CookieJar()
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
		#登录post字典参数
		self.data = {
				"form_email":email,
				"form_password":password,
				"source":"index_nav"
		}
		#post headers
		head = {
			"Connection":'keep-alive',
			"HOST":'www.douban.com',
			"Referer":'http://www.baidu.com/',
			"User_Agent":'Mozilla/5.0 (Windows NT 6.1; rv:25.0) Gecko/20100101 Firefox/25.0'
		}

		req = urllib2.Request(self.url)
		#request添加headers
		for  item in head:
			req.add_header(item, head[item])

		self.response = self.opener.open(req, urllib.urlencode(self.data))

	'''登录豆瓣'''
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
		html = self.response.read()
		self.ckcode = re.findall(r'<a href="http://www.douban.com/accounts/logout\?.+ck=(.*?)">', html)

	'''发豆瓣广播'''
	def post_douban(self):
		html = self.response.read()
		ckcode = re.findall(r'<a href="http://www.douban.com/accounts/logout\?.+ck=(.*?)">', html)
		content = raw_input("我说:")
		dic = {
			"ck":ckcode[0],
			"comment":content
		}
		self.response = self.opener.open("http://www.douban.com/?", urllib.urlencode(dic))
		if self.response.geturl() == "http://www.douban.com/":
		    print 'post success !'


	'''小组话题抢沙发'''
	def sofa(self):
		self.response = self.opener.open("http://www.douban.com/group/hangzhou/#topics")
		#可能要，可能不要，看login函数里的ckcode能不能起作用
		#html = self.response.read()
		#self.ckcode = re.findall(r'<a href="http://www.douban.com/accounts/logout\?.+ck=(.*?)">', html)
   		
		topicid_and_count = re.findall(r'topic/(\d+?)/.*?class="">.*?<td nowrap="nowrap" class="">(.*?)</td>', html, re.DOTALL)
		#发帖信息
		replays = ['哦', '呵呵', '@@', '沙发']

		topics = {
			"ck":self.ckcode[0],
			"rv_comment":random.choice(replays),
			"start":"0",
			"submit_btn":"加上去"
		}

		for item in topicid_and_count:
			if item[1] == '':
				self.opener.open("http://www.douban.com/group/topic/" + item[0] + "/add_comment#last?", urllib.urlencode(topics))

	'''发豆油'''
	def send_douyou(self):
		#豆瓣ID为数字，在你的主页能看到
		ID = raw_input("Input your douban ID:")
		self.response = self.opener.open("http://www.douban.com/doumail/write?to=" + ID)
		
		douyou_dic = {
			"ck":self.ckcode[0],
			"m_submit":"好了，寄出去",
			"m_text":"嘿，你好。",
			"to":ID
		}

		self.opener.open("http://www.douban.com/doumail/write?", urllib.urlencode(douyou_dic))


'''
增加多线程模块
'''

class MyThread(threading.Thread):
	def __init__(self, email, password):
		super(MyThread, self).__init__()

	def run():
		m = LoginDouban(self.email, self.password)
		m.login_douban()
		m.send_douyou()


def main():
	email = raw_input("Email:")
	password = raw_input("Password:")
	mt = MyThread(email, password)
	mt.start()
	mt.join()

if __name__ == '__main__':
	main()

# email = raw_input("Email:")
# password = raw_input("Password:")
# m = LoginDouban(email, password)
# m.login_douban()
# #m.post_douban()
# #m.sofa()
# m.send_douyou()