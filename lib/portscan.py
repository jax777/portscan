#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# __author__ jax777
import nmap
import threading
import Queue
import sys
import time
from plugins.ftp import *
from plugins.ssh import *
from plugins.telnet import *
from plugins.mongo import *
from plugins.mysql import *
from plugins.mssql import *
from plugins.memcache import *
from plugins.elasticsearch import *
from plugins.redis import *
from plugins.rsync import *


class Portscan:
    def __init__(self,threads_num,mongodb,g_lock,Wdb):
        self.wdb = Wdb
        self.db = mongodb
        self.thread_count = self.threads_num = threads_num
        self.g_lock  = g_lock
        self.lock = threading.Lock()
        self.STOP_ME = False

    def _queuesetup(self):
        self.queue = Queue.Queue()
        for item in self.db.find({"status": 0 }):
            self.queue.put(item["ip"])
    def _startnmap(self):
        while self.queue.qsize() > 0 and not self.STOP_ME :
                ip = self.queue.get(timeout=1.0)
                self.db.update({'ip': ip}, {"$set" : {'status' : 1}})
                result = {}
                try:
                    nm = nmap.PortScanner()
                    nm.scan(hosts= ip , arguments='-sS -p 21,22,23,25,53,67,68,69,80,110,139,143,161,389,443,512,513,514,873,1080,1352,1433,1521,2049,2181,3306,3389,4000-5000,5432,5632,5900,6379,7000-9000,9090,9200,9300,11211,27017,37017')
                    result = nm[ip].get("tcp")
                    result = {str(v):k for v, k in result.items()}
                    for v, k in result.items():
                        if k["state"] != "open":
                            result.pop(v)
                    try:
                        for j,q in result.items():
                            port = int(j)
                            try:
                                if port == 21:
                                    ftp_attack(ip,port,self.wdb)        #attack
                                elif port == 22:
                                    ssh_attack(ip,port,self.wdb)
                                elif port == 23:
                                    telnet_attack(ip,port,self.wdb)
                                elif port == 873:
                                    rsync_attack(ip,port,self.wdb)
                                elif port == 27017:
                                    mongo_attack(ip,port,self.wdb)
                                elif port == 37017:
                                    mongo_attack(ip,port,self.wdb)
                                elif port == 3306:
                                    mysql_attack(ip,port,self.wdb)
                                elif port == 1433:
                                    mssql_attack(ip,port,self.wdb)
                                elif port == 6379:
                                    redis_attack(ip,port,self.wdb)
                                elif port == 9200:
                                    elasticsearch_attack(ip,port,self.wdb)
                                elif port == 11211:
                                    memcache_attack(ip,port,self.wdb)
                            except IOError:
                                print "nofile"
                    except AttributeError:
                        pass
                except:
                    self.db.update({'ip': ip}, {"$set" : {'isup' : 0 }})
                temp = dict(
                       portinfo = result
                )
                self.db.update({'ip': ip}, {"$set" : {'status' : 2}})
                self.db.update({'ip': ip}, {"$set" : temp})

        self.lock.acquire()
        self.thread_count -= 1
        self.lock.release()
    def run(self):
        self.g_lock.acquire()
        self._queuesetup()
        for i in range(self.threads_num):
            t = threading.Thread(target=self._startnmap, name=str(i))
            t.setDaemon(True)
            t.start()
        while 1:
            if self.thread_count > 1:
                try:
                    time.sleep(1.0)
                except KeyboardInterrupt,e:
                    msg = '[WARNING] User aborted, wait all slave threads to exit...'
                    sys.stdout.write('\r' + msg +  '\n\r')
                    sys.stdout.flush()
                    self.STOP_ME = True
            if  self.thread_count == 0:
                self.g_lock.release()
                break