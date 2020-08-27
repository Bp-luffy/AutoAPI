import redis, json
from tools.dbtools.base.baseConfig import Config
from tools.dbtools.base.sshServer import sshserver


class redispool(Config, sshserver):
    def __init__(self, section, sshconn=False):
        try:
            Config.__init__(self)
            conf = self.get_content(section)
            if sshconn:
                sshserver.__init__(self, conf)
                self.start_server()
                pool = redis.ConnectionPool(host='127.0.0.1', port=self.get_local_bind_port(),
                                            password=str(conf['password']), db=conf['db'])
            else:
                pool = redis.ConnectionPool(host=conf['host'], port=conf['port'], password=str(conf['password']),
                                            db=conf['db'])
            self.r = redis.Redis(connection_pool=pool)
        except Exception as e:
            print("redis 连接失败，错误信息%s" % e)

    def str_get(self, k):
        res = self.r.get(k)  # 会从服务器传对应的值过来，性能慢
        if res:
            return res.decode()  # 从redis里面拿到的是bytes类型的数据，需要转换一下

    def str_set(self, k, v, time=None):  # time默认失效时间
        self.r.set(k, v, time)

    def str_delete(self, k):
        tag = self.r.exists(k)
        # 判断这个key是否存在，相对于get到这个key他只是传回一个存在的信息，而不用将整个k值传过来
        if tag:
            self.r.delets(k)
        else:
            print('这个key不存在')

    def hash_get(self, name, k):  # 哈希类型存储的是多层字典（嵌套字典）
        res = self.r.hget(name, k)
        if res:
            return res.decode()  # 因为get不到值的话也不会报错所以需要判断一下

    def hash_set(self, name, k, v):  # 哈希类型的是多层
        self.r.hset(name, k, v)  # set 也不会报错

    def hash_getall(self, name):
        res = self.r.hgetall(name)  # 得到的是字典类型，里面的k,v都是bytes类型
        data = {}
        if res:
            for k, v in res.items():  # 循环取出字典里面的k，v，再进行decode
                k = k.decode()
                v = v.decode()
                data[k] = v
        return data

    def hash_del(self, name, k):
        res = self.hdel(name, k)
        if res:
            print('删除成功')
            return 1
        else:
            print('删除失败，该key不存在')
            return 0

    @property  # 属性方法
    # 使用的时候和变量一个用法就好比实例，A=MyRedis(),A.clean_redis使用，
    # 如果不加这个@property，使用时A=MyRedis(),A.cleam_redis（）后面需要加这个函数的括号
    def clean_redis(self):
        self.r.flushdb()  # 清空redis
        print('清空redis成功')
        return 0


if __name__ == '__main__':
    r = redispool('redisdb')  # redisdb appstoreredis
    # r.clean_redis
    data = json.dumps({'project': 'india', 'total_size': '15.8 MB', "action": 1})
    r.hash_set('wait_task2', 1, data)
    # r.str_set('name','lily')
    # r.close_server()
