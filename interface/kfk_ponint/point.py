import configparser
import json, time
from conf import settings
from kafka import KafkaConsumer
from interface.kfk_ponint import get_userid_by_db as dbhandle
from db.conn_redis import redispool


class KafkaPython:
    consumer = None
    BROKER_LIST = '47.99.74.38:9092'
    server = topic = None

    def __init__(self, mobile=None):
        self.server = self.BROKER_LIST
        self.con = ReadConfig()
        self.r = redispool('redisdb')

        if mobile:
            self.userid = dbhandle.get_userid_by_phone(mobile)
        else:
            self.userid = self.con.read('USERID', 'userid')

        self.topic = self.con.read('TOPIC', 'topic')
        self.query_key_list = eval(self.con.read('QUERYKEY', 'query_key_list'))
        self.query_dict = dict.fromkeys(self.query_key_list)
        self.group = self.con.read('GROUP', 'group')
        self.eventType = eval(self.con.read('EventType', 'eventType')) if self.con.read('EventType', 'eventType') else (
            '1', '2')
        self.deviceid = (self.con.read('DEVICEID', 'deviceid'))
        print('topic:{0}\n当前group: {1}\n当前userid: {2}\n当前deviceid: {3}\n当前eventType:{4}\n查询的字段是{5}'.format \
                  (self.topic, self.group, self.userid, self.deviceid, self.eventType, self.query_key_list))

    def __del__(self):
        print("stop")

    def getConnect(self):
        self.consumer = KafkaConsumer(self.topic, bootstrap_servers=self.server,
                                      group_id=self.group,
                                      value_deserializer=lambda m: json.loads(m.decode('utf-8')))

    def beginConsumer(self):
        if self.consumer:
            print(self.consumer)
            print('连接kafka成功')
            print("begin Query-kafka\n")
        try:
            for oneLog in self.consumer:
                data = oneLog.value
                if not data['user_id'] == self.userid and not data['device_id'] == self.deviceid:
                    continue
                if self.userid:
                    if str(data['eventType']) in self.eventType and data['user_id'] == self.userid:
                        res = self.get_dic(data)
                        print(res)
                        # print(res, flush=True)
                        time.sleep(0.5)
                else:
                    if str(data['eventType']) in self.eventType and data['device_id'] == self.deviceid:
                        res = self.get_dic(data)
                        print(res, flush=True)
                        time.sleep(0.5)
        except KeyboardInterrupt as e:
            print('中断kafka连接')

    def get_dic(self, data):
        for key in self.query_dict:
            res = data.get(key)
            if key == 'sourceId' and self.r.key_is_exist(res):
                data1 = self.r.str_get(res) + ' ' + res
                self.query_dict[key] = data1
            else:
                self.query_dict[key] = res
        beautifule_dict = json.dumps(self.query_dict, ensure_ascii=False)
        return beautifule_dict

    def disConnect(self):
        self.consumer.close()

    def main(self):
        self.getConnect()
        self.beginConsumer()


class ReadConfig:

    def __init__(self):
        self.config = configparser.ConfigParser()
        # self.propath = os.path.split(os.path.realpath(__file__))[0]
        # self.file_path = os.path.join(self.propath, 'config.ini')
        self.file_path = settings.KFK_PATH

    def read(self, section, option):
        self.config.read(self.file_path)
        res = self.config.get(section, option)
        return res


if __name__ == '__main__':
    kp = KafkaPython()
    kp.main()
