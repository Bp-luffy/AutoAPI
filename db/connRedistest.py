#coding=utf-8
from db.base.baseConfig import Config
from sshtunnel import SSHTunnelForwarder
from pymongo import MongoClient
import pandas,json,time

#显示所有行
pandas.set_option('display.max_rows',None)
#设置数据的显示长度，默认为50
pandas.set_option('max_colwidth',200)
#禁止自动换行(设置为Flase不自动换行，True反之)
pandas.set_option('expand_frame_repr', False)
#设置取消科学法表示
pandas.set_option('float_format', lambda x: '%.0f' % x)


class mongodbpool(Config):
    def __init__(self,section,sshcon=False):
        try:
            Config.__init__(self)
            self.conf=self.get_content(section)
            self.mongoClient = self.__getconn(sshcon)
        except Exception as e:
            print("redis 连接失败，错误信息%s"%e)

    def __getconn(self,sshcon):
        try:
            if sshcon == True:
                self.server = SSHTunnelForwarder(
                   ssh_address_or_host = (self.conf['ssh_address_or_host'],self.conf['ssh_port']),
                    ssh_username = self.conf['ssh_username'],
                    ssh_password = self.conf['ssh_password'],
                    remote_bind_address = (self.conf['remote_bind_address'],self.conf['port']))
                self.server.start()
                client = MongoClient('127.0.0.1', self.server.local_bind_port)  ##这里一定要填入ssh映射到本地端口
                db = client.admin
                db.authenticate(self.conf['mongo_user'], self.conf['mongo_password'])
            elif sshcon == False:
                client = MongoClient(self.conf['host'], self.conf['port'])
            return client
        except Exception as e:
            print('sshcon类型选择错误:%s' %e)

    def df2mongo(self,df_data,db_name,form_name):
        '''DataFrame数据写入mongodb'''
        def df2bson(df):
            '''DataFrame类型转换为Bson类型'''
            data=json.loads(df.T.to_json()).values()
            return data
        try:
            my_db=self.mongoClient[db_name]
            bson_data = df2bson(df_data)
            my_posts = my_db[form_name]
            result = my_posts.insert_many(bson_data)
        except Exception as e:
            print("异常了：%s"%e)
        return result

    def collection2df(self,db_name,collection_name,query={},no_id=False):
        '''查询数据库，导出dataframe类型数据
        （db_name:数据库名，collection_name:集合名，query：查询条件式，no_id：不显示ID，默认为不显示）'''
        try:
            collection = self.mongoClient[db_name][collection_name]
            cursor = collection.find(query)
            df = pandas.DataFrame(list(cursor))
            if no_id:
                del df['_id']
        except Exception as e:
            print("异常了：%s"%e)
        return df

    def close_server(self):
        self.server.close()

if __name__ == '__main__':
    starttime=time.time()
    #df_data = pandas.DataFrame({"staff":["2jqwq3fiprg2"],"amount":[200000],"itime":[1576252800],"type":[1],"status":[0]})
    db_name = 'appstore' #appstore xinletao
    collection_name = 'charge'#charge user
    query={"itime":{'$gte':1576252800,'$lte':1576339199}}
    test=mongodbpool('appstore',sshcon=True).collection2df(db_name,collection_name,query=query)
    endtime=time.time()
    print(test)
    print(endtime-starttime)