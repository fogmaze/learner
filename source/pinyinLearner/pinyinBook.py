from typing import List,Tuple
from core import Book
from pinyinLearner.findAns import getPinyin_concised

def splitBlank(str:str)->List[str]:
    res = []
    inMark = False
    lastBlank = 0
    for i in range(len(str)):
        if str[i] == ' ' and not inMark:
            res.append(str[lastBlank:i].replace('"',''))
            lastBlank = i + 1
        elif str[i] == '"':
            if inMark:
                inMark = False
            else:
                inMark = True
        if i+1 == len(str):
            res.append(str[lastBlank:i+1].replace('"',''))
    return res


def ListOfListByRange(list:list,range:range)->list:
    return list[range.start:range.stop:range.step]

def MarkString(str:str,range:range):
    return str[0:range.start] + '[' + str[range.start:range.stop] + ']' + str[range.stop:len(str)]

def MergeString(list):
    if len(list) == 0:
        return
    ret = list[0]
    for i in range(1,len(list)):
        ret += ',' + list[i]
    return ret

class PinyinBook(Book):
    @staticmethod
    def askQuestionAndAnswer(inp: str)->Tuple[str,str]:
        inp = splitBlank(inp)
        que = inp[0]
        testingRange = range(0,len(que))
        if len(inp) == 2:
            testingRange = range(int(inp[1]),int(inp[1]) + 1)
        ans = PinyinBook.getAnsFromInternet(que)

        if ans[0] == 'none0':
            ans = []
            for c in que:
                ans_char = PinyinBook.getAnsFromInternet(c)[0]
                ans.append(ans_char)
        
        lastAns = ListOfListByRange(ans,testingRange) 

        if lastAns[0] == 'none0':
            print(lastAns)
            print("can't find answer, please enter yourself")
            lastAns = input()

        return MarkString(que,testingRange),MergeString(lastAns)


    @staticmethod
    def getAnsFromInternet(que, mode='preset'):
        return getPinyin_concised(que)