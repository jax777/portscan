#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# __author__ jax777
import Queue
import sys
import dns.resolver
import threading
import time
import os

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



class Dnstask:
    def __init__(self, target,names_file, threads_num,mongodb,g_lock):
        self.db = mongodb
        self.STOP_ME = False
        self.target = target.strip()
        self.names_file = names_file
        self.thread_count = self.threads_num = threads_num
        self.scan_count = self.found_count = 0
        self.lock = threading.Lock()
        self.resolvers = [dns.resolver.Resolver() for _ in range(threads_num)]
        self._load_dns_servers()
        self._load_sub_names()
        self._load_next_sub()
        self.ip_dict = {}
        self.STOP_ME = False
        self.g_lock  = g_lock



    def _load_dns_servers(self):
        dns_servers = []
        with open('dict/dns_servers.txt') as f:
            for line in f:
                server = line.strip()
                if server.count('.') == 3 and server not in dns_servers:
                    dns_servers.append(server)
        self.dns_servers = dns_servers
        self.dns_count = len(dns_servers)

    def _load_sub_names(self):
        self.queue = Queue.Queue()
        file = 'dict/' + self.names_file if not os.path.exists(self.names_file) else self.names_file
        with open(file) as f:
            for line in f:
                sub = line.strip()
                if sub: self.queue.put(sub)

    def _load_next_sub(self):
        next_subs = []
        with open('dict/next_sub.txt') as f:
            for line in f:
                sub = line.strip()
                if sub and sub not in next_subs:
                    next_subs.append(sub)
        self.next_subs = next_subs
    def _update_scan_count(self):
        self.lock.acquire()
        self.scan_count += 1
        self.lock.release()

    def _print_progress(self):
        self.lock.acquire()
        msg = '%s found | %s remaining | %s scanned in %.2f seconds' % (
            self.found_count, self.queue.qsize(), self.scan_count, time.time() - self.start_time)
        sys.stdout.write('\r' + ' '  + msg)
        sys.stdout.flush()
        self.lock.release()


    def _scan(self):
        thread_id = int( threading.currentThread().getName() )
        self.resolvers[thread_id].nameservers.insert(0, self.dns_servers[thread_id % self.dns_count])
        self.resolvers[thread_id].lifetime = self.resolvers[thread_id].timeout = 10.0
        while self.queue.qsize() > 0 and not self.STOP_ME and self.found_count < 4000:    # limit found count to 4000
            sub = self.queue.get(timeout=1.0)
            for _ in range(6):
                try:
                    cur_sub_domain = sub + '.' + self.target
                    answers = self.resolvers[thread_id].query(cur_sub_domain)
                    is_wildcard_record = False
                    if answers:
                        for answer in answers:
                            self.lock.acquire()
                            if answer.address not in self.ip_dict:
                                self.ip_dict[answer.address] = 1
                            else:
                                self.ip_dict[answer.address] += 1
                                if self.ip_dict[answer.address] > 2:    # a wildcard DNS record
                                    is_wildcard_record = True
                            self.lock.release()
                        if is_wildcard_record:
                            self._update_scan_count()
                            self._print_progress()
                            continue
                        self.lock.acquire()
                        self.found_count += 1
                        msg = cur_sub_domain.ljust(30)
                        sys.stdout.write( msg  + '\n')
                        sys.stdout.flush()
                        self.lock.release()
                        for i in self.next_subs:
                           self.queue.put(i + '.' + sub)
                        for answer in answers:
                            temp = answer.address
                            sys.stdout.write(temp)
                            ip_info = dict(
                            site = cur_sub_domain,
                            ip = temp,
                            portinfo = {},
                            islocal = is_intranet(temp),
                            status = 0,
                            isup = 1
                            )
                            if self.db.find({"ip": temp }).count() == 0 :
                                self.db.insert(ip_info)
                        break
                except dns.resolver.NoNameservers, e:
                    break
                except Exception, e:
                    pass
            self._update_scan_count()
            self._print_progress()
        self._print_progress()
        self.lock.acquire()
        self.thread_count -= 1
        self.lock.release()
    def run(self):
        self.g_lock.acquire()
        self.start_time = time.time()
        for i in range(self.threads_num):
            t = threading.Thread(target=self._scan, name=str(i))
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