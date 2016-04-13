import re



def lsip(mongodb):
    ip_info = dict(
        site = "",
        ip = "",
        portinfo = {},
        islocal = 0,
        status = 0
    )
    iplist = []
    for item in mongodb.find({"islocal": 0 }):
        tempip = re.findall(r'\d+.\d+.\d+.',item["ip"])
        if tempip[0] not in iplist:
            iplist.append(tempip[0])
    for ip in iplist:
        for i in range(1,255):
            iptemp =  ip + str(i)
            if mongodb.find({"ip": iptemp }).count() == 0 :
                ip_info = dict(
                    site = "",
                    ip = iptemp,
                    portinfo = {},
                    islocal = 0,
                    status = 0,
                    isup = 1
                )
                mongodb.insert(ip_info)
