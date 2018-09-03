#!-*- coding:utf-8 -*-
from logging import LoggerAdapter

class LoggerMsgAdapter(LoggerAdapter):
    """
    log msg封装器
    @:param logger: log对象
    @:param adapter_param : 需要预封装的日志信息
    """
    def __init__(self, logger, adapter_param):
        self.logger = logger
        self.adapter_param = adapter_param
        LoggerAdapter.__init__(self, logger, logger.extra)

    def process(self, msg, kwargs):
        kwargs["extra"] = self.logger.extra
        adapter_msg = ""
        for _ in range(1):
            if not isinstance(self.adapter_param, dict):
                self.logger.error('log adapter params not dict, adapter_param=%s' % self.adapter_param)
                break
            try:
                adapter_msg = ''.join(['{}={}\t'.format(k, v) for k, v in self.adapter_param.items()])
            except BaseException as e:
                self.logger.error('init log adapter failed, err_msg=%s' % e)
        msg = '%s%s' % (adapter_msg, msg)
        return msg, kwargs


import logging
import os

PATH = os.path.abspath(os.path.dirname(__file__))
log_filename = r'p2p.log'

logging.basicConfig(
    filename=os.path.join(PATH, log_filename),
    format='[%(levelname)s %(asctime)s] %(message)s',
    level=logging.INFO,
)

def get_console_handler():
    console = logging.StreamHandler()
    formatter = logging.Formatter('[%(levelname)s %(asctime)s] %(message)s')
    console.setFormatter(formatter)
    console.setLevel(logging.INFO)
    return console

logger = logging.getLogger(__name__)
logger.addHandler(get_console_handler())

logger.info('-----------')
