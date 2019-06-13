#!-*- coding:utf-8 -*-

def chunkize(seq, size):
    for i in xrange(0, len(seq), size):
        yield seq[i:i+size]


if __name__ == "__main__":
    phones = range(100)
    for val in chunkize(phones, 10):
        print val
