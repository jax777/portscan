#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# __author__ jax777
import sys
import optparse
from lib.dnstask import Dnstask
from lib.iplist import *
from lib.portscan import *
from lib.mongodb import *
import threading

def is_intranet(ip):  #内网ip 判断
    ret = ip.split('.')
    if not len(ret) == 4:
       return 1
    if ret[0] == '10':
       return 1
    if ret[0] == '172' and 16 <= int(ret[1]) <= 32:
       return 1
    if ret[0] == '192' and ret[1] == '168':
       return 1
    return 0


if __name__ == '__main__':
    parser = optparse.OptionParser('usage: %prog [options] target.com')
    parser.add_option('-t', '--threads', dest='threads_num',
              default=30, type='int',
              help='Number of threads. default = 30')
    parser.add_option('-f', '--file', dest='names_file', default='subnames.txt',
              type='string', help='Dict file used to brute sub names')
    (options, args) = parser.parse_args()
    if len(args) < 1:
        parser.print_help()
        sys.exit(0)
    target=args[0]
    mongodb = Mongodb(db_info,target)
    Wdb = Mongodb(db_info,target+"_vul")
    g_lock = threading.Lock()
    d = Dnstask(target=target, names_file=options.names_file,
                 threads_num=options.threads_num,mongodb = mongodb,g_lock =g_lock
                 )
    d.run()
    g_lock.acquire()
    print "list all ip \n"
    lsip(mongodb)
    g_lock.release()
    print "start portscan \n"
    p = Portscan(threads_num=options.threads_num,mongodb = mongodb,g_lock =g_lock,Wdb = Wdb)
    p.run()
    g_lock.acquire()
    print "task over \n"
