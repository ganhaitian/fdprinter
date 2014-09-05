#coding=UTF-8
__author__ = 'zhijieliu'

import MySQLdb
from DBUtils.PooledDB import PooledDB

def initDBPool(username,password,host,port,db):
    return PooledDB(MySQLdb,maxcached=2,maxshared=2,maxconnections=2,user=username,passwd=password,host=host,port=port,db=db,charset='utf8')

def query(pool, sql, params={}):
    if pool is None or sql is None:
        return []
    print sql
    try:
        conn = pool.connection()
        cursor = conn.cursor()
        #执行查询 语句
        cursor.execute(sql.replace('%',"%%"), params);

        #查询所有记录
        vals = cursor.fetchall()

        if vals is None:
            vals = []

        return vals
    except Exception,ex:
        print ex
        return []
    finally:
        try:
            cursor.close()
        except:
            pass
        try:
            conn.close()
        except:
            pass


def saveOrUpdate(pool, sql, params={}):
    if pool is None or sql is None:
        return []

    try:
        conn = pool.connection()
        cursor = conn.cursor()

        #执行语句

        cursor.execute(sql,params)

        conn.commit()


    except Exception,ex:
        print ex
    finally:
        try:
            cursor.close()
        except:
            pass
        try:
            conn.close()
        except:
            pass