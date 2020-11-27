#!/usr/bin/env python

import datetime
import logging
import os
import sys
import time
from pathlib import Path


def log_call():
    systemlogdir = Path('/var/log')
    # systemlogdir = Path('/Users/davidwu/learn_python/playground')
    today = datetime.date.today().strftime('%Y%m%d')
    logdir = systemlogdir.joinpath('python-{}'.format(today))
    logfile = logdir.joinpath('xxxx.log')

    # 检查日志目录是否存在，如不存在则创建目录
    if not logdir.is_dir():
        try:
            # 使用makedirs来确保建立路径上所有的目录
            os.makedirs(logdir)
        except OSError as err:
            print('Create log directory failed: {}'.format(err))
            sys.exit(1)

    # 配置日志的文件、级别、格式
    logging.basicConfig(filename=logfile,
                        level=logging.DEBUG,
                        datefmt='%Y-%m-%d %X',
                        format='%(asctime)s %(name)-8s %(levelname)-8s %(message)s')

    # 日志记录函数被调用的时间
    logging.info("It's called in: {}".format(time.ctime()))


if __name__ == '__main__':
    log_call()
