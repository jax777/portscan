#coding:utf-8

import subprocess
import time
# failed
def rsync_attack(host, port, mongo):
    _info = dict(
        name="rsync",
        ip=host,
        port=port,
        username="",
        password=""
    )

    try:
        cmd = "rsync "+host+"::; exit 0"
        p = subprocess.Popen(cmd,stdout=None)
        time.sleep(2)
        if p.poll():
            pass
        else:
            mongo.insert(_info)
    except:
        pass
