from typing import List
from core import Book,completePathFormat,delEnter
from idomLearner.IdiomBook import IdiomBook
from otherLearner.otherBook import OtherBook
from pinyinLearner.pinyinBook import PinyinBook
import sys
from argparse import ArgumentParser


engines = {
    'pin':PinyinBook,
    'pinyin':PinyinBook,
    'idiom':IdiomBook,
    'other':OtherBook
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
                test_que = str(buf)
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
    print(mode.mode)
    if mode.mode == 'add':
        ArgParser = ArgumentParser()
        ArgParser.add_argument('-b','-book',dest='b',nargs='+')
        ArgParser.add_argument('-e','-engine',dest='e')
        args,unknown = ArgParser.parse_known_args(cmd)
        
        bookEngine = OtherBook
        for engine in engines:
            if engine == args.e:
                bookEngine = engines[engine]
                print('set to :' + engine)

        books = []
        for bookName in args.b:
            books.append(bookEngine(bookName))
        adder(books)

    if mode.mode == 'test':
        ArgParser = ArgumentParser()
        ArgParser.add_argument('-b','--book',dest='b')
        ArgParser.add_argument('-n','--note',dest='n')
        ArgParser.add_argument('-e','-engine',dest='e')
        ArgParser.add_argument('--inv',dest='inv',action="store_true")
        args,unknown = ArgParser.parse_known_args(cmd)

        book = Book(args.b)
        note = False
        if args.n:
            note = Book(args.n)
        if args.inv:
            tester(book,note,inverse=True)
        else:
            tester(book,note)    


def ListOfListByRange(list:list,range:range)->list:
    return list[range.start:range.stop:range.step]

if __name__ == '__main__':
    argv = list(sys.argv)
    print(sys.argv)
    del argv[0]
    if len(argv) == -1:
        print('enter command:')
        argv = splitBlank(input())

    command(argv)


