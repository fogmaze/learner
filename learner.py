from re import I
from core import Book,completePathFormat,delEnter
from idomLearner.IdiomBook import IdiomBook
from otherLearner.otherBook import OtherBook
from pinyinLearner.pinyinBook import PinyinBook
import sys


def tester(book:Book,note:Book):
    try:
        print('enter command ( else->quiz, q->quit)')
        inp = input()
        while True:
            if inp == 'q':
                break
            test_que,test_ans,index = book.getRandWord()
            print(test_que)
            input()
            print(test_ans)
            print('enter command ( else->quiz, q->quit, a-> add to note, d -> delete this[%s], e -> edit definition) (%d unfamiliar left)' %(test_que,book.getUnfamiliarLength()))
            inp = input()
            if inp == 'e':
                print('enter new definition')
                inp = input()
                book.items[index][1] = inp
                print('changed')
                print('enter command ( else->quiz, q->quit)' %(test_que))
                inp = input()
            if inp == 'a' and note:
                if note.add(test_que,ans=test_ans):
                    print('added')
                else:
                    print('already added')
                print('enter command ( else->quiz, q->quit)')
                inp = input()
            elif inp == 'd':
                book.delWord(index)
                #mkAnsFile.deleteWord(index,file_root=book)
                print('deleted')
                print('enter command ( else->quiz, q->quit)')
                inp = input()
    finally:
        book.release()

def adder(objs:list):
    print('enter a word or "q" for quit,"-e <engine>" to change engine')
    inp = input()
    findAnsMethod = objs[0].getAnsFromInternet
    while True:
        if inp == 'q':
            [obj.releaseIfNeed() for obj in objs]
            break
        if "-e" in inp and ' ' in inp:
            en = inp.split(' ')[1]
            if en == 'idiom':
                findAnsMethod = IdiomBook.getAnsFromInternet
            elif en == 'pin' or en == 'pinyin':
                findAnsMethod = PinyinBook.getAnsFromInternet
            elif en == 'self':
                findAnsMethod = OtherBook.getAnsFromInternet
            else:
                print('undefined:' + en)
            inp = input()
        definition = findAnsMethod(inp)
        rets = [obj.add(delEnter(inp),ans = definition) for obj in objs]
        [print(r) for r in rets]
        print('enter a word or "q" for quit,"d" to delete this[%s], "e" to edit definition, "eq" to edit question,"-e <engine>" to change engine' %(inp))

        if objs[0].getAnsFromInternet != findAnsMethod:
            findAnsMethod = objs[0].getAnsFromInternet
            print('set engine to defaut')

        inp = input()
        if inp == 'd':
            [obj.delWord(len(obj.items)-1)for obj in objs]
            print('enter a word or "q" for quit,"-e <engine>" to change engine')
            inp = input()
        if inp == 'e':
            print('enter new definition')
            inp = input()
            for obj in objs:
                obj.items[len(obj.items)-1][1] = inp
            print('changed')
            print('enter a word or "q" for quit,"-e <engine>" to change engine')
            inp = input()
        if inp == 'eq':
            print('enter new question')
            inp = input()
            for obj in objs:
                obj.items[len(obj.items)-1][0] = inp
            print('changed')
            print('enter a word or "q" for quit,"-e <engine>" to change engine')
            inp = input()
        



if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('enter command:')
        sys.argv = input().split(' ')
    previous_arg = ''
    mode = 'none'
    Args = {}
    for arg in sys.argv:
        if arg == '--add':
            mode = 'add'
            Args['bookClass'] = OtherBook
            previous_arg = arg
            continue
        elif arg == '--test':
            mode = 'test'
            previous_arg = arg
            continue
        elif arg == '--merge':
            mode = 'merge'
            previous_arg = arg
            continue

        if mode == 'test':
            if previous_arg == '-b':
                Args['book'] = Book(arg)
            if previous_arg == '-n':
                Args['note'] = Book(arg)
        elif mode == 'add':
            if arg == 'idiom':
                Args['bookClass'] = IdiomBook
                print('serch mode set to "idiom"')
            elif arg == 'pinyin' or arg == 'pin':
                Args['bookClass'] = PinyinBook
                print('serch mode set to "pinyin"')
            if previous_arg == '-b':
                if not 'books' in Args:
                    Args['books'] = []
                Args['books'].append(Args['bookClass'](arg))
                print('add to: '+arg)
        elif mode == 'merge':
            if previous_arg == '-o':
                Args['object'] = Book(arg)
            if previous_arg == '-f':
                Args['inFile'] = open(arg,'r',encoding='utf-8')
                Args['inAns'] = None
            if previous_arg == '-b':
                Args['inFile'] = open(completePathFormat(arg)+'que.txt','r',encoding='utf-8')
                Args['inAns'] = open(completePathFormat(arg)+'ans.txt','r',encoding='utf-8')
        previous_arg = arg

    if mode == 'test':
        if not 'book' in Args:
            Args['book'] = Book('All_idioms')
        if not 'note' in Args:
            Args['note'] = False
        tester(Args['book'],Args['note'])
        Args['book'].releaseIfNeed()
        if Args['note']:
            Args['note'].releaseIfNeed()
        
    if mode == 'add':
        if not 'books' in Args:
            Args['books'] = [Args['bookClass']('All')]
            print('preset:add to All')
        adder(Args['books'])
        

    if mode == 'merge':
        if not 'object' in Args or not 'inFile' in Args:
            print('error file input')
        else:
            for que in Args['inFile']:
                Args['object'].add(que,ans=Args['inAns'].readline())
            print('merged')
            Args['object'].releaseIfNeed()
    

    