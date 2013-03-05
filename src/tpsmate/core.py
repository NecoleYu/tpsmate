# -*- coding: utf-8 -*-
import os
import sys
import time
import fileinput
import re
import json
import csv
import urllib2

import pyquery
import poster

import auth
import config


TPS_PAGE = 'http://tps.tms.taobao.com/photo/index.htm'
UPLOAD_HOST = 'http://tps.tms.taobao.com'
FILE_ENCODING = ('utf-8','gbk','big5')

class TPSMate():
    def __init__(self,**nargs):
        #super(TPSMate,self).__init__(**nargs)
        inst = auth.Auth(**nargs)
        self.opener = inst.opener

    def upload(self,photo):
        page = self.opener.open(TPS_PAGE)

        selector = pyquery.PyQuery(page.read(), parser = 'html')

        form = selector('#J_UploadForm')
        fields = form.filter('input')
        params =[]

        def params_collection(index, node):
            if node.attr('name') != 'force_opt':
                params.append(poster.encode.MultipartParam(node.attr('name'), node.attr('value')))
            else:
                params.append(poster.encode.MultipartParam('force_opt','1'))

        fields.each(params_collection)
        params.append(poster.encode.MultipartParam('photo',filename=os.path.basename(photo).decode('utf-8','ignore'),fileobj=open(photo,'rb')))

        datagen, headers = poster.encode.multipart_encode(params)
        request = urllib2.Request(UPLOAD_HOST + form.attr('action'), datagen, headers)
        upload_response = urllib2.urlopen(request)

        return json.loads(upload_response.read())

    def batch(self, photos):
        for photo in photos:
            response = self.upload(photo['path'])

            if response.has_key('url'):
                photo.update({
                    'url':response['url'],
                    'filename':response['file_name'],
                })

        return photos

    def parse(self, path):
        chunk = open(path,'rb')
        paths = re.finditer('url\(([a-zA-Z0-7_\-\/]+\.(jpg|png|gif|jpeg))\)|src="([a-zA-Z0-7_\-\/]+\.(jpg|png|gif|jpeg))', chunk.read())
        files = []
        store = []

        chunk.close()

        for path in paths:
            matchgroup = path.group(1) if path.group(1) else path.group(3)
            files.append(matchgroup)


        files = list(set(files))
        for original in files:
            store.append({
                'original':original,
                'path':os.path.join(os.path.dirname(file), original),
            })

        return store

    def generate(self, path, export = None):
        data = self.batch(self.parse(path))

        for line in fileinput.FileInput(path, inplace = 1, backup = '.bak'):
            for enc in FILE_ENCODING:
                try:
                    line = line.decode(enc)
                    for o in data:
                        if o.has_key('url'):
                            line = line.replace('url(' + o['original'] +')','url(' + o['url'] +')') \
                                    .replace('src="' + o['original'] +'"','src="' + o['url'] +'"')

                    sys.stdout.write(line.encode(enc))
                    break
                except Exception:
                    if enc != FILE_ENCODING[-1]:
                        continue

                    sys.exit(1)

        fileinput.close()

        return data

    def csv(self, o, path):
        prefix = 'tpsmate_'
        path = os.path.join(os.path.abspath(path),prefix + time.strftime('%Y%m%d%H%S',time.localtime(time.time())) + '.csv')
        f = open(path,'wb')
        c = csv.writer(f)
        c.writerow(['FileName','Path','URL'])

        for item in o:
            url = item['url'] if item.has_key('url') else ''
            c.writerow([item['filename'],item['path'],url])

        f.close()

        return path 

    def log(self, o):
        for item in o:
            url = item['url'] if item.has_key('url') else ''
            print '%s[%s] = %s' % (item['filename'].decode(config.default_encoding),item['path'].decode(config.default_encoding),url)


#def main():
    #pass
#if __name__ == '__main__':
    #main()
