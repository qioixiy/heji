#!env python
import re
import copy
import splider
import libs
import excel_op
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')

def saveToExcel(lists, filter_date, filename):
    excel_opeator = excel_op.excel_OP(filename)
    excel_opeator.add_sheet('sheet1')
    row = 0
    col = 0
    col_name = 2
    col_href = 3
    col_time = 4
    col_desc = 5
    col_star = 6
    excel_opeator.write('sheet1', row, col_name, 'name')
    #excel_opeator.write('sheet1', row, col_href, 'href')
    excel_opeator.write('sheet1', row, col_time, 'time')
    excel_opeator.write('sheet1', row, col_desc, 'desc')
    excel_opeator.write('sheet1', row, col_star, 'star')

    row = row + 1

    for list in lists:
        ___title = list['title']
        print ___title.encode("gbk")

        __title = re.findall('.+\((.*?)\).+', ___title)
        if 0 != len(__title):
            _title = __title[0]
            title = unicode(_title, "utf-8")
            excel_opeator.write('sheet1', row, col, title)

        comments = list['comments']
        for comment in comments:
            if (comment['time'] != filter_date) :
                continue

            name = unicode(comment['name'], "utf-8")
            #href = unicode(comment['href'], "utf-8")
            time = unicode(comment['time'], "utf-8")
            desc = unicode(comment['desc'], "utf-8")
            star = unicode(comment['star'], "utf-8")

            excel_opeator.write('sheet1', row, col_name, name)
            #excel_opeator.write('sheet1', row, col_href, href)
            excel_opeator.write('sheet1', row, col_time, time)
            excel_opeator.write('sheet1', row, col_desc, desc)
            excel_opeator.write('sheet1', row, col_star, star)
            row = row + 1

        row = row + 1

    excel_opeator.save()

def parserUrl(url):
    mysplider = splider.BrowserBase()
    fp = mysplider.openurl(url)
    html = fp.read()
    title = re.findall('<title>(.*?)</title>', html, re.S)[0]
    
    DEBUG = False
    if DEBUG:
        logfp = open('log.html', 'w')
        logfp.write(html)
        logfp.close()

    #lists = libs.getListsFromHtml(html, r'<li class="comment-item"', r'</li>')
    #for list in lists:
    #    libs.getMapFromLists(list)

    myItems = re.findall('<li id="rev_(.*?)" data-id="(.*?)"(.*?)</li>', html, re.S)
    print len(myItems)
    items = []
    for item in myItems:
        items.append(item[2])

    comments = []
    for item in items:
        comments.append(libs.getMapFromLists(item))
    return title, comments, url

def getUrlsFromConf(cFile):
    fp = open(cFile)
    urllists = []
    filter_date = ''
    while(True):
        line = fp.readline()

        if len(line) == 1 :
            continue
        if(line[0] == '#'):
            continue

        date = re.findall('[0-2][0-9]-[0-3][0-9]', line)
        if(0 != len(date)) :
           filter_date = date[0]
           print filter_date

        lines = re.findall('(.*?)#(.*?)', line)
        if (len(lines) == 0) :
            break

        line = lines[0][0]
        urllists.append(line + '/review_more')

    return urllists,filter_date

def main(conf, xlsfilename):
    oneshop = {}
    allshop =[]

    urllists,filter_date = getUrlsFromConf(conf)
    
    for url in urllists:
        title, comments, url = parserUrl(url)
        oneshop['title'] = title
        oneshop['comments'] = comments
        oneshop['url'] = url

        #note must be deepcopy
        allshop.append(copy.deepcopy(oneshop))

    print 'len = %d' % len(allshop)

    saveToExcel(allshop, filter_date, xlsfilename)


if __name__=='__main__':
    main('conf_1.txt', 'result_1.xls')
    main('conf_2.txt', 'result_2.xls')

    os.system("pause")
