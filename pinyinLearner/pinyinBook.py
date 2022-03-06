
from core import Book
from pinyinLearner.findAns import getPinyin_concised


class PinyinBook(Book):
    @staticmethod
    def getAnsFromInternet(que, mode='preset'):
        return getPinyin_concised(que)