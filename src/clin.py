# -*- coding: utf-8 -*-
import sys
import re
import os
import argparse
import getpass

import tpsmate.auth
import tpsmate.core
import tpsmate.config

def auth(username = None, password = None):
    pass

def upload(args):
    print args

def config(args):
    print args

def execute():
    parser = argparse.ArgumentParser(add_help = False)
    parser.add_argument('--username', type = str)
    parser.add_argument('--password', type = str)
    parser.add_argument('--logdir', type = str)
    subparsers = parser.add_subparsers(help = 'upload or config')

    upload_parser = subparsers.add_parser('upload')
    upload_parser.add_argument('file', type = str)
    upload_parser.add_argument('--no-interactive', action = 'store_true')
    upload_parser.add_argument('--no-log', action = 'store_true')
    upload_parser.set_defaults(func = upload)

    config_parser = subparsers.add_parser('config')
    config_parser.add_argument('--encoding', type = str)
    config_parser.set_defaults(func = config)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    execute()
