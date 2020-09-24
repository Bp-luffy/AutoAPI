from db.conn_mysql import MYSQLpool


def get_userid_by_phone(mobile=None):
    account_center_dbhandler = MYSQLpool('qtsdb')
    sql = f'select id FROM user where mobile = {mobile}'
    userid = account_center_dbhandler.query(sql)[0]
    userid = str(userid['id'])
    return userid


if __name__ == '__main__':
    res = get_userid_by_phone(mobile='13100001111')
    print(type(res))
