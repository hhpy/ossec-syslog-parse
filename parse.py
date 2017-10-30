#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import os
import time
import requests
import logging
import logging.handlers
import json
import hashlib
import traceback

class OssecLog(object):
    def __init__(self, log_file):
        super(OssecLog, self).__init__()
        self.log_file = log_file
        # 判断log文件
        if os.path.isfile(self.log_file) == False:
            throw_error('log文件不存在')
            pass
        # 记录日志
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        rh = logging.handlers.TimedRotatingFileHandler('debug.log','D')
        fm = logging.Formatter("%(asctime)s  %(levelname)s - %(message)s","%Y-%m-%d %H:%M:%S")
        rh.setFormatter(fm)
        logger.addHandler(rh)

    # 5分钟分析一次，每次分析拿到6分钟的错误日志
    def parseInvalidUser(self):
        # 计算时间
        now = time.time()
        now_min = time.localtime(now)
        pre6min = time.localtime(now - 360)
        t1 = time.asctime(now_min)[4:15]
        t2 = time.asctime(pre6min)[4:15]
        if t1 == t2:
            date_grep = t1
            pass
        else:
            date_grep = '%s|%s' % (t1, t2)
            pass
        # 拼接cat命令执行
        command = 'cat %s | grep -E "%s" | grep "Invalid user"'%(self.log_file, date_grep)
        output = os.popen(command)
        logging.info(command)
        # 请求接口
        self._sendRequest('InvalidUser', {'data': output.read()})
        pass

    # 5分钟分析一次，每次分析拿到6分钟的错误日志
    def parseNoIdentification(self):
        # 计算时间
        now = time.time()
        now_min = time.localtime(now)
        pre6min = time.localtime(now - 360)
        t1 = time.asctime(now_min)[4:15]
        t2 = time.asctime(pre6min)[4:15]
        if t1 == t2:
            date_grep = t1
            pass
        else:
            date_grep = '%s|%s' % (t1, t2)
            pass
        # 拼接cat命令执行
        command = 'cat %s | grep -E "%s" | grep "Did not receive identification"'%(self.log_file, date_grep)
        output = os.popen(command)
        logging.info(command)
        # 请求接口
        self._sendRequest('InvalidUser', {'data': output.read()})
        pass

    def _sendRequest(self, action, params):
        url = "http://test.com/api/" + action;
        # params.auth
        hash_key = hashlib.sha1('xxx').hexdigest()
        hash_pre = hashlib.sha1(time.strftime('%M')).hexdigest()
        params["auth"] = hashlib.sha1(hash_pre + hash_key).hexdigest();
        r = requests.post(url, data=params)
        # return
        try:
            res = r.json()
        except Exception as e:
            res = r.text
        pass
        # log
        requests_log = {
            # 'params': params,
            'res': res
        }
        logging.info(json.dumps(requests_log) + "\n")
        pass

def throw_error(msg):
    raise Exception(msg)

def main():
    try:
        ol = OssecLog(sys.argv[1])
        ol.parseInvalidUser()
        ol.parseNoIdentification()
    except IndexError as e:
        print '缺少参数：python parse.py logFile'
    except Exception as e:
        print e
    pass

if __name__ == '__main__':
    main()