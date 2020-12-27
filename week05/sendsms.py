import redis
import math


def sendsms(telephone_number, content, key=None):
    client = redis.Redis(
        host='ec2-3-137-159-11.us-east-2.compute.amazonaws.com', password='WyqWys75$')
    # 对计数器加一
    result = client.incr(telephone_number)

    # 如果已经大于5，提示调用方等待，并重试
    if result > 5:
        print('Quota used out, please wait for 60s and retry!')
    else:
        # 按照70字符一条发送
        n = math.ceil(len(content)/70)
        for i in range(n):
            print("send to {} with content '{}'".format(
                telephone_number, content[70*i:70*(i+1)]))
        # 如果是1说明是新开始，设置过期时间
        if result == 1:
            client.expire(telephone_number, 60)


if __name__ == '__main__':
    sendsms(1861001711, 'test'*100)
