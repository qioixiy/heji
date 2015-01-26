#!/bin/env python
# -*- coding: UTF-8 -*-

import sys
import copy
import re

reload(sys)
sys.setdefaultencoding('utf-8')

from HTMLParser import HTMLParser

class MyHTMLParser(HTMLParser):
    '''
li
li@div.class=pic
li@div.class=pic@a.target=_blank.title=.href=/member;获取用户名
li@div.class=content
li@div.class=content@div.class=user-info
li@div.class=content@div.class=user-info@span;获取星级
li@div.class=content@div.class=comment-txt
li@div.class=content@div.class=comment-txt@div.class=J_brief-cont;获取评价
li@div.class=content@span.class=time;获取时间
    '''
    def __init__(self):
        HTMLParser.__init__(self)

        self.temp_a_commit = {}
        self.comment_list = []
        self.result = {}
                
        self.tag_status = 'none'
        self.title_flag = False
        self.title = []
        
        self.li_flag = False
        self.links_li_href = []

    def get_result(self):
        self.result['comments'] = self.comment_list
        title = re.findall('.+\((.*?)\).+', self.title)
        self.result['shop_name'] = title[0] if len(title) != 0 else ''
        return self.result

    #handle start tag
    def handle_starttag(self, tag, attrs):
        #print "Encountered the beginning of a %s tag" % tag
        if tag == 'title':
            self.title_flag = True
        if tag == 'li':
            if len(attrs) != 0 :
                have_id = False
                have_data_id = False
                for (variable, value)  in attrs:
                    if variable == "id":
                        have_id = True
                    if variable == "data-id":
                        have_data_id = True
                if have_id and have_data_id and self.tag_status == 'none':
                    self.tag_status = 'li'
        if tag == 'div':
            if len(attrs) != 0:
                for (variable, value)  in attrs:
                    if variable == 'class' and value == 'pic' and self.tag_status == 'li+end':
                        self.tag_status = 'li@div.class=pic'
                    elif variable == 'class' and value == 'content' and self.tag_status == 'li@div.class=pic@a.target=_blank.title=.href=/member+end':
                        self.tag_status = 'li@div.class=content'
                    elif variable == 'class' and value == 'user-info' and self.tag_status == 'li@div.class=content+end':
                        self.tag_status = 'li@div.class=content@div.class=user-info'
                    elif variable == 'class' and value == 'comment-txt' and self.tag_status == 'li@div.class=content@div.class=user-info@span+end':
                        self.tag_status = 'li@div.class=content@div.class=comment-txt'
                    elif variable == 'class' and value == 'J_brief-cont' and self.tag_status == 'li@div.class=content@div.class=comment-txt+end':
                        self.tag_status = 'li@div.class=content@div.class=comment-txt@div.class=J_brief-cont'
                        
        if tag == 'a':
            if len(attrs) != 0:
                target_have = False
                title_have = False
                href_have = False
                for (variable, value)  in attrs:
                    if variable == 'target' and value == '_blank':
                        target_have = True
                    elif variable == 'title' and value == '':
                        title_have = True
                    elif variable == 'href' and -1 != value.find('member'):
                        href_have = True
                if target_have and title_have and href_have and self.tag_status == 'li@div.class=pic+end':
                    self.tag_status = 'li@div.class=pic@a.target=_blank.title=.href=/member'
                    
        if tag == 'span':
            if len(attrs) != 0:
                for (variable, value)  in attrs:
                    title_have = False
                    if variable == 'title' and value == '' and self.tag_status == 'li@div.class=content@div.class=user-info+end':
                        self.tag_status = 'li@div.class=content@div.class=user-info@span'
                        title_have = True
                    if variable == 'class' and self.tag_status == 'li@div.class=content@div.class=user-info@span':
                        #print 'start:', value #获取星级
                        self.temp_a_commit['star'] = value[-2:-1]
                    if variable == 'class' and value == 'time' and self.tag_status == 'li@div.class=content@div.class=comment-txt@div.class=J_brief-cont+end':
                        self.tag_status = 'li@div.class=content@span.class=time'
                    
                        
    # handle end tag
    def handle_endtag(self, tag):
        pass

    # handle data           
    def handle_data(self, data):
        if self.title_flag :
            self.title_flag = False
            self.title = data
            #print 'title:',data
        if self.tag_status == 'li':
            self.tag_status = 'li+end'
        elif self.tag_status == 'li@div.class=pic':
            self.tag_status = 'li@div.class=pic+end'
        elif self.tag_status == 'li@div.class=pic@a.target=_blank.title=.href=/member':
            self.tag_status = 'li@div.class=pic@a.target=_blank.title=.href=/member+end'
            #print 'user:', data #获取用户名
            self.temp_a_commit['username'] = data
        elif self.tag_status == 'li@div.class=content':
            self.tag_status = 'li@div.class=content+end'
        elif self.tag_status == 'li@div.class=content@div.class=user-info':
            self.tag_status = 'li@div.class=content@div.class=user-info+end'
        elif self.tag_status == 'li@div.class=content@div.class=user-info@span':
            self.tag_status = 'li@div.class=content@div.class=user-info@span+end'
        elif self.tag_status == 'li@div.class=content@div.class=comment-txt':
            self.tag_status = 'li@div.class=content@div.class=comment-txt+end'
        elif self.tag_status == 'li@div.class=content@div.class=comment-txt@div.class=J_brief-cont':
            self.tag_status = 'li@div.class=content@div.class=comment-txt@div.class=J_brief-cont+end'
            #print 'comment:', data.strip() #获取评价
            self.temp_a_commit['comment'] = data.strip()
        elif self.tag_status == 'li@div.class=content@span.class=time':
            self.tag_status = 'li@div.class=content@span.class=time+end'
            self.tag_status = 'none'
            #print 'time:', data #获取时间
            self.temp_a_commit['date'] = data

            self.comment_list.append(copy.deepcopy(self.temp_a_commit))
            
        #if self.tag_status != 'none':
        #    print self.tag_status

def html_parser(html):

    htmlparser = MyHTMLParser()
    htmlparser.feed(html)
    htmlparser.close()

    result = htmlparser.get_result()

    '''
    print result['shop_name']
    comments = result['comments']
    print len(comments)
    for comment in comments:
        print comment['username'], comment['date'], comment['comment'], comment['star']
    #'''

    return result

if __name__ == "__main__":
    file_object = open('log.html')
    try:
        all_the_text = file_object.read()
    finally:
        file_object.close()

    comments = html_parser(all_the_text)
    import csv_op
    csv_op.save_result_to_csv('result.csv', comments)
