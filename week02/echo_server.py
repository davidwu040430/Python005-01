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
            command = buf.decode('utf-8')
            logging.debug('接收到客户端 {}:{} 内容：{}'.format(addr[0], addr[1], command))
            if command.split()[0].lower() == 'put':
                logging.debug(f'收到一个put请求: {command}')
                server_put(command, conn)
            elif command.split()[0].lower() == 'get':
                logging.debug(f'收到一个get请求: {command}')
                server_get(command, conn)
            else:
                conn.sendall(buf)
                logging.debug('发送到客户端 {}:{} 内容：{}'.format(addr[0], addr[1], command))
    conn.close()
    logging.info('客户端退出, 客户端 {}:{}, pid: {}'.format(addr[0], addr[1], os.getpid()))

def server_put(command, conn):
    # 检查put命令是否是3个参数，如果不是，发送错误回应，并返回
    if len(command.split()) != 4:
        conn.sendall("Error: 错误的命令，正确命令应该为 put source_file [None|target_dir|target_file] size.".encode('utf-8'))
    else:
        _, src_file, target_file, file_size = command.split()
        filename = Path(src_file).name
        # 如果没有指定目标目录，则为当前目录下的recv目录
        if target_file == 'None':
            target_p = Path(__file__).resolve().parent.joinpath('recv', filename)
        else:
            if target_file[-1] == '/':
                target_p = Path(target_file).joinpath(filename)
            else:
                target_p = Path(target_file)
                if target_p.is_dir():
                    target_p = target_p.joinpath(filename)
        
        # 取出目录和文件名
        target_dir = target_p.parent
        filename = target_p.name
        try:
            target_dir.mkdir(parents=True, exist_ok=True)
            with open(target_p, 'wb') as f:
                pass
        except Exception as e:
            logging.critical('Error: {}'.format(e))
            conn.sendall('Error: {}'.format(e).encode('utf-8'))
            return        
        
        logging.debug('文件名: {}, 目标目录：{}'.format(filename, target_dir))
        # 一切正常，则向客户端返回OK
        conn.sendall(b'OK: Server is ready to recieve file.')
        try:
            with open(target_p, 'wb') as f:
                r_size = 0
                while r_size < int(file_size):
                    buf = conn.recv(1024)
                    r_size += len(buf)
                    print(buf.decode('utf-8'))
                    if not buf:
                        break
                    else:
                        f.write(buf)
        except Exception as e:
            conn.sendall(b'Error: Server side error occured {}'.format(e))
            logging.critical('Error: {}'.format(e))
        logging.debug('接受文件完成，{}，文件大小：{}'.format(target_p, file_size))

def server_get(command, conn):
    pass

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
