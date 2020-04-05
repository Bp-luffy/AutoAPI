#coding=utf-8
import pymysql
from pymysql.cursors import DictCursor
from DBUtils.PooledDB import PooledDB
from tools.dbtools.base.baseConfig import Config

class mysqlpool(Config):
    __pool=None
    def __init__(self,section):
        try:
            Config.__init__(self)
            config=self.get_content(section)
            self._conn=self.__getConn(config)
            self._cursor=self._conn.cursor()
        except Exception as e:
            print("mysql 连接错误： %s"%e)

    def __getConn(self,config):
        if mysqlpool.__pool is None:
            __pool=PooledDB(creator=pymysql,
                            mincached=1,
                            maxcached=20,
                            host=config['host'],
                            port=config['port'],
                            user=config['user'],
                            password=str(config['password']),
                            db=config['db'],
                            use_unicode=False,
                            charset=config['charset'],
                            cursorclass=DictCursor)
        return __pool.connection()

    def __execute(self,sql,param):
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        return count

    def query(self,sql,param=None,type=None,num=None):
        '''
        :summary 查询数据库，并返回结果，结果集为list/tuple
        :param sql: 执行的sql
        :param param: 可选参数，查询条件
        :param type: 可选参数，返回查询结果数，为one时，返回一条；为many时，返回num条；否则返回所有
        :param num: 可选参数，为many时才有效，并返回num条
        :return: 返回查询结果，结果list/tuple
        '''
        count=self.__execute(sql,param)
        if count>0:
            if type=='one':
                result=self._cursor.fetchone()
            elif type=='many':
                result=self._cursor.fetchmany(num)
            else:
                result=self._cursor.fetchall()
        else:
            result=False
        return result

    def insert(self,sql,param=None,type=None):
        '''
        :summary 插入记录到数据库
        :param sql: 执行的sql
        :param param: 插入的参数值
        :param type: 插入的类型，若为many则插入多条，否则只插入一条
        :return: count 受影响的行数
        '''
        if type=='many':
            count=self._cursor.executemany(sql,param)
        else:
            count=self.__execute(sql,param)
        return count

    def update(self,sql,param):
        '''
         :summary 更新数据库记录
         :param sql: 执行的sql
         :param param: 更新的参数值
         :return: count 受影响的行数
         '''
        return self.__execute(sql,param)

    def delete(self,sql,param):
        '''
         :summary 删除数据库记录
         :param sql: 执行的sql
         :param param: 删除的条件
         :return: count 受影响的行数
         '''
        return self.__execute(sql,param)

    def begin(self):
        '''
        :summary  开启事务
        '''
        self._conn.autocommit(0)

    def end(self,option = 'commit'):
        '''
        :summary 结束事务
        '''
        if option == 'commit':
            self._conn.commit()
        else:
            self._conn.rollback()

    def dispose(self,isEnd=1):
        '''
        :summary 释放连接池资源
        '''
        if isEnd == 1:
            self.end('commit')
        else:
            self.end('rollback')
        self._cursor.close()
        self._conn.close()

if __name__ == '__main__':
    pymysql=mysqlpool('mysqldb')
    sql='select * from sign_guest'
    value=['12312313','342323',234234,'2323234']
    sql1='insert into test1(domain ,id,ip,t) values (%s,%s,%s,%s)'
    #query(sql,type='many',num=2)
    print(pymysql.insert(sql1,param=value))
    pymysql.dispose()
