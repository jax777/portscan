# portscan
依赖
```
apt-get install -y python-dev
apt-get install -y nmap
pip install paramiko
apt-get install -y python2.7-mysqldb
pip install dnspython
pip install pymongo
pip install python-nmap
apt-get install -y freetds-dev
pip install pymssql
pip install redis
pip install
pip install 
```

mongo设置
```
docker run --name hackdb -p 37017:27017  -d mongo --auth
docker exec -it hackdb mongo admin
db.createUser({ user: 'jax777', pwd: 'hackall', roles: [ { role: "__system", db: "admin" } ] });
```


待写
```
mstsc
ldap
vnc    
Pcanywhere
IIS   PUT写文件
Resin
Oracle 1521
PostgreSQL 
ZooKeeper是一个分布式的，开放源码的分布式应用程序协调服务，是Google的Chubby一个开源的实现，是Hadoop和Hbase的重要组件。zookeeper未授权访问，泄露敏感信息，os，hostname，还有存的数据键值，zk默认端口2181
```
