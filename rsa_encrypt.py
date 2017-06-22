#!-*- coding:utf-8 -*-
"""
rsa 加密相关及一些爬虫可能会用到的加密方法
"""
import binascii
import base64
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA

def rsa_encrypt_ne(text, (n, e)):
    """rsa encrypt by n,e"""
    assert isinstance(n, long), "n should be long"
    assert isinstance(e, long), "n should be long"
    rsa_pubkey = RSA.construct((n, e))
    rsakey = rsa_pubkey.publickey()
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    cipher_text = base64.b64encode(cipher.encrypt(text))
    return cipher_text

def b64tohex(b64_str):
    """base64编码转化为16进制"""
    b64_decode_str = base64.b64decode(b64_str)
    hex_str = binascii.b2a_hex(b64_decode_str) #b64_decode_str.encode('hex')
    return hex_str

def rsa_encrypt_by_pubkey(text, pubkey):
    """ 江苏加密 """
    rsakey = RSA.importKey(pubkey)
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    cipher_text = base64.b64encode(cipher.encrypt(text))
    return cipher_text

if __name__ == "__main__":
    modules = long(133577494198148480430612897540418888692931351064400868851463750344280724700637488816013416296027589322313185686658804112470606590157353131781454864604052799191828165846907612008610633337430567113478281171106409416463063042538432915769216578662727202070486756423406799233043863186811273145007704172995469597011)
    expotent = long(65537)
    text = 'test'
    print rsa_encrypt_ne(text, (modules, expotent))

    pubkey = """-----BEGIN PUBLIC KEY-----
    'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDdvuIdeVk87qexa'
    'G1p22cSF7ymAwpjpGhiGPGl+wj8414zUR+EXdp0aXvhOS0zknjV/1'
    'VYVe10/YMnuDnyXVQx8owfWor3k+ok+spukUTJn1Vwa1CgiOXabZ1'
    'MbV+ipFTa3sHMaVyBoF3nPYUWPN0XYeP2g/f+GXeWTg7Sgw3q1QIDAQAB'
    -----END PUBLIC KEY-----
    """
    print rsa_encrypt_by_pubkey(text, pubkey)