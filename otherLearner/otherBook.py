from core import Book
from typing import Tuple

class OtherBook(Book):
    @staticmethod
    def getAnsFromInternet(que, mode='preset'):
        print('edter the answer of the quetion')
        return input()
    @staticmethod
    def askQuestionAndAnswer(inp: str) -> Tuple[str, str]:
        return inp,OtherBook.getAnsFromInternet(inp)