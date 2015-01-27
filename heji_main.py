#!env python
import re
import copy
import sys
import os

import splider
import libs
import conf_parser
import heji_htmlparser
import csv_op

reload(sys)
sys.setdefaultencoding('utf-8')

def get_data_from_url(url):
    mysplider = splider.BrowserBase()
    html = mysplider.openurl(url).read()
    
    DEBUG = False
    if DEBUG:
        logfp = open('log.html', 'w')
        logfp.write(html)
        logfp.close()
    
    return html

def main(conf, filename):

    urllists,filter_date = conf_parser.getUrlsFromConf(conf)
	
    urls_comments = []
    for url in urllists:
        url_comments = heji_htmlparser.html_parser(get_data_from_url(url))
        urls_comments.append(url_comments)
    csv_op.save_result_to_csv(filename, urls_comments, filter_date)

if __name__=='__main__':
    main('conf_zdd.txt', 'result_zdd.csv')
    main('conf_zmj.txt', 'result_zmj.csv')

    os.system("pause")

