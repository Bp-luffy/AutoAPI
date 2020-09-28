import logging,os
from logging import handlers

class Log():
    def __init__(self,name='root',logfilename='bug.log'):
        #CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET 日志等级
        self._logger=logging.getLogger(name)
        #默认情况下，logger本身的log level是warning，为了让info handler的level等级生效，所以调低logger本身的level
        self._logger.setLevel(logging.DEBUG) #整个logger的最低日志等级

        filename=os.path.join(os.path.dirname(__file__),'logs',logfilename)
        formatter=logging.Formatter('[%(asctime)s] [%(levelname)s]-%(filename)s(line:%(lineno)d) - %(message)s','%Y-%m-%d %H:%M:%S')

        #创建输出文件日志对象
        fh=handlers.TimedRotatingFileHandler(filename,when='D',encoding='utf-8',interval=1)
        #当handler的log level高于logger本身的log level时，此设置才会生效
        fh.setLevel(logging.DEBUG)

        #创建控制台输出文件日志对象
        ch=logging.StreamHandler()
        ch.setLevel(logging.INFO)#控制台输出的日志等级，若低于此等级，控制台不会打印日志

        #设置日志格式
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        #把ch fh添加到logger
        self._logger.addHandler(fh)
        self._logger.addHandler(ch)

    def getLogger(self):
        return self._logger

if __name__ == '__main__':
    logger=Log().getLogger()
    # level高于对应输出的等级才能输出，比如高于文件输出等级debug，能在文件中打印，低于控制台的等级，不打印
    logger.info("123")
    logger.debug("456")
