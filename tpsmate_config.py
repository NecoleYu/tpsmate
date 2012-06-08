# -*- coding: utf-8 -*-
import os
import sys

def get_config_path(filename):
    if os.path.exists(filename):
        return filename
    local_path = os.path.join(sys.path[0], filename)
    if os.path.exists(local_path):
        return local_path
    user_home = os.getenv('USERPROFILE') or os.getenv('HOME')
    return os.path.join(user_home, filename)

DEFAULT_CONFIG = get_config_path('.tpsmate.config')
DEFAULT_COOKIES = get_config_path('.tpsmate.cookies')

def load_config(path):
	values = {}
	if os.path.exists(path):
		with open(path) as x:
			for line in x.readlines():
				line = line.strip()
				if line:
					if line.startswith('--'):
						line = line.lstrip('-')
						if line.startswith('no-'):
							values[line[3:]] = False
						elif '=' in line:
							k, v = line.split('=', 1)
							values[k] = v
						else:
							values[line] = True
					else:
						raise NotImplementedError(line)
	return values

def dump_config(path, values):
	with open(path, 'w') as x:
		for k in values:
			v = values[k]
			if v is True:
				x.write('--%s\n'%k)
			elif v is False:
				x.write('--no-%s\n'%k)
			else:
				x.write('--%s=%s\n'%(k, v))

class Config:
	def __init__(self, path=DEFAULT_CONFIG):
		self.path = path
		self.values = load_config(path)
	def put(self, k, v=True):
		self.values[k] = v
		dump_config(self.path, self.values)
	def get(self, k, v=None):
		return self.values.get(k, v)
	def delete(self, k):
		if k in self.values:
			del self.values[k]
			dump_config(self.path, self.values)
	def source(self):
		if os.path.exists(self.path):
			with open(self.path) as x:
				return x.read()
	def __str__(self):
		return '<Config{%s}>' % self.values

global_config = Config()

def put_config(k, v=True):
	if k.startswith('no-') and v is True:
		k = k[3:]
		v = False
	global_config.put(k, v)

def get_config(k, v=None):
	return global_config.get(k, v)

def delete_config(k):
	return global_config.delete(k)

def source_config():
	return global_config.source()
