import redis
import functools
import math


def send_times(times=5):
    def decorator(func):
        @functools.wraps(func)
        def wrappers(*args, **kw):
            # 连接redis
            client = redis.Redis(
                host='ec2-3-137-159-11.us-east-2.compute.amazonaws.com', password='WyqWys75$')
            # 从函数参数中取第一个参数作为key
            result = client.incr(args[0])
            if result > times:
                # 如果超过次数，直接打印，不执行发送动作
                print('Quota used out, Please wait 1 min and retry!')
            else:
                # 如果是第一个设定计数器，设置上超时60s
                if result == 1:
                    client.expire(args[0], 60)
                # 执行发送动作
                return func(*args, **kw)
        return wrappers
    return decorator


@send_times(times=5)
def sendsms(telephone_number, content, key=None):
    # 计算发送条数
    n = math.ceil(len(content)/70)
    for i in range(n):
        # 发送短信
        print("send to {} with content '{}'".format(
            telephone_number, content[70*i:70*(i+1)]))


if __name__ == '__main__':
    sendsms(18610010000, 'Test decro')
