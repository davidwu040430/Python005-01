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
        msg = input('input > ')
        # 如果直接回车，跳过后面的处理，直接要求用户再次输入
        if not msg:
            continue
        # 如果输入exit，退出
        elif msg == 'exit':
            break
        elif msg[:4].upper() == 'PUT ':
            client_put(msg, s)
        elif msg[:4].upper() == 'GET ':  
            client_get(msg, s)  
        else:
        # 发送数据到服务器
            s.sendall(msg.encode('utf-8'))

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
    if len(elements) == 2:
        source_file = elements[1]
        target_file = None
    elif len(elements) == 3:
        source_file = elements[1]
        target_file = elements[2]
    else:
        print('Error: 命令格式错误')
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

def client_get(msg, s):
    elements = msg.split()
    if len(elements) == 2:
        source_file = elements[1]
        target_file = None
    elif len(elements) == 3:
        source_file = elements[1]
        target_file = elements[2]
    else:
        print('Error: 命令格式错误')
    filename = Path(source_file).name
    if target_file == None:
        target_p = Path(__file__).parent.joinpath('recv', filename)
    elif target_file[-1] == '/':
        target_p = Path(target_file).joinpath(filename)
    else:
        target_p = Path(target_file)
        if target_p.is_dir():
            target_p = target_p.joinpath(filename)
    
    target_dir = target_p.parent
    filename = target_p.name
    try:
        target_dir.mkdir(parents=True, exist_ok=True)
        with open(target_p, 'wb') as f:
            pass
    except Exception as e:
        print(f'Error: {e}')
        return
    
    # 发送命令
    s.sendall('GET {} {}'.format(source_file, target_p).encode('utf-8'))

    # 接受反馈, 按照协议，服务器端应该回传：OK size，或者Error error message
    response = s.recv(1024)
    if response.decode('utf-8').startswith('OK'):
        s.sendall(b'OK')
        file_size = int(response.split()[1])
        try:
            with open(target_p, 'wb') as f:
                r_size = 0
                while r_size < file_size:
                    buf = s.recv(1024)
                    r_size += len(buf)
                    if not buf:
                        break
                    else:
                        f.write(buf)
        except Exception as e:
            print(f'Error {e}')
            s.sendall(f'Error {e}'.encode('utf-8'))
            return
        s.sendall(b'Succeed')
    else:
        print(response.decode('utf-8'))
        

if __name__ == '__main__':
    echo_client()
