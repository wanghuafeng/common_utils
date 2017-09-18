#!-*- coding:utf-8 -*-
"""
rsa 加密相关及一些爬虫可能会用到的加密方法
"""
import binascii
import base64
import hashlib
from pyDes import *
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA
from binascii import b2a_hex

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
    """rsa encrypt by public key"""
    rsakey = RSA.importKey(pubkey)
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    cipher_text = base64.b64encode(cipher.encrypt(text))
    return cipher_text

def rsa_encrypt(text, e, n):
    """rsa no padding加密模式"""
    text = text[::-1]
    rs = int(b2a_hex(text), 16) ** int(e, 16) % int(n, 16)
    return format(rs, 'x').zfill(256)

def md5(str):
    """封装md5处理"""
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()

def des_encrypt(data):
    """
    des加密
    triple_des()，key Bytes containing the encryption key, must be either 16 or 24 bytes long
    des(), Bytes containing the encryption key, must be exactly 8 bytes
    """
    IV = "01234567"  # 偏转向量
    KEY = "private key"  # 密钥
    k = triple_des(KEY, CBC, IV, pad=None, padmode=PAD_PKCS5)
    return base64.b64encode(k.encrypt(data))

def des_decrypt(data):
    """des解密"""
    IV = "01234567"     #偏转向量
    KEY = "private key"     #密钥
    k = triple_des(KEY, CBC, IV, pad=None, padmode=PAD_PKCS5)
    return k.decrypt(base64.b64decode(data))

if __name__ == "__main__":
    modules = long(133577494198148480)
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