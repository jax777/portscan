# coding: utf8
import pymongo

db_info = dict(
    host="127.0.0.1",
    port=37017,
    username="jax777",
    password="hackall"
)



def Mongodb( db_info,db_name):
    db_info = db_info
    client = pymongo.MongoClient(db_info.get('host'), db_info.get('port'))
    client.security_detect.authenticate(
        db_info.get('username'),
        db_info.get('password'),
        source='admin'
    )
    db = client["scan_info"]
    return db[db_name]

