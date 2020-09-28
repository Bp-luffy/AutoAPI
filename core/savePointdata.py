from lib.common.get_excel_data import getTestData
from db.conn_redis import redispool


def save_data_in_redis(data_path=None):
    if data_path:
        xinfo = getTestData(data_path)
        info = xinfo.get_sheetinfo_by_index(0)
        r = redispool('redisdb')
        for data in info:
            model = data[0]
            point = data[1]
            if point != r.str_get(point):
                r.str_set(point, model)
    else:
        print('不需要保存数据')


if __name__ == '__main__':
    path = '/Users/edz/Downloads/data.csv'
    run = save_data_in_redis(path)

