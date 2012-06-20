# -*- coding: utf-8 -*-
import sys
import os

basic_usage = '''python tpsmate_cli.py <command> [<args>]

Basic commands
 help       get the help 
 login      login tps with taobao account
 upload     upload single picture or dir to tps 
 sheet      upload all image for background-image rule in the style sheet to tps
 config     set username,password,logdir and encoding etc 
 logout     logout from tps 

'''

def usage():
	return basic_usage + '''

Use 'python tpsmate_cli.py help' for details.
Use 'python tpsmate_cli.py help <command>' for more information on a specific command. 

'''

help = '''Get helps:
  python tpsmate_cli.py help help
  python tpsmate_cli.py help examples
  python tpsmate_cli.py help readme
  python tpsmate_cli.py help <command>

'''


welcome = '''TPSMate(Taobao Photo System Mate) Command Line Version.

Basic usage:
''' + basic_usage + '\n' + help

def examples():
	return '''python tpsmate_cli.py login "username" "password"
python tpsmate_cli.py login "password"
python tpsmate_cli.py login

python tpsmate_cli.py config username "username"
python tpsmate_cli.py config password "password"
python tpsmate_cli.py config encoding "utf-8,gbk"
python tpsmate_cli.py config logdir "/path/to/save/csv/log/"

python tpsmate_cli.py upload --file "/path/to/image.jpg"
python tpsmate_cli.py upload --file "/path/to/image.jpg" --no-interactive
python tpsmate_cli.py upload --file "/path/to/image.jpg" --no-log
python tpsmate_cli.py upload --file "/path/to/image.jpg,/path/to/another/image.png"
python tpsmate_cli.py upload --dir "/path/to/image/directory"
python tpsmate_cli.py upload --dir "/path/to/image/directory" --logdir "/path/to/save/csv/log/"

python tpsmate_cli.py sheet --file "/path/to/sheet.css"
python tpsmate_cli.py sheet --file "/path/to/sheet.css" --logdir "/path/to/save/csv/log/"

python tpsmate_cli.py logout

'''

def readme():
	doc = os.path.join(sys.path[0], 'README.md')
	with open(doc) as txt:
		return txt.read().decode('utf-8')


login  = '''python tpsmate_cli.py login <username> <password>

login TPS

Examples:
 python tpsmate_cli.py login "username" "password"
 python tpsmate_cli.py login "password"
 python tpsmate_cli.py login

'''

upload = '''python tpsmate_cli.py upload [options] [file|directory|csv]

upload image to tps 

Options:
 --file=[file]           upload image to tps,multiple file supported.
 --dir=[directory]       upload all images in the directory.
 --logdir=[csv]          save the log to a csv file.
 --no-interactive        NOT print upload info in the terminal
 --no-log                NOT export log to a csv file 

Examples:
 python tpsmate_cli.py upload --file "/path/to/image.jpg"
 python tpsmate_cli.py upload --file "/path/to/image.jpg" --no-interactive
 python tpsmate_cli.py upload --file "/path/to/image.jpg,/path/to/another/image.png"
 python tpsmate_cli.py upload --dir "/path/to/image/directory"
 python tpsmate_cli.py upload --dir "/path/to/image/directory" --logdir "/path/to/save/csv/log/"

'''

sheet  = '''python tpsmate_cli.py sheet [options] [file|directory]

upload image to tps 

Options:
 --file=[file]           the style sheet file.
 --logdir=[csv]          save the log to a csv file.
 --no-log                NOT export log to a csv file 

Examples:
 python tpsmate_cli.py upload --file "/path/to/image.jpg"
 python tpsmate_cli.py upload --file "/path/to/image.jpg" --no-interactive
 python tpsmate_cli.py upload --file "/path/to/image.jpg" --no-log
 python tpsmate_cli.py upload --file "/path/to/image.jpg,/path/to/another/image.png"
 python tpsmate_cli.py upload --dir "/path/to/image/directory"
 python tpsmate_cli.py upload --dir "/path/to/image/directory" --logdir "/path/to/save/csv/log/"

'''

config = '''python tpsmate_cli.py config key [value]

configuration

Examples:
 python tpsmate_cli.py config username "username"
 python tpsmate_cli.py config password "password"
 python tpsmate_cli.py config encoding "utf-8,gbk"

'''

info   = '''python tpsmate_cli.py info

print info'''

logout = '''python tpsmate_cli.py logout

logout from tps

'''
