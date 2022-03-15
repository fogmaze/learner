from re import I
from core import Book,completePathFormat,delEnter
from idomLearner.IdiomBook import IdiomBook
from otherLearner.otherBook import OtherBook
from pinyinLearner.pinyinBook import PinyinBook
import sys
from argparse import ArgumentParser

def splitBlank(str:str)->list:
    res = []
    inMark = False
    lastBlank = 0
    for i in range(len(str)):
        if str[i] == ' ' and not inMark:
            res.append(str[lastBlank:i].replace('"',''))
            lastBlank = i + 1
        elif str[i] == '"':
            if inMark:
                inMark = False
            else:
                inMark = True
        if i+1 == len(str):
            res.append(str[lastBlank:i+1].replace('"',''))
    return res

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
        if note:
            note.releaseIfNeed()
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
        




def command(cmd:list):

    ArgParser = ArgumentParser()
    ArgParser.add_argument('mode',choices=['add','test','merge'])
    mode,unknown = ArgParser.parse_known_args(cmd)
    print(mode.mode)
    if mode.mode == 'add':
        ArgParser = ArgumentParser()
        ArgParser.add_argument('-b','-book',dest='b',nargs='+')
        ArgParser.add_argument('-e','-engine',dest='e')
        args,unknown = ArgParser.parse_known_args(cmd)
        
        bookEngine = OtherBook
        if args.e == 'idiom':
            bookEngine = IdiomBook
        elif args.e == 'pin' or args.e == 'pinyin':
            bookEngine = PinyinBook

        books = []
        for bookName in args.b:
            books.append(bookEngine(bookName))
        adder(books)

    if mode.mode == 'test':
        ArgParser = ArgumentParser()
        ArgParser.add_argument('-b','-book',dest='b')
        ArgParser.add_argument('-n','--note',dest='n')
        ArgParser.add_argument('-e','-engine',dest='e')
        args,unknown = ArgParser.parse_known_args(cmd)

        book = Book(args.b)
        note = False
        if args.n:
            note = Book(args.n)
        tester(book,note)    


if __name__ == '__main__':
    
    print(IdiomBook.getAnsFromInternet('不見經傳'))
 
    argv = list(sys.argv)
    print(sys.argv)
    del argv[0]
    if len(argv) == 0:
        print('enter command:')
        argv = splitBlank(input())

    command(argv)


