import socket
from pathlib import Path

HOST = 'localhost'
PORT = 60000

def echo_client():
    '''Echo server的客户端'''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    while True:
        # 接收用户输入
        data = input('input > ')
        # 设定退出条件
        if data == 'exit':
            break
        if data.split()[0].lower() == 'put':
            client_put(data, s)
            continue
        else:
        # 发送数据到服务器
            s.sendall(data.encode('utf-8'))

        # 接受服务器数据
        data = s.recv(1024)
        if not data:
            break
        else:
            print(data.decode('utf-8'))
    s.close()

def client_put(data, s):
    comm, src_file, target_file = data.split()
    src_file = './echo_server.log'
    src_p = Path(src_file)
    print(src_p.stat())
    size = src_p.stat().st_size
    s.sendall('{} {}'.format(data, size).encode('utf-8'))
    # s.sendall(data.encode('utf-8'))
    with open(src_file, 'rb') as f:
        while True:
            file_data = f.read(1024)
            if not file_data:
                break
            print(file_data.decode('utf-8'))
            s.sendall(file_data)

if __name__ == '__main__':
    echo_client()
