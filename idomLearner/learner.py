import mkAnsFile
import sys
from randWords import getRandWord
import numpy as np

def tester(book:str,note = './HardOnes'):
    try:
        Ques = getRandWord(book)
        print('enter command ( else->quiz, q->quit)')
        inp = input()
        while True:
            if inp == 'q':
                break
            test_idom,test_ans,index = Ques.getRandWord()
            print(test_idom)
            input()
            print(test_ans)
            print('enter command ( else->quiz, q->quit, a-> add to note, d -> delete this[%s], e -> edit definition) (%d unfamiliar left)' %(test_idom[0:test_idom.find('\n')],Ques.getUnfamiliarLength()))
            inp = input()
            if inp == 'e':
                print('enter new definition')
                inp = input()
                Ques.idoms[index][1] = inp
                print('changed')
                print('enter command ( else->quiz, q->quit, a-> add to note, d-> delete this[%s])' %(test_idom))
                inp = input()
            if inp == 'a':
                if mkAnsFile.AddWord2AnsFile(test_idom,definition=test_ans,file_root=note) == 'already been added':
                    print('already been added')
                else:
                    print('added')
                print('enter command ( else->quiz, q->quit)')
                inp = input()
            elif inp == 'd':
                Ques.delWord(index)
                #mkAnsFile.deleteWord(index,file_root=book)
                print('deleted')
                print('enter command ( else->quiz, q->quit)')
                inp = input()
    finally:
        Ques.release()

if __name__ == '_main_':
    if(len(sys.argv)==1):
        tester('./All_Idoms')
    else:
        #extra mode
        if sys.argv[1] == '--add':
            #add idoms to main folder by file
            if sys.argv[2] == '-wf':
                while True:
                    print('enter a idom or "q" for quit')
                    inp = input()
                    if inp == 'q':
                        break
                    definition = mkAnsFile.AddWord2AnsFile(inp,file_root=sys.argv[3])
                    print('definition: '+ definition)
            #add idoms to main folder by typing
            elif sys.argv[2] == '-w':
                while True:
                    print('enter a idom or "q" for quit')
                    inp = input()
                    if inp == 'q':
                        break
                    definition = mkAnsFile.AddWord2AnsFile(inp,file_root='./All_Idoms')
                    print('definition: '+ definition)
            else:
                print(sys.argv[2])
        elif sys.argv[1] == '--test':
            #test by file
            if sys.argv[2] == '-f':
                tester(sys.argv[3])
        elif sys.argv[1] == '--make':
            mkAnsFile.createNewIdomFiles(sys.argv[2])
        elif sys.argv[1] == 'check':
            Ques = getRandWord(root_path='./All_Idoms')
            print(np.sum(Ques.weighted))
            Ques.release()

class arrayStream:
    def __init__(self,list:list):
        self.list = list

    def next(self):
        if not self.availible():
            return None
        d = self.list[0]
        del self.list[0]
        return d

    def availible(self)->bool:
        return len(self.list)>0


if __name__ == '__main__':
    arg_stream = arrayStream(sys.argv)
    while arg_stream.availible():
        arg = arg_stream.next()
        #test mode
        if arg == '--test':
            book = 'All_Idoms'
            note = 'HardOnes'
            while True:
                arg_test = arg_stream.next()
                if arg_test == '-b':
                    book = arg_stream.next()
                elif arg_test == '-n':
                    note = arg_stream.next()
                else:
                    arg_stream.list.insert(0,arg_test)
                    break
            tester(book,note=note)
        if arg == '--add':
            mode = 'file'
            book = './All_Idoms'
            while True:
                arg_add = arg_stream.next()
                if arg_add == '-w':
                    mode = 'type'
                elif arg_add == '-b':
                    book = arg_stream.next()
                elif arg_add == '-f':
                    with open(arg_stream.next(),'r',encoding='utf-8') as f:
                        mkAnsFile.AddFIle2AnsFile(f,book)
                else:
                    arg_stream.list.insert(0,arg_add)
                    break
            if mode == 'type':
                while True:
                    print('enter a idom or "q" for quit')
                    inp = input()
                    if inp == 'q':
                        break
                    definition = mkAnsFile.AddWord2AnsFile(inp,file_root=book)
                    print('definition: '+ definition)
            

