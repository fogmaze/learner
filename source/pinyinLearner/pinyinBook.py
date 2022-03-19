from typing import List,Tuple
from source.core import Book,splitBlank,ListOfListByRange,MarkString,MergeString
from source.pinyinLearner.findAns import getPinyin_concised


class PinyinBook(Book):
    @staticmethod
    def askQuestionAndAnswer(inp: str)->Tuple[str,str]:
        inp = splitBlank(inp)
        que = inp[0]
        testingRange = range(0,len(que))
        if len(inp) == 2:
            testingRange = range(int(inp[1]),int(inp[1]) + 1)
        ans = PinyinBook.getAnsFromInternet(que)

        if ans[0] == 'none1':
            return que + 'not found',ans[0]

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