import configparser
from conf import settings


class Config:
    def __init__(self, config_filename='dbconfig.conf'):
        '''
        :summary 初始化数据库配置的路径，以及配置信息
        :param config_filename: 数据库配置的路径
        '''
        # file_path=os.path.join(os.path.dirname(__file__),config_filename).replace('\\','/')
        # file_path=os.path.join(os.getcwd(),config_filename)
        file_path = settings.DB_PATH
        self.cf = configparser.ConfigParser()
        self.cf.read(file_path)

    def get_sections(self):
        '''
        :summary 获取所有数据库的[]部分的信息，相当于获取所有的数据库
        :return: 返回所有的数据库信息
        '''
        return self.cf.sections()

    def get_options(self, section):
        '''
        :summary 获取'section'的信息
        :param section: 某个数据库
        :return: 返回section的信息
        '''
        return self.cf.options(section)

    def get_content(self, section):
        '''
        :summary 将section部分的信息转换为列表，并返回
        :param section: 某个数据库
        :return: 以列表形式返回数据库详细参数信息
        '''
        result = {}
        for option in self.get_options(section):
            value = self.cf.get(section, option)
            result[option] = int(value) if value.isdigit() else value
        return result


if __name__ == '__main__':
    testdb = Config()
    print(testdb.get_content('mysqldb'))
