import logging
import datetime
import time
import os
import sys

def log_call():
    today = datetime.date.today().strftime('%Y%m%d')
    #logfile = '/var/log/python-' + today + '/xxxx.log'
    logfile = '/Users/davidwu/learn_python/playground/' + today + '/xxxx.log'
    logdir = '/Users/davidwu/learn_python/playground/' + today
    if not os.path.isdir(logdir):
        try:
            os.mkdir(logdir)
        except OSError as err:
            sys.exit(1)

    logging.basicConfig(filename=logfile,
                        level=logging.DEBUG,
                        datefmt='%Y-%m-%d %X',
                        format='%(asctime)s %(name)-8s %(levelname)-8s %(message)s')
    logging.info("It's called in: {}".format(time.ctime()))

if __name__ == '__main__':
    log_call()

