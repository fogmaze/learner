import sys
import os
from typing import Tuple

from source.core import Book
import source.idomLearner.findAns as dk

class IdiomBook(Book):
    @staticmethod
    def getAnsFromInternet(que, mode='preset'):
        return dk.getDefinition_both(que)
    @staticmethod
    def askQuestionAndAnswer(inp: str) -> Tuple[str, str]:
        return inp,IdiomBook.getAnsFromInternet(inp)