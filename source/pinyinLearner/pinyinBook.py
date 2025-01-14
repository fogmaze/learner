from typing import List,Tuple
from source.core import Book, MarksString,splitBlank,ListOfListByRange,MergeString
from source.pinyinLearner.findAns import getPinyin_concised

def findRanges(data:List[bool])->List[range]:
    ndata = list(data)
    ndata.append(False)
    res = []
    inArange = False
    nstart = None
    for ind,b in enumerate(ndata):
        if b:
            if not inArange:
                inArange = True
                nstart = ind
        else:
            if inArange:
                inArange = False
                res.append(range(nstart,ind))
    return res


class PinyinBook(Book):
    @staticmethod
    def askQuestionAndAnswer(inp: str)->Tuple[str,str]:
        inp = splitBlank(inp)
        que = inp[0]

        testingRange_str = inp[1] if len(inp) == 2 else input('pls enter testing area:')
        testingRanges = findRanges([True if d == '1' else False for d in testingRange_str])

        ans = PinyinBook.getAnsFromInternet(que)

        if ans[0] == 'none0' or ans[0] == 'none1':
            ans = []
            for c in que:
                ans_char = PinyinBook.getAnsFromInternet(c)[0]
                ans.append(ans_char)
        lastAns = []
        for r in testingRanges:
            lastAns.extend(ListOfListByRange(ans,r))

        if lastAns[0] == 'none0':
            print(lastAns)
            print("can't find answer, please enter yourself")
            lastAns = [input()]
        return MarksString(que,testingRanges),MergeString(lastAns)


    @staticmethod
    def getAnsFromInternet(que, mode='preset'):
        return getPinyin_concised(que)