
from core import Book
from pinyinLearner.findAns import getPinyin_concised


class PinyinBook(Book):
    def getAnsFromInternet(self,que, mode='preset'):
        return getPinyin_concised(que)