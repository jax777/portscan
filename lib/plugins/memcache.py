# coding:utf-8
import memcache
def memcache_attack(host, port, mongo):
    _info = dict(
        name="memcache",
        ip=host,
        port=port,
        username="",
        password=""
    )
    try:

        mc = memcache.Client([host+':'+port],debug=0)
        mc.set("foo","bar")
        mongo.insert(_info)
    except:
        pass