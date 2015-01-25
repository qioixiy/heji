#!/bin/env python
# -*- coding: UTF-8 -*-

import sys
import libs

reload(sys)
sys.setdefaultencoding('utf-8')

from HTMLParser import HTMLParser


class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.links_a_href = []
        self.links_img_href = []
 
    def handle_starttag(self, tag, attrs):
        #print "Encountered the beginning of a %s tag" % tag
        if tag == "a":
            if len(attrs) == 0:
                pass
            else:
                for (variable, value)  in attrs:
                    if variable == "href":
                        self.links_a_href.append(value)
        elif tag == 'img':
            if len(attrs) == 0:
                pass
            else:
                for (variable, value)  in attrs:
                    if variable == "src":
                        self.links_img_href.append(value)

def test_html_parser():
    html_code = """
    <a href="www.google.com"> google.com</a>
    <A Href="www.pythonclub.org"> PythonClub </a>
    <A HREF = "www.sina.com.cn"> Sina </a>
    """
    htmlparser = MyHTMLParser()
    htmlparser.feed(html_code)
    htmlparser.close()
    libs.printList(htmlparser.links_a_href)

def html_parser(html, tag = 'a'):

    htmlparser = MyHTMLParser()
    htmlparser.feed(html)
    htmlparser.close()

    if tag == 'a':
        links_a_href = htmlparser.links_a_href
        #libs.printList(links_a_href)
        return links_a_href
    elif tag == 'img':
        links_img_href = htmlparser.links_img_href
        #libs.printList(links_img_href)
        return links_img_href
    else:
        return []

if __name__ == "__main__":
    test_html_parser()
    html_parser("")