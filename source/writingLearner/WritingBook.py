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

        if len(val) != 2:
            return
        que_orig = val[0]
        
        testingRange = [True if d == '1' else False for d in val[1]]

        all_pinyin = PinyinBook.getAnsFromInternet(que_orig)
        if all_pinyin[0] == 'none0' or all_pinyin[0] == 'none1':
            all_pinyin = []
            for ind,c in enumerate(que_orig):
                if testingRange[ind]:
                    all_pinyin.append(PinyinBook.getAnsFromInternet(c)[0])
                else:
                    all_pinyin.append('')
                    
        
        que_last = ''
        ans_last = ''

        for ind,d in enumerate(testingRange):
            if d:
                que_last += all_pinyin[ind] + ' '
                ans_last += que_orig[ind] + ' '
            else:
                que_last += que_orig[ind]
        
        return que_last,ans_last