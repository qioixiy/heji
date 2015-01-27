import re

def getUrlsFromConf(cFile):
    urllists = []
    filter_date = ''
    
    try:
        fp = open(cFile)
    except:
        print cFile, 'not exist!'
        return urllists,filter_date
    
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
