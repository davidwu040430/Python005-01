import socket
from multiprocessing import Process
import time
import os
import sys
import logging
from pathlib import Path

HOST = 'localhost'
PORT = 60000
DEBUG = True

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((HOST, PORT))
        s.listen(5)
    except Exception as e:
        logging.critical(f'Lesten {HOST}:{PORT} failed: {e}')
        sys.exit(1)
    logging.info('服务器socket设置完成：{}:{}'.format(HOST, PORT))

    try:
        while True:
            time.sleep(0.01)
            # 接受请求
            connection, address = s.accept()
            logging.info("接收到新连接，客户端 {}:{}".format(address[0], address[1]))
            
            # 开一个新进程处理请求
            p = Process(target=echo_server, args=(connection, address))
            p.start()

            connection.close()
    finally:
        s.close()

# echo服务器处理代码
def echo_server(conn, addr):
    logging.info('进入echo服务器, 客户端 {}:{}, pid: {}'.format(addr[0], addr[1], os.getpid()))
    while True:
        buf = conn.recv(1024)
        # 如果buf是eof，则退出
        if not buf:
            break
        else:
            str_get = buf.decode('utf-8')
            if str_get.split()[0] == 'put':
                logging.debug('Get a put')
            else:
                logging.debug('接收到客户端 {}:{} 内容：{}'.format(addr[0], addr[1], str_get))
                conn.sendall(buf)
                logging.debug('发送到客户端 {}:{} 内容：{}'.format(addr[0], addr[1], str_get))
    conn.close()
    logging.info('客户端退出, 客户端 {}:{}, pid: {}'.format(addr[0], addr[1], os.getpid()))

# 启动守护进程
def daemonize(stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    try:
        # 创建新进程
        pid = os.fork()

        # 父进程退出
        if pid > 0:
            sys.exit(0)
    except OSError as err:
        sys.stderr.write('_Fork #1 failed: {}\n'.format(err))
        sys.exit(1)
    
    # 从父进程环境脱离
    # chdir确认进程不占用任何目录，否则不能umount
    os.chdir('/')
    os.umask(0)
    os.setsid()

    # 第二次fork
    try:
        pid = os.fork()

        if pid > 0:
            # 第二个父进程退出
            sys.exit(0)
    except OSError as err:
        sys.stderr.write('_Fork #2 failed: {}\n'.format(err))
        sys.exit(1)

    # 重定向标准文件描述符
    sys.stdout.flush()
    sys.stderr.flush()

    si = open(stdin, 'r')
    so = open(stdout, 'a+')
    se = open(stderr, 'w')

    # dup2函数原子化关闭和复制文件描述符
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())
    logging.info('守护进程初始化完成，当前进程号: {}'.format(os.getpid()))

def config_logging():
    loglevel = logging.DEBUG
    if DEBUG:
        logfile = '/dev/stdout'
    else:
        logfile = Path(__file__).parent.joinpath('echo_server.log')
    logging.basicConfig(filename=logfile,
                        level=loglevel,
                        datefmt='%Y-%m-%d %X',
                        format='%(asctime)s %(levelname)-8s %(message)s')
    logging.info('logging配置完成')

if __name__ == '__main__':
    config_logging()
    if not DEBUG:
        daemonize()
    main()
