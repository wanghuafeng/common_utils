__author__="wanghuafeng"
#coding:utf-8
import re
import os
import io
import sys
import time
import codecs

def splitdrive(p):#from os.path
    """Split a pathname into drive and path specifiers. Returns a 2-tuple
"(drive,path)";  either part may be empty"""
    if p[1:2] == ':':
        return p[0:2], p[2:]
    return '', p

# Split a path in head (everything up to the last '/') and tail (the
# rest).  After the trailing '/' is stripped, the invariant
# join(head, tail) == p holds.
# The resulting head won't end in '/' unless it is the root.
def split(p):#os.path
    """Split a pathname.

    Return tuple (head, tail) where tail is everything after the final slash.
    Either part may be empty."""

    d, p = splitdrive(p)
    # set i to index beyond p's last slash
    i = len(p)
    while i and p[i-1] not in '/\\':
        i = i - 1
    head, tail = p[:i], p[i:]  # now tail has no slashes
    # remove trailing slashes from head, unless it's all slashes
    head2 = head
    while head2 and head2[-1] in '/\\':
        head2 = head2[:-1]
    head = head2 or head
    return d + head, tail

def unique_list(xs):
    seen = set()
    # not seen.add(x) here acts to make the code shorter without using if statements, seen.add(x) always returns None.
    return [x for x in xs if x not in seen and not seen.add(x)]

def re_show(regexp, string, left="{", right="}"):
    print(re.compile(regexp, re.M).sub(left + r"\g<0>" + right, string.rstrip()))

def splitport(host):
    """splitport('host:port') --> 'host', 'port'."""
    _portprog = re.compile('^(.*):([0-9]+)$')
    match = _portprog.match(host)
    if match: return match.group(1, 2)
    return host, None

# Null bytes; no need to recreate these on each call to guess_json_utf
def guess_json_utf(data):
    # JSON always starts with two ASCII characters, so detection is as
    # easy as counting the nulls and from their location and count
    # determine the encoding. Also detect a BOM, if present.
    _null = '\x00'.encode('ascii')  # encoding to ASCII for Python 3
    _null2 = _null * 2
    _null3 = _null * 3
    sample = data[:4]
    if sample in (codecs.BOM_UTF32_LE, codecs.BOM32_BE):
        return 'utf-32'     # BOM included
    if sample[:3] == codecs.BOM_UTF8:
        return 'utf-8-sig'  # BOM included, MS style (discouraged)
    if sample[:2] in (codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE):
        return 'utf-16'     # BOM included
    nullcount = sample.count(_null)
    if nullcount == 0:
        return 'utf-8'
    if nullcount == 2:
        if sample[::2] == _null2:   # 1st and 3rd are null
            return 'utf-16-be'
        if sample[1::2] == _null2:  # 2nd and 4th are null
            return 'utf-16-le'
            # Did not detect 2 valid UTF-16 ascii-range characters
    if nullcount == 3:
        if sample[:3] == _null3:
            return 'utf-32-be'
        if sample[1:] == _null3:
            return 'utf-32-le'
            # Did not detect a valid UTF-32 ascii-range character
    return None

def combine_freq_words():
    '''合并多个文件，按词频进行倒序排列'''
    import glob
    file_path = r'C:\Users\wanghuafeng\Desktop\test\*.freq'
    total_line_list = []
    file_list = glob.glob(file_path)
    print 'file_list lenght: ', len(file_list)
    for filename in file_list:
        total_line_list.extend(codecs.open(filename).readlines())
    total_line_list = sorted(total_line_list, key=lambda x: int(x.split('\t')[-1]), reverse=True)
    codecs.open(os.path.join(r'C:\Users\wanghuafeng\Desktop\test', 'combine_freq.txt'), mode='wb').writelines(total_line_list)


def make_inorder_by_freq(filename):
    '''使文件按词频倒序排列
    文件格式: 第一列为词，第二列为词频, \t 分割'''
    with codecs.open(filename, encoding='utf-8') as f:
        line_list_inorder = sorted(f.readlines(), key=lambda x:int(x.split('\t')[-1]), reverse=True)
        codecs.open(filename, mode='wb', encoding='utf-8').writelines(line_list_inorder)

def mail_send(mail_content,mail_user='', mail_password= '', mailto= ''):
    import time
    import smtplib
    from email.mime.text import MIMEText
    smtp_server = "" #smtp server

    #设置邮件类型
    msg = MIMEText(mail_content, _subtype='html', _charset='utf-8')#
    timestamp = time.strftime('%Y_%m_%d %H:%M:%S')
    msg['Subject'] = 'ppd monitor, ' + timestamp
    msg['From'] = mail_user

    s = smtplib.SMTP()
    s.connect(smtp_server)
    s.login(mail_user, mail_password)
    s.sendmail(mail_user, mailto, msg.as_string())
    s.close()
