#!-*- coding:utf-8 -*-
def is_ascii(s):
    """check if a string in Python is in ASCII?"""
    return all(ord(c) < 128 for c in s)

def whatisthis(s):
    if isinstance(s, str):
        print "ordinary string"
    elif isinstance(s, unicode):
        print "unicode string"
    else:
        print "not a string"