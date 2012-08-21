# -*- coding: utf-8 -*-
import os
import sys
import urllib
import urllib2
import cookielib
import poster
import config

LOGIN_PAGE = 'http://login.taobao.com/member/login.jhtml'

class Auth(object):
    def __init__(self, username=None, password=None, cookie_path=None, login=True):
        self.cookie_path = cookie_path

        if cookie_path:
            self.cookiejar = cookielib.MozillaCookieJar()
            if os.path.exists(cookie_path):
                self.load_cookies()
            else:
                self.cookiejar = cookielib.MozillaCookieJar()

        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookiejar))
        self.uploader = poster.streaminghttp.register_openers()
        self.uploader.add_handler(urllib2.HTTPCookieProcessor(self.cookiejar))

        if not self.has_logged() and login:
            if username:
                username = username.decode(default_encoding).encode('utf-8')
            else:
                if self.has_cookie('.taobao.com', 'tracknick'):
                    username = self.get_username()
                else: 
                    username = config.get_config('username')
            if not password:
                raise NotImplementedError('user is not logged in')

            self.login(username, password)

    def login(self, username, password):
        login_data = urllib.urlencode({
            'TPL_username':username.decode('utf-8').encode('gbk'),
            'TPL_password':password,
        })
        self.opener.open(LOGIN_PAGE, login_data)
        self.save_cookies()

    def logout(self):
        if self.cookie_path:
            self.cookiejar.clear()
            self.save_cookies()

    def has_logged(self):
		return self.get_cookie('.taobao.com', '_l_g_') and self.get_username()

    def load_cookies(self):
        self.cookiejar.load(self.cookie_path, ignore_discard=True, ignore_expires=True)

    def save_cookies(self):
        if self.cookie_path:
            self.cookiejar.save(self.cookie_path, ignore_discard=True)

    def get_cookie(self, domain, k):
        if self.has_cookie(domain, k):
            return self.cookiejar._cookies[domain]['/'][k].value

    def has_cookie(self, domain, k):
        return domain in self.cookiejar._cookies and k in self.cookiejar._cookies[domain]['/']

    def get_username(self):
        return self.get_cookie('.taobao.com', 'tracknick')

default_encoding = config.get_config('encoding', sys.getfilesystemencoding())
if default_encoding is None or default_encoding.lower() == 'ascii':
	default_encoding = 'utf-8'
