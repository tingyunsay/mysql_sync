#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from config import *
from subprocess import getstatusoutput
import logging
import re
import pymysql

file_name = __file__.split('/')[-1].replace(".py","")
logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='%s.log'%file_name,
                filemode='a')

#将日志打印到标准输出（设定在某个级别之上的错误）
console = logging.StreamHandler()
console.setLevel(logging.INFO)
#formatter = logging.Formatter('%(name)-12s: %(levelname)-6s %(lineno)s %(message)s')
formatter = logging.Formatter('%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

def db_connetionSS(ip,port,user,pwd,db=""):
    conn = pymysql.connect(host=ip,
                           port=port,
                           user=user,
                           password=pwd,
                           db=db,
                           charset='utf8'
                           )
    cursor = pymysql.cursors.SSCursor(conn)
    return conn,cursor


class Sync(object):
    def __init__(self):
        self.source_db =  source_database
        self.target_db =  target_database
        pass

    def sync(self):
        #备份数据到当前路径下
        if self.bak():
            ret_list,fail_num = self.load()
            if fail_num > 0: 
                logging.warning("load data to some tatget_database failed , please check connect , nums is [%d],the ret_list is [%s] ."%(fail_num,';'.join(ret_list)))
            #为所有目标机器建立db
            self.create_db()

            #导入数据
            self.load()
        pass 

    def bak(self):
        bak_sql = "mysqldump -u{user} -p{pwd} -h{host} -P{port} {db} {table} > ./{bakfile_name}".format(
                user = self.source_db['user'],
                pwd = self.source_db['pwd'],
                host = self.source_db['host'],
                port = self.source_db['port'],
                db = self.source_db['db'],
                table = self.source_db['table'],
                bakfile_name = bakfile_name
                )
        ret = getstatusoutput(bak_sql)
        if re.search("error",ret[1]):
            logging.fatal("mysqldump failed , please check config:source_database and connect!")
            return False
        return True
        pass 

    def load(self):
        ret_list = []
        success_num = 0
        for t_db in self.target_db:
            load_sql = "mysql -u{user} -p{pwd} -h{host} -P{port} {db} < ./{bakfile_name}".format(
                    user = t_db['user'],
                    pwd = t_db['pwd'],
                    host = t_db['host'],
                    port = t_db['port'],
                    db = t_db['db'],
                    bakfile_name = bakfile_name
                    )
            ret = getstatusoutput(load_sql)
            fail_num = 0
            if ret[0] != 0:
                logging.fatal("mysql load bakfile data failed , please check config:target_database and connect!")
                ret_list.append(False)
                fail_num += 1
                continue
            ret_list.append(True)
        return ret_list,success_num

        pass 
    #对每个target_db中创建配置中的dababase
    def create_db(self):
        for t_db in self.target_db:
            conn, cursor = db_connetionSS(t_db['host'], t_db['port'], t_db['user'], t_db['pwd'])
            db = t_db['db']
            cursor.execute("show databases;")
            databases = [x[0] for x in cursor.fetchall()]
            if db not in databases:
                sql_database = "create database if not exists %s"%db
                cursor.execute(sql_database)
                conn.commit()
                logging.info("数据库 %s 建立完成."% db)
            else:
                logging.info("数据库 %s 已经存在." % db)
            cursor.close()
            conn.close()
            

if __name__ == '__main__':
    sync = Sync().sync()

    pass

