import sys
import os

sys.path.insert(0,os.path.dirname(__file__))

from core import Book
import findAns as dk

class IdiomBook(Book):
    def getAnsFromInternet(self,que, mode='preset'):
        return dk.getDefinition_both(que)
