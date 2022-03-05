import requests
from bs4 import BeautifulSoup
import time
from core import TIME_LIMIT_EACH_REQUEST,delEnter

def getIncludedWord(s:str,c_start:str,c_end:str)->str:
    return s[s.find(c_start)+1:s.find(c_end)]

def findHref_con(word:str) -> list:
    time.sleep(TIME_LIMIT_EACH_REQUEST)
    res = requests.get('https://dict.concised.moe.edu.tw/search.jsp',params={"word":word})
    soup = BeautifulSoup(res.text,'html.parser')
    filtered_herf = list()
    '''
    if('基本檢索' in soup.head.title.getText()):
        herfs = soup.find_all('a')
        for herf in herfs:
            if('dictView' in str(herf)):
                filtered_herf.append(herf['href'])
    '''
    if '基本檢索' in soup.head.title.getText():
        filtered_herf = [a['href'] for a in soup.find_all('a') if 'dictView' in str(a)]
    elif '辭典檢視' in soup.head.title.getText() :
        filtered_herf.append("search.jsp?word=%s" %(word))
    else:
        print('error:mapping lost')
    return filtered_herf

def readPinyinFromForm_con(soup:BeautifulSoup) -> str:
    ret = ''
    i = 1
    for section in soup.find('article').find_all('section'):
        if '注　　音' in section.getText():
            ret = delEnter(section.getText())
            return ret
    return 'not found'

def getPinyin_concised(val:str) -> str:
    time.sleep(TIME_LIMIT_EACH_REQUEST)
    parms = findHref_con(val)
    print(val)
    if len(parms) == 0:
        return 'none0'
    res = requests.get('https://dict.concised.moe.edu.tw/'+parms[0])
    soup = BeautifulSoup(res.text,'html.parser')
    if delEnter(val) in soup.head.title.getText():
        return readPinyinFromForm_con(soup)
    return 'none1'

