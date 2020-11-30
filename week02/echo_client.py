import socket

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

        # 发送数据到服务器
        s.sendall(data.encode('utf-8'))

        # 接受服务器数据
        data = s.recv(1024)
        if not data:
            break
        else:
            print(data.decode('utf-8'))
    s.close()

if __name__ == '__main__':
    echo_client()
