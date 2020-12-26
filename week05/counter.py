import redis


def counter(redis_client, vedio_id):
    result = redis_client.incr(vedio_id)
    return result


def main():
    client = redis.Redis(
        host='ec2-3-137-159-11.us-east-2.compute.amazonaws.com', password='WyqWys75$')
    vedio_id = '10001'
    count = counter(client, vedio_id)
    print('{}: {}'.format(vedio_id, count))


if __name__ == '__main__':
    main()