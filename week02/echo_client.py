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
        data = input('input > '):
        if not data:
            continue
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
    elements = data.split()
    # 根据命令的不同参数个数来赋值
    src_p = Path(elements[1])
    if len(elements) == 2:
        source_file = elements[1]
        target_file = None
    elif len(elements) == 3:
        source_file = elements[1]
        target_file = elements[2]
    else:
        print('Error: 错误命令')
        return
    
    src_p = Path(source_file)
    # src_p如果不是文件，打印错误信息返回
    if not src_p.is_file():
        print("'{}' should be a file".format(src_p))
        return
    # 获取文件的尺寸，发送给服务器端
    s.sendall('{} {} {} {}'.format('PUT', elements[1], target_file, src_p.stat().st_size).encode('utf-8'))

    # 接受服务器端的回复，OK开始传送文件，ERROR表示有错误发送，显示错误信息
    response = s.recv(1024)
    if response.decode('utf-8').startswith("OK"):
        with open(src_p, 'rb') as f:
            while True:
                file_data = f.read(1024)
                if not file_data:
                    break
                print(file_data.decode('utf-8'))
                s.sendall(file_data)
    else:
        print(response.decode('utf-8'))

if __name__ == '__main__':
    echo_client()
