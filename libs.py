# -*- coding: utf-8 -*-

import re

def getListsFromHtml(html, str_start, str_end):
    lists = []
    substring = html

    while True:
        pointer1 = substring.find(str_start)

        _substring = substring[pointer1:len(substring)]
        pointer2 = pointer1 + _substring.find(str_end) + len(str_end)
        if (pointer1 == -1 | pointer2 == -1):
            break
        
        lists.append(substring[pointer1:pointer2])
        
        substring = substring[pointer2+1:]

    return lists

def printList(lists):
    for list in lists:
        print list

def getMapFromLists(list):
    #print list
    unicodePage = list.decode("utf-8")
    kv = {}

    myItems = re.findall('<a target="_blank" title="" href="(.*?)">(.*?)</a>', list ,re.S)
    for item in myItems:
        kv['href'] = item[0]
        kv['name'] = item[1]

    myItems = re.findall('<div class="J_brief-cont">(.*?)</div>',list,re.S)
    
    kv['desc'] = ''.join(myItems[0].split())
    myItems = re.findall('<span class="time">(.*?)</span>',list,re.S)
    if (0 != len(myItems)):
        kv['time'] = myItems[0]
    else :
        print 'warning. %s' % (kv['name'])
        kv['time'] = ''

    myItems = re.findall('<span title="" class="item-rank-rst irr-star(.*?)0"></span>',list,re.S)
    kv['star'] = myItems[0]

    #print kv['href']
    #print kv['name']
    #print kv['desc']
    #print kv['time']
    #print kv['star']

    return kv
