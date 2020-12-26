import redis


def counter(vedio_id):
    client = redis.Redis(
        host='ec2-3-137-159-11.us-east-2.compute.amazonaws.com', password='WyqWys75$')
    result = client.incr(vedio_id)
    return result


def main():

    vedio_id = '10001'
    count = counter(vedio_id)
    print('{}: {}'.format(vedio_id, count))


if __name__ == '__main__':
    main()
