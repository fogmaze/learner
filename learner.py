from typing import List
from source.core import Book,completePathFormat,delEnter
from source.idomLearner.IdiomBook import IdiomBook
from source.otherLearner.otherBook import OtherBook
from source.pinyinLearner.pinyinBook import PinyinBook
from source.writingLearner.WritingBook import WritingBook
import sys
from os import path
from argparse import ArgumentParser

BOOK_PATH_ROOT = './books/'

engines = {
    'pin':PinyinBook,
    'pinyin':PinyinBook,
    'idiom':IdiomBook,
    'other':OtherBook,
    'writing':WritingBook,
    'wri':WritingBook
}

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

def tester(book:Book,note:Book,inverse = False):
    try:
        print('enter command ( else->quiz, q->quit)')
        inp = input()
        while True:
            if inp == 'q':
                break
            test_que,test_ans,index = book.getRandWord()
            if inverse :
                buf = str(test_ans)
                test_ans = str(test_que)
                test_que = str(buf).replace(test_ans,'XXXX')
            print(test_que)
            input()
            print(test_ans)
            print('enter command ( else->quiz, q->quit, a-> add to note, d -> delete this[%s], e -> edit definition) (%d unfamiliar left)' %(book.items[index][0],book.getUnfamiliarLength()))
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

def adder(objs:List[Book]):
    print('enter a word or "q" for quit,"-e <engine>" to change engine')
    inp = input()
    NowEngine = objs[0].__class__
    while True:
        if inp == 'q':
            [obj.releaseIfNeed() for obj in objs]
            break
        if "-e" in inp and ' ' in inp:
            en = inp.split(' ')[1]
            for flag in engines:
                if en == flag:
                    NowEngine = engines[flag]
            inp = input()
            
        que,ans = NowEngine.askQuestionAndAnswer(inp)


        rets = [obj.add(delEnter(que),ans = delEnter(ans)) for obj in objs]
        [print(r) for r in rets]
        print('enter a word or "q" for quit,"d" to delete this[%s], "e" to edit definition, "eq" to edit question,"-e <engine>" to change engine' %(inp))

        if objs[0].__class__ != NowEngine:
            NowEngine = objs[0].__class__
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
    if mode.mode == 'add':
        ArgParser = ArgumentParser()
        ArgParser.add_argument('mode')
        ArgParser.add_argument('engine')
        ArgParser.add_argument('books',nargs='+')
        args,unknown = ArgParser.parse_known_args(cmd)
                
        bookEngine = OtherBook
        for engine in engines:
            if engine == args.engine:
                bookEngine = engines[engine]
                print('set to :' + engine)

        books = []
        for bookName in args.books:
            books.append(bookEngine(path.join(BOOK_PATH_ROOT,bookName)))
        adder(books)

    if mode.mode == 'test':
        ArgParser = ArgumentParser()
        ArgParser.add_argument("mode")
        ArgParser.add_argument('book')
        ArgParser.add_argument('-n','--note',dest='n')
        ArgParser.add_argument('-H',dest='test_hard',action="store_true")
        ArgParser.add_argument('--inv',dest='inv',action="store_true")
        args,unknown = ArgParser.parse_known_args(cmd)

        book = None
        if args.test_hard:
            book = Book(path.join(BOOK_PATH_ROOT,args.book,'hards'))
        else:
            book = Book(path.join(BOOK_PATH_ROOT,args.book))

        note = False
        if args.n:
            note = Book(path.join(BOOK_PATH_ROOT,args.n))
        elif not args.test_hard and path.isdir(path.join(BOOK_PATH_ROOT,args.book,'hards')):
            note = Book(path.join(BOOK_PATH_ROOT,args.book,'hards'))
        
        if args.inv:
            tester(book,note,inverse=True)
        else:
            tester(book,note)    


def ListOfListByRange(list:list,range:range)->list:
    return list[range.start:range.stop:range.step]

if __name__ == '__main__':

    argv = list(sys.argv)
    del argv[0]
    if len(argv) < 2:
        print('enter command:')
        argv = splitBlank(input())

    command(argv)


