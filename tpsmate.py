# -*- coding: utf-8 -*-
import os
import sys
import time
import fileinput
import re
import json
import csv
import urllib
import urllib2
import cookielib
from bs4 import BeautifulSoup 
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import tpsmate_config


LOGIN_PAGE = 'http://login.taobao.com/member/login.jhtml'
TPS_PAGE = 'http://tps.tms.taobao.com/photo/index.htm'
UPLOAD_HOST = 'http://tps.tms.taobao.com'
FILE_ENCODING = ('utf-8','gbk','big5')

class TPSMate(object):
    def __init__(self, username=None, password=None, cookie_path=None, login=True):
        self.cookie_path = cookie_path

        if cookie_path:
            self.cookiejar = cookielib.MozillaCookieJar()
            if os.path.exists(cookie_path):
                self.load_cookies()
            else:
                self.cookiejar = cookielib.MozillaCookieJar()

        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookiejar))

        if not self.has_logged() and login:
            if username:
                username = username.decode(default_encoding).encode('utf-8')
            else:
                if self.has_cookie('.taobao.com', 'tracknick'):
                    username = self.get_username()
                else: 
                    username = tpsmate_config.get_config('username')
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

    def upload(self,photo):
        page = self.opener.open(TPS_PAGE)
        soup = BeautifulSoup(page.read())
        form = soup.find(id="J_UploadForm")
        upload_url = form['action']

        upload_data = {}
        fields = form.find_all('input')
        for field in fields:
            upload_data[field['name']] = field['value']

        upload_data.update({
            'filename':os.path.basename(photo),
            'photo':open(photo,'rb'),
            'force_opt':'1',
        })

        opener = register_openers()
        opener.add_handler(urllib2.HTTPCookieProcessor(self.cookiejar))
        datagen, headers = multipart_encode(upload_data)
        request = urllib2.Request(UPLOAD_HOST + upload_url, datagen, headers)
        upload_response = urllib2.urlopen(request)

        return json.loads(upload_response.read())

    def _batch(self,photos):
        for photo in photos:
            response = self.upload(photo['path'])

            if response.has_key('url'):
                photo.update({
                    'url':response['url'],
                    'filename':response['file_name'],
                })

        return photos

    def parse_css(self,sheet):
        chunk = open(sheet,'rb')
        paths = re.finditer('url\(([a-zA-Z0-7_\-\/]+\.(jpg|png|gif))\)',chunk.read())
        files = []
        store = []

        chunk.close()

        for path in paths:
            if re.match('^http:\/\/',path.group(1)) is None:
                files.append(path.group(1))

        files = list(set(files))
        for original in files:
            store.append({
                'original':original,
                'path':os.path.join(os.path.dirname(sheet),original),
            })

        return store

    def generate(self,sheet):
        data = self.parse_css(sheet)
        self._batch(data)

        for line in fileinput.FileInput(sheet, inplace=1):
            for enc in FILE_ENCODING:
                try:
                    line = line.decode(enc)
                    for o in data:
                        if o.has_key('url'):
                            line = line.replace('url(' + o['original'] +')','url(' + o['url'] +')')
                    sys.stdout.write(line.encode(enc))

                    break
                except Exception:
                    if enc == FILE_ENCODING[-1]:
                        sys.exit(1)
                    continue

        fileinput.close()

        return data

    def csv(self, o, path):
        f = open(os.path.join(os.path.abspath(path),time.strftime('%Y%m%d%H%S',time.localtime(time.time())) + '.csv'),'wb')
        c = csv.writer(f)
        c.writerow(['FileName','Path','URL'])

        for item in o:
            url = item['url'] if item.has_key('url') else ''
            c.writerow([item['filename'],item['path'],url])

        f.close()

default_encoding = tpsmate_config.get_config('encoding', sys.getfilesystemencoding())
if default_encoding is None or default_encoding.lower() == 'ascii':
	default_encoding = 'utf-8'

#def main():
    #pass
#if __name__ == '__main__':
    #main()
