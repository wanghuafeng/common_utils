#!-*- coding:utf-8 -*-
import time

"""
计算时间差系列
"""
def convert_2_timestamp():
    """通过转化为时间戳"""
    timestring = '2017-12-04 11:13:01'
    converted_timestring = time.mktime(time.strptime(timestring, '%Y-%m-%d %H:%M:%S'))   # 1512357181.0(float类型)
    current_timestamp = time.time()
    time_interval = current_timestamp - converted_timestring
    print time_interval


def convert_2_datetime(timestring):
    """通过转化为datetime类型"""
    from dateutil import parser
    import datetime
    converted_timestring = parser.parse(timestring)
    current_datetime = datetime.datetime.now()
    interval_second = (current_datetime-converted_timestring).seconds
    return interval_second
# timestring = '2017-12-04 11:13:01'
# print convert_2_datetime(timestring)



import datetime
yesterday = datetime.datetime.now() - datetime.timedelta(days=3)
print yesterday.strftime('%Y_%m_%d')