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


def byteify(input):
    """Python中将json-loads后的unicode转换为str"""
    if isinstance(input, dict):
        return {byteify(key): byteify(value)
                for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input