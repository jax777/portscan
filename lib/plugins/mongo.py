# coding:utf-8
import pymongo


def mongo_attack(host, port, mongo):
    _info = dict(
        name="mongo",
        ip=host,
        port=port,
        username="",
        password=""
    )
    try:
        conn = pymongo.MongoClient(host, port, socketTimeoutMS=3000)
        dbname = conn.database_names()
        mongo.insert(_info)
    except:
        pass
