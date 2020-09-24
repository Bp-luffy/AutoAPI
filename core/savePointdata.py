from lib.common.get_excel_data import getTestData
from db.conn_redis import redispool

def save_data_in_redis():
    path = '/Users/edz/Downloads/data.csv'
    xinfo = getTestData(path)
    info = xinfo.get_sheetinfo_by_index(0)
    r = redispool('redisdb')
    for data in info:
        model = data[0]
        point = data[1]
        if point != r.str_get(point):
            r.str_set(point,model)
    r.close_server()


if __name__ == '__main__':
    info = save_data_in_redis()

