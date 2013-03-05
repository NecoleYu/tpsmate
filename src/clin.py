# -*- coding: utf-8 -*-
import sys
import re
import os
import argparse
import getpass

import tpsmate.auth
import tpsmate.core
import tpsmate.config

COOKIE_PATH  = tpsmate.config.DEFAULT_COOKIES

def authorize(username = None, password = None):
    username = username if username is not None else tpsmate.config.get_config('username')
    password = password if password is not None else tpsmate.config.get_config('password')

    if not username or not password:
        cookies = tpsmate.auth.Auth(cookie_path = COOKIE_PATH, login = False)
        if cookies.has_logged():
            return True
        else:
            username = raw_input('username: ')
            password = getpass.getpass('password: ')
            return authorize(username, password)
    else:
        try:
            cookies = tpsmate.auth.Auth(username = username, password = password, cookie_path = COOKIE_PATH, login = True)
            return cookies.has_logged()
        except Exception, e:
            print e
            return False 

def upload(args):
    is_authorized = authorize(args.username, args.password)
    sources = args.sources 
    export = args.export

    if not is_authorized:
        return

    client = tpsmate.core.TPSMate(username = args.username, password = args.password, cookie_path = COOKIE_PATH, login = True)
    log_output = []

    for source in sources:
        if os.path.isfile(source):
            if os.path.exists(source):
                r = upload_skel(source)
                log_output.append(r)

        elif os.path.isdir(source):
            if os.path.exists(source):
                for root,dirs,f in os.walk(source):
                    for filepath in f:
                        r = upload_skel(os.path.join(root, filepath))
                        log_output.append(r)
        else:
            pass

def upload_skel(client, source, export = None):
    ret = None

    if re.match('.*\.(jpg|png|gif|jpeg)$',os.path.basename(source)):
        ret = {'path':os.path.abspath(source),'filename':os.path.basename(source)} 
        response = client.upload(source)
        if response.has_key('url'):
            ret.update({'url':response['url']})
    elif re.match('.*\.(css|less|sass|scss|styl)$',os.path.basename(source)):
        response = client.generate(source)

def config(args):
    print args

def login(args):
    print args

def execute():
    parser = argparse.ArgumentParser(add_help = False)
    parser.add_argument('--username', type = str)
    parser.add_argument('--password', type = str)
    subparsers = parser.add_subparsers(help = 'upload or config')

    upload_parser = subparsers.add_parser('upload')
    upload_parser.add_argument('sources', nargs='+')
    upload_parser.add_argument('--no-interactive', action = 'store_true')
    upload_parser.add_argument('--no-log', action = 'store_true')
    upload_parser.add_argument('--logdir', type = str)
    upload_parser.set_defaults(func = upload)

    config_parser = subparsers.add_parser('config')
    config_parser.add_argument('--logdir', type = str)
    config_parser.add_argument('--encoding', type = str)
    config_parser.set_defaults(func = config)

    config_parser = subparsers.add_parser('login')
    config_parser.set_defaults(func = login)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    execute()
