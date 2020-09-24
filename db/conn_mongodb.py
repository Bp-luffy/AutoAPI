# coding=utf-8
from db.base.baseConfig import Config
from db import sshserver
from pymongo import MongoClient
import pandas, json, time

# 显示所有行
pandas.set_option('display.max_rows', None)
# 设置数据的显示长度，默认为50
pandas.set_option('max_colwidth', 2000)
# 禁止自动换行(设置为Flase不自动换行，True反之)
pandas.set_option('expand_frame_repr', False)
# 设置取消科学法表示
pandas.set_option('float_format', lambda x: '%.0f' % x)


class mongodbpool(Config, sshserver):
    def __init__(self, section, sshcon=False, auth_pwd=True):
        try:
            Config.__init__(self)
            conf = self.get_content(section)
            # 有ssh和密码的数据连接
            if sshcon:
                sshserver.__init__(self, conf)
                self.start_server()
                self.mongoClient = MongoClient('127.0.0.1', self.get_local_bind_port())  ##这里一定要填入ssh映射到本地端口
                db = self.mongoClient.admin
                db.authenticate(conf['user'], conf['password'])
            # 没有ssh，但是有密码的数据连接
            elif auth_pwd:
                self.mongoClient = MongoClient(conf['host'], conf['port'])
                db = self.mongoClient.admin
                db.authenticate(conf['user'], conf['password'], mechanism='SCRAM-SHA-1')
            # 针对没有ssh和密码的数据库连接
            else:
                self.mongoClient = MongoClient(conf['host'], conf['port'])
        except Exception as e:
            print("mongo 连接失败，错误信息%s" % e)

    def df2mongo(self, df_data, db_name, form_name):
        '''DataFrame数据写入mongodb'''

        def df2bson(df):
            '''DataFrame类型转换为Bson类型'''
            data = json.loads(df.T.to_json()).values()
            return data

        try:
            my_db = self.mongoClient[db_name]
            bson_data = df2bson(df_data)
            my_posts = my_db[form_name]
            result = my_posts.insert_many(bson_data)
        except Exception as e:
            print("异常了：%s" % e)
        return result

    def collection2df(self, db_name, collection_name, query={}, no_id=False):
        '''查询数据库，导出dataframe类型数据
        （db_name:数据库名，collection_name:集合名，query：查询条件式，no_id：不显示ID，默认为不显示）'''
        try:
            collection = self.mongoClient[db_name][collection_name]
            cursor = collection.find(query)
            df = pandas.DataFrame(list(cursor))
            if no_id:
                del df['_id']
        except Exception as e:
            print("异常了：%s" % e)
        return df

    def removecollection(self, db_name, collection_name, conditions={}):
        '''使用remove方法删除集合'''
        try:
            collection = self.mongoClient[db_name][collection_name]
            cursor = collection.remove(conditions)
        except Exception as e:
            print('异常了：%s' % e)


if __name__ == '__main__':
    starttime = time.time()
    # df_data = pandas.DataFrame({"staff":["2jqwq3fiprg2"],"amount":[200000],"itime":[1576252800],"type":[1],"status":[0]})
    db_name = 'haike'  # appstore xinletao haike
    collection_name = 'user'  # charge user
    # query={"itime":{'$gte':1576252800,'$lte':1576339199}}
    # condtions={'app_id':'2kbfrdcbsw06'}
    # test=mongodbpool('appstore',sshcon=True).collection2df(db_name,collection_name,query=condtions)
    # test=mongodbpool('xlt',auth_pwd=False).collection2df(db_name,collection_name)
    test = mongodbpool('hkbf').collection2df(db_name, collection_name, no_id=True)
    print(test)
    endtime = time.time()
    # print(test)
    print(endtime - starttime)
