# coding:utf-8


def elasticsearch_attack(host, port, mongo):
    _info = dict(
        name="elasticsearch",
        ip=host,
        port=port,
        username="",
        password=""
    )
    mongo.insert(_info)
