import sys
import os
from typing import Tuple

sys.path.insert(0,os.path.dirname(__file__))

from core import Book
import findAns as dk

class IdiomBook(Book):
    @staticmethod
    def getAnsFromInternet(que, mode='preset'):
        return dk.getDefinition_both(que)
    @staticmethod
    def askQuestionAndAnswer(inp: str) -> Tuple[str, str]:
        return inp,IdiomBook.getAnsFromInternet(inp)