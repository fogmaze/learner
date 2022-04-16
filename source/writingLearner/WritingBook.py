from source.pinyinLearner.pinyinBook import PinyinBook,findRanges
from source.core import *
from typing import Tuple,List


class WritingBook(Book):
    @staticmethod
    def getAnsFromInternet(que, mode='preset'):
        return super().getAnsFromInternet(que, mode)
    
    @staticmethod
    def askQuestionAndAnswer(inp: str) -> Tuple[str, str]:
        val = splitBlank(inp)

        if len(val) < 2:
            return
        que_orig = val[0]

        
        testingRange = range(0,len(que_orig))
        if len(inp) == 2:
            testingRange = findRanges([True if d == '1' else False for d in val[1]])[0]

        all_pinyin = PinyinBook.getAnsFromInternet(que_orig)
        if all_pinyin[0] == 'none0':
            all_pinyin = []
            for c in que_orig:
                all_pinyin.append(PinyinBook.getAnsFromInternet(c))
        
        que_last = que_orig[0:testingRange.start] + ' ' + MergeString(ListOfListByRange(all_pinyin,testingRange),mark=' ') + ' ' + que_orig[testingRange.stop:len(que_orig)]
        ans_last = ListOfListByRange(que_orig,testingRange)
        return que_last,ans_last