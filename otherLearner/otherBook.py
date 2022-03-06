from core import Book

class OtherBook(Book):
    @staticmethod
    def getAnsFromInternet(que, mode='preset'):
        print('edter the answer of the quetion')
        return input()