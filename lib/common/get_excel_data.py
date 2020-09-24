# coding=utf-8
import xlrd
import os


class getTestData:
    def __init__(self, path=''):
        self.xl = xlrd.open_workbook(path)

    # 返回以字典为数据的列表，如：[{'a':1,'b':2},{'a':3,'b':4}]
    def get_sheet_info_dict(self):
        listkey = self.sheet.row_values(0)
        infolist = []
        for row in range(1, self.sheet.nrows):
            info = self.sheet.row_values(row)
            tmp = zip(listkey, info)
            infolist.append(dict(tmp))
        return infolist

    # 不作加工处理的每一行excel表数据，如：[['a','b'],['a','b']]
    def get_sheet_info(self):
        infolist = []
        for row in range(1, self.sheet.nrows):
            info = self.sheet.row_values(row)
            infolist.append(info)
        return infolist

    def get_sheetinfo_by_name(self, name, dict_data=False):
        self.sheet = self.xl.sheet_by_name(name)
        if dict_data:
            return self.get_sheet_info_dict()
        return self.get_sheet_info()

    def get_sheetinfo_by_index(self, index, dict_data=False):
        self.sheet = self.xl.sheet_by_index(index)
        if dict_data:
            return self.get_sheet_info_dict()
        return self.get_sheet_info()


if __name__ == '__main__':
    # path = r'D:\projects\AutoAPI\testdatas\zs_data.xlsx'
    path = '/Users/edz/Downloads/data.xlsx'
    xinfo = getTestData(path)
    info = xinfo.get_sheetinfo_by_index(0,dict_data=True)
    print(info)
