# -*- coding: utf-8 -*- 

import xlrd
import xlwt
import xlutils

class excel_OP(object):
    def __init__(self, fileName = 'result.xls'):
        self.fileName = fileName
        self.workbook = xlwt.Workbook()
        self.sheetNameVK = {}

    def __del__(self):
        print self.fileName +' save ok.'

    def save(self):
        self.workbook.save(self.fileName)

    def add_sheet(self, sheetName):
        sheet = self.workbook.add_sheet(sheetName)
        self.sheetNameVK[sheetName] = sheet

    def write(self, sheetName, row, col, val):
        #print('row=%d,col=%d' % (row,col))
        sheet = self.sheetNameVK[sheetName]
        sheet.write(row, col, val)

if __name__ == '__main__':
    excel_opeator = excel_OP()
    excel_opeator.add_sheet('sheet1')

    excel_opeator.write('sheet1', 1, 1, u'中文test')
    excel_opeator.write('sheet1', 1, 2, u'中文test')

    excel_opeator.save()
