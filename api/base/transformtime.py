import time

class TransformTime():
    def strTotimestamp(xttime):
        '''字符日期转换为unix时间'''
        timeArray = time.strptime(xttime.strip(), '%Y-%m-%d %H:%M:%S')
        timeStamp = int(time.mktime(timeArray))
        return timeStamp

if __name__ == '__main__':
    a=time.time()
