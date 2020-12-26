import redis


def sendsms(telephone_number, content, key=None):
    client = redis.Redis(
        host='ec2-3-137-159-11.us-east-2.compute.amazonaws.com', password='WyqWys75$')
    # 对计数器加一
    result = client.incr(telephone_number)

    # 如果已经大于5，提示调用方等待，并重试
    if result > 5:
        print('Quota used out, please wait for 60s and retry!')
    else:
        print("send to {} with content '{}'".format(telephone_number, content))
        if result == 1:
            client.expire(telephone_number, 60)


if __name__ == '__main__':
    sendsms(1861001711, 'test')
