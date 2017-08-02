#!-*- coding:utf-8 -*-
import os
import re
import sys
import codecs

"""
配置文件加载，返回字典


配置文件格式:
host=127.0.0.1
port=6379
password=password
db=10
"""

LINE_PATTERN = re.compile(r'\A\s*(?P<key>.+?)\s*=\s*(?P<val>.+?)\s*\Z')
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))

def _load_config():
    redis_config_file = os.path.join(CURRENT_DIR, '../config/redis.ini')
    if not os.path.isfile(redis_config_file):
        print('Error: file not found %s' % redis_config_file)
        sys.exit(1)
    entries = {}
    line_num = 0
    for line in codecs.open(redis_config_file, mode='r', encoding='utf_8', errors='ignore'):
        line_num += 1
        line = line.strip()
        if not line:
            continue # skip empty line
        if line[0] == ';' or line[0] == '#':
            continue # skip comment line
        match = LINE_PATTERN.match(line)
        if not match:
            print('Warning(file %s, line %d): invalid entry' % (redis_config_file, line_num))
            continue
        key = match.group('key')
        if key in entries:
            print('Warning(file %s, line %d): duplicated entry ignored for "%s"' % (redis_config_file, line_num, key))
            continue
        entries[key] = match.group('val')
    return entries
