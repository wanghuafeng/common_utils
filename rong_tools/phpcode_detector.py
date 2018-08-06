# -*- coding: utf-8 -*-
import os
import sys
import subprocess


def get_phpfile_list(dir):
    php_file_list = []
    for root, subdir, filelist in  os.walk(dir):
        for filename in filelist:
            abs_path = os.path.join(root, filename)
            if (os.path.isfile(abs_path) and abs_path.endswith('.php')):
                php_file_list.append(abs_path)
    return php_file_list
# get_phpfile_list()

def detect_phpfile(phpfile):
    if not os.path.isfile(phpfile):
        print 'file not exists:%s' % phpfile
        return
    check_command = 'php -l %s' % phpfile
    detect_handle = subprocess.Popen(check_command, shell=True, stdout=subprocess.PIPE)
    # popen = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    detect_info = detect_handle.stdout.read()
    # print detect_info
    if(detect_info.find('No syntax errors detected') == 0):
        return
    else:
        return detect_info
# detect_phpcode(r'E:\php_workspace\ec_vm\home\rong\www\ec\model\CreditBill.php')'

def detect(detect_dir):
    php_file_list = get_phpfile_list(detect_dir)
    error_count = 0
    php_file_count = len(php_file_list)
    for php_file in php_file_list:
        error_info = detect_phpfile(php_file)
        if error_info:  #error msg founded
            error_count += 1
            print error_info

    print '检测完毕，共检测php文件数量:%d, 正确文件数:%d, 错误文件数:%d' % (php_file_count, php_file_count-error_count, error_count)

USAGE = '''
-d, -D 待检测根目录
'''
detect_dir = r'E:\php_workspace\ec_vm\home'
detect(detect_dir)
# if __name__ == '__main__':
#     args = sys.argv[1:]
#     if len(args) == 2:
#         if args[0] in ('-d', '-D'):
#             root_dir = args[1]
#             if os.path.isdir(root_dir):
#                 print "%s not exists"%root_dir
#                 sys.exit()
#             else:
#                 detect(root_dir)
#     else:
#         print USAGE


