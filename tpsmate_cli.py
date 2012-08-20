# -*- coding: utf-8 -*-
import sys
import re
import os

import tpsmate_help
import tpsmate.core
import tpsmate.config
from getpass import getpass

def parse_login_command_line(args, keys=[], bools=[], alias={}, default={}, help=None):
    common_keys = ['username', 'password', 'cookies']
    common_default = {'cookies': tpsmate.config.DEFAULT_COOKIES, 'username': tpsmate.config.get_config('username'), 'password': tpsmate.config.get_config('password')}
    common_keys.extend(keys)
    common_default.update(default)
    args = parse_command_line(args, common_keys, bools, alias, common_default, help=help)

    if args.password == '-':
        args.password = getpass('Password: ')
    if args.cookies == '-':
        args._args['cookies'] = None
    return args

def login(args):
    args = parse_login_command_line(args, help=tpsmate_help.login)
    if args.cookies == '-':
        args._args['cookies'] = None

    if len(args) < 1:
        args.username = args.username or tpsmate.core.TPSMate(cookie_path=args.cookies, login=False).get_username() or tpsmate.config.get_config('username') or raw_input('username: ')
        args.password = args.password or tpsmate.config.get_config('password') or getpass('password: ')
    elif len(args) == 1:
        args.username = args.username or tpsmate.core.TPSMate(cookie_path=args.cookies, login=False).get_username() or tpsmate.config.get_config('username')
        args.password = args[0]
    if args.password == '-':
        args.password = getpass('password: ')
    elif len(args) == 2:
        args.username, args.password = list(args)
    if args.password == '-':
        args.password = getpass('password: ')
    elif len(args) == 3:
        args.username, args.password, args.cookies = list(args)
    if args.password == '-':
        args.password = getpass('password: ')
    elif len(args) > 3:
        raise RuntimeError('too many arguments')

    if not args.username:
        raise RuntimeError('please input username')

    if args.cookies:
        print 'saving login session to', args.cookies
    else:
        print 'testing login without saving session'

    client = tpsmate.core.TPSMate(args.username, args.password, args.cookies)
    if not client.has_logged():
        print 'login FAILED,MAYBE the username and passwd is NOT correct'

def logout(args):
    args = parse_command_line(args, ['cookies'], default={'cookies': tpsmate.config.DEFAULT_COOKIES}, help=tpsmate_help.logout)

    if len(args):
        raise RuntimeError('too many arguments')

    print 'logging out from', args.cookies
    client = tpsmate.core.TPSMate(cookie_path=args.cookies, login=False)
    client.logout()

def upload(args):
    args = parse_login_command_line(args, ['file', 'dir', 'logdir'], ['interactive','log'], alias={}, default={'interactive':True,'log':True}, help=tpsmate_help.upload)

    if not args.file and not args.dir:
        raise RuntimeError('please select a image or directory')

    client = tpsmate.core.TPSMate(args.username, args.password, args.cookies)
    log_output = []

    if args.dir:
        if os.path.exists(args.dir) and os.path.isdir(args.dir):
            for root,dirs,f in os.walk(args.dir):
                for filepath in f:
                    r = {'path':os.path.join(root,filepath),'filename':os.path.basename(filepath)} 
                    if re.match('.*\.(jpg|png|gif|jpeg)',os.path.basename(filepath)):
                        response = client.upload(os.path.join(root,filepath))
                        if response.has_key('url'):
                            r.update({'url':response['url']})
                        else:
                            pass

                    log_output.append(r)
        else:
            raise RuntimeError('the directory is not exist')

    elif args.file:
        files = args.file.split(',')
        files = list(set(files))

        for f in files:
            r = {'path':os.path.abspath(f),'filename':os.path.basename(f)} 
            if os.path.exists(f) and re.match('.*\.(jpg|png|gif|jpeg)',os.path.basename(f)):
                response = client.upload(f)
                if response.has_key('url'):
                    r.update({'url':response['url']})
                else:
                    pass

            log_output.append(r)

    if args.interactive:
        client.log(log_output)

    args.logdir = args.logdir or tpsmate.config.get_config('logdir') or tpsmate.config.DEFAULT_LOGDIR
    if args.log and args.logdir:
        if os.path.exists(args.logdir) and os.path.isdir(args.logdir):
            client.csv(log_output,args.logdir)
        else:
            raise RuntimeError('can NOT create the log file')

def sheet(args):
    args = parse_login_command_line(args, ['file','logdir'], ['log'], alias={}, default={'log':True}, help=tpsmate_help.upload)

    if not args.file:
        raise RuntimeError('please select a style sheet')

    client = tpsmate.core.TPSMate(args.username, args.password, args.cookies)

    if os.path.exists(args.file) and os.path.isfile(args.file):
        response = client.generate(args.file)
        args.logdir = args.logdir or tpsmate.config.get_config('logdir') or tpsmate.config.DEFAULT_LOGDIR
        if args.log and args.logdir:
            if os.path.exists(args.logdir) and os.path.isdir(args.logdir):
                client.csv(response,args.logdir)
            else:
                raise RuntimeError('can NOT create the log file')
    else:
        raise RuntimeError('can NOT parse the style sheet')

def info(args):
    pass

def config(args):
    args = parse_command_line(args, [], [], help=tpsmate_help.config)

    if len(args) < 1:
        raise RuntimeError('no arguments')

    if args[0] == 'password':
        if len(args) == 1 or args[1] == '-':
            password = getpass('password: ')
        else:
            password = args[1]
        print 'saving password to', tpsmate.config.global_config.path
        tpsmate.config.put_config('password', password)
    else:
        print 'saving configuration to', tpsmate.config.global_config.path
        tpsmate.config.put_config(*args)

def usage(doc=tpsmate_help.usage, message=None):
    if hasattr(doc, '__call__'):
        doc = doc()
    if message:
        print message
    print doc.lstrip()

def help(args):
    if len(args) == 1:
        helper = getattr(tpsmate_help, args[0].lower(), tpsmate_help.help)
        usage(helper)
    elif len(args) == 0:
        print tpsmate_help.welcome
    else:
        print tpsmate_help.help

def execute_command(args=sys.argv[1:]):
    if not args:
        usage()
        sys.exit(1)

    command = args[0]
    if command.startswith('-'):
        if command in ('-h', '--help'):
            usage()
        else:
            usage()
            sys.exit(1)
            sys.exit(0)

    commands = {'login': login, 'logout': logout, 'upload': upload, 'sheet': sheet, 'info': info, 'config': config, 'help': help}

    if command not in commands:
        usage()
        sys.exit(1)

    if '-h' in args or '--help' in args:
        help([command])
    else:
        commands[command](args[1:])

def parse_command_line(args, keys=[], bools=[], alias={}, default={}, help=None):
    options = {}
    for k in keys:
        options[k] = None
    for k in bools:
        options[k] = None

    left = []
    args = args[:]
    while args:
        x = args.pop(0)
        if x == '--':
            left.extend(args)
            break
        if x.startswith('-'):
            k = x.lstrip('-')
            if k in bools:
                options[k] = True
            elif k.startswith('no-') and k[3:] in bools:
                options[k[3:]] = False
            elif k in keys:
                options[k] = args.pop(0)
            elif '=' in k and k[:k.index('=')] in keys:
                options[k[:k.index('=')]] = k[k.index('=')+1:]
            elif k in alias:
                k = alias[k]
                if k in bools:
                    options[k] = True
                else:
                    options[k] = args.pop(0)
            else:
                if help:
                    print 'Unknown option ' + x
                    print
                    print help
                    exit(1)
                else:
                    raise RuntimeError('Unknown option '+x)
        else:
            left.append(x)

    for k in default:
        if options[k] is None:
            options[k] = default[k]

    class Args(object):
        def __init__(self, args, left):
            self.__dict__['_args'] = args
            self.__dict__['_left'] = left
        def __getattr__(self, k):
            v = self._args.get(k, None)
            if v:
                return v
            if '_' in k:
                return self._args.get(k.replace('_', '-'), None)
        def __setattr__(self, k, v):
            self._args[k] = v
        def __getitem__(self, i):
            if type(i) == int:
                return self._left[i]
            else:
                return self._args[i]
        def __setitem__(self, i, v):
            if type(i) == int:
                self._left[i] = v
            else:
                self._args[i] = v
        def __len__(self):
            return len(self._left)
        def __str__(self):
            return '<Args%s%s>' % (self._args, self._left)
    return Args(options, left)

if __name__ == '__main__':
    execute_command()
