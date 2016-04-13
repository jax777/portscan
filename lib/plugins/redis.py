import redis


def redis_attack(host, port, mongo):
    _info = dict(
        name="redis",
        ip=host,
        port=port,
        username="",
        password=""
    )
    try:
        r = redis.StrictRedis(host='localhost', port=6379, db=0,socket_timeout=2)
        r.set('foo', 'bar')
        mongo.insert(_info)
    except:
        pass
