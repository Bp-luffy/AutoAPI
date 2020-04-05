#coding=utf-8
import xlrd
import os

class getTestData:
    def __init__(self,path=''):
        self.xl=xlrd.open_workbook(path)

    def get_sheet_info(self):
        listkey=self.sheet.row_values(0)
        infolist=[]
        for row in range(1,self.sheet.nrows):
            info=self.sheet.row_values(row)
            tmp=zip(listkey,info)
            infolist.append(dict(tmp))
        return infolist

    def get_sheetinfo_by_name(self,name):
        self.sheet=self.xl.sheet_by_name(name)
        return self.get_sheet_info()

    def get_sheetinfo_by_index(self,index):
        self.sheet=self.xl.sheet_by_index(index)
        return self.get_sheet_info()

if __name__ == '__main__':
    path=r'D:\projects\AutoAPI\testdatas\zs_data.xlsx'
    xinfo=getTestData(path)
    info=xinfo.get_sheetinfo_by_index(0)
    for i in info:
        i.update(som=0)
        i.pop('渠道名称')
    print(info)