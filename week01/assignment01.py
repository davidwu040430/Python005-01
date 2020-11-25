import logging
import datetime
import time
import os
import sys

def log_call():
    today = datetime.date.today().strftime('%Y%m%d')
    logdir = '/var/log/python-' + today
    
    # logdir = '/Users/davidwu/learn_python/playground/' + today
    # 检查日志目录是否存在，如不存在则创建目录
    if not os.path.isdir(logdir):
        try:
            os.mkdir(logdir)
        except OSError as err:
            print('Create log directory failed: {}'.format(err))
            sys.exit(1)
    
    logfile = logdir + '/xxxx.log'

    # 配置日志的文件、级别、格式
    logging.basicConfig(filename=logfile,
                        level=logging.DEBUG,
                        datefmt='%Y-%m-%d %X',
                        format='%(asctime)s %(name)-8s %(levelname)-8s %(message)s')
    
    # 日志记录函数被调用的时间
    logging.info("It's called in: {}".format(time.ctime()))

if __name__ == '__main__':
    log_call()

