import time
from bs4 import BeautifulSoup
import requests
from core import TIME_LIMIT_EACH_REQUEST

def getIncludedWord(s:str,c_start:str,c_end:str)->str:
    return s[s.find(c_start)+1:s.find(c_end)]

def delEnter(s:str)->str:
    new_str = ''
    for c in s:
        if c != '\n' and c != '\r':
            new_str += c
    return new_str

def findHref_con(word:str) -> list:
    time.sleep(TIME_LIMIT_EACH_REQUEST)
    res = requests.get('https://dict.concised.moe.edu.tw/search.jsp',params={"word":word})
    soup = BeautifulSoup(res.text,'html.parser')
    filtered_herf = list()
    if('基本檢索' in soup.head.title.getText()):
        herfs = soup.find_all('a')
        for herf in herfs:
            if('dictView' in str(herf)):
                filtered_herf.append(herf['href'])
    elif '辭典檢視' in soup.head.title.getText() :
        filtered_herf.append("search.jsp?word=%s" %(word))
    else:
        print('error:mapping lost')
    return filtered_herf


def findHref(word:str) -> list:
    time.sleep(TIME_LIMIT_EACH_REQUEST)
    res = requests.get('https://dict.revised.moe.edu.tw/search.jsp',params={"word":word})
    soup = BeautifulSoup(res.text,'html.parser')
    filtered_herf = list()
    if('基本檢索' in soup.head.title.getText()):
        herfs = soup.find_all('a')
        for herf in herfs:
            if('dictView' in str(herf)):
                filtered_herf.append(herf['href'])
    elif('辭典檢視' in soup.head.title.getText()):
        filtered_herf.append("search.jsp?word=%s" %(word))
    else:
        print('error:mapping lost')
    return filtered_herf

def readDefinitionFromFrom(soup:BeautifulSoup) -> str:
    return delEnter(soup.find(id='order0').getText())

def readDefinitionFromFrom_con(soup:BeautifulSoup) -> str:
    ret = ''
    i = 1
    for ol in soup.find_all('ol'):
        for li in ol.find_all('li'):
            ret += ' ' + str(i) + ': ' + li.getText()
            i += 1
    if not ret == '':
        return delEnter(ret)
    for section in soup.find('article').find_all():
        if '釋　　義' in section.getText():
            ret = delEnter(section.find('div').getText())
            return ret
    return 'not found'
    

def getDefinition_concised(val:str) -> str:
    time.sleep(TIME_LIMIT_EACH_REQUEST)
    parms = findHref_con(val)
    if len(parms) == 0:
        return 'none'
    res = requests.get('https://dict.concised.moe.edu.tw/'+parms[0])
    soup = BeautifulSoup(res.text,'html.parser')
    return '<'+getIncludedWord(soup.head.title.getText(),'<','>')+'>'+ readDefinitionFromFrom_con(soup)

def getDefinition_revised(val:str) -> str:
    time.sleep(TIME_LIMIT_EACH_REQUEST)
    parms = findHref(val)
    if len(parms) == 0:
        return 'none'
    res = requests.get('https://dict.revised.moe.edu.tw/'+parms[0])
    soup = BeautifulSoup(res.text,'html.parser')
    return '<'+getIncludedWord(soup.head.title.getText(),'[',' :')+'>'+readDefinitionFromFrom(soup)

def getDefinition_both(val:str) -> str:
    ret = getDefinition_idi(delEnter(val))
    if ret != 'none':
        return '(成) ' + ret
    ret = getDefinition_concised(val)
    if ret != 'none':
        return '(簡) ' + ret
    ret = getDefinition_revised(val)
    if ret == 'none':
        return ret
    return '(修) '+ret


def findHref_idi(word:str) -> list:
    time.sleep(TIME_LIMIT_EACH_REQUEST)
    res = requests.get('https://dict.idioms.moe.edu.tw/idiomList.jsp',params={"idiom":word})
    soup = BeautifulSoup(res.text,'html.parser')
    filtered_herf = list()
    if('成語檢索' in soup.head.title.getText()):
        herfs = soup.find_all('a')
        for herf in herfs:
            if('idiomView' in str(herf)):
                filtered_herf.append(herf['href'])
    elif('成語檢視' in soup.head.title.getText()):
        filtered_herf.append("idiomList.jsp?idiom=%s" %(word))
    else:
        print('error:mapping lost')
    return filtered_herf

def readDefinitionFromForm_idi(soup:BeautifulSoup)->str:
    return soup.find('tr',id='row_mean').td.getText()

def getDefinition_idi(val:str)->str:
    time.sleep(TIME_LIMIT_EACH_REQUEST)
    params = findHref_idi(val)
    if len(params) == 0:
        return 'none'
    res = requests.get('https://dict.idioms.moe.edu.tw/'+params[0])
    soup = BeautifulSoup(res.text,'html.parser')
    return delEnter(readDefinitionFromForm_idi(soup))

if __name__ == '__main__':
    print(getDefinition_both('不見經傳'))
