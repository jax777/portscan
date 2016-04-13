#coding:utf-8

def oracle_attack(host, port, mongo):
    _info = dict(
        name="mysql",
        ip=host,
        port=port,
        username="",
        password=""
    )

    # 字典爆破测试
    for username in open("dict/oracle_user.dic", "r"):
        for password in open("dict/oracle_pass.dic", "r"):
            _username = username.strip()
            _password = password.strip()
            try:
                _info["username"] = _username
                _info["password"] = _password
                mongo.insert(_info)
                db.close()
                break
            except:
                pass
