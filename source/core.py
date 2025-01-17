import json
import platform
import random
import os
import sys
from typing import Tuple,List


TIME_LIMIT_EACH_REQUEST = 0.3

BOOK_BASE = './books/'

if platform.system() == 'Windows':
    def myopen(name:str,mode,encoding='utf-8'):
        return open(name.replace('/','\\'),mode,encoding=encoding)
else:
    def myopen(name:str,mode,encoding='utf-8'):
        return open(name,mode,encoding=encoding)

def splitBlank(str:str)->List[str]:
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


def ListOfListByRange(list:list,range:range)->list:
    return list[range.start:range.stop:range.step]

def MarkString(str:str,range:range):
    return str[0:range.start] + '[' + str[range.start:range.stop] + ']' + str[range.stop:len(str)]

def MarksString(str:str,ranges:List[range]):
    marked = [False for c in str]
    marked.append(False)
    nstr = str + ' '
    for r in ranges:
        for i in r:
            marked[i] = True
    res = ''
    Marking = False
    for ind,c in enumerate(nstr):
        if marked[ind] and not Marking:
            Marking = True
            res += '['
        if not marked[ind] and Marking:
            Marking = False
            res += ']'
        res += c
    return res 

def MergeString(list,mark = ','):
    if len(list) == 0:
        return
    ret = list[0]
    for i in range(1,len(list)):
        ret += mark + list[i]
    return ret
def my_rand(start,stop):
    s = random.random()
    return start + s * (stop-start)

def delEnter(s:str)->str:
    new_str = ''
    for c in s:
        if c != '\n' and c != '\r':
            new_str += c
    return new_str

def completePathFormat(s:str)->str:
    if s[len(s)-1] != '/':
        s+= '/'
    return s

def sumList(list:List[float])->float:
    sum = 0
    for item in list:
        sum += item
    return sum

def preDirName(filename:str)->str:
    return os.path.basename(os.path.dirname(filename))
    

class Err(Exception):pass

class Book:
    def delWord(self,index:int):
        extraWeight = 1.0 - self.weighted[index]
        del self.items[index]
        del self.weighted[index]
        self.weighted = [w-(extraWeight/len(self.weighted)) for w in self.weighted]
        


    @staticmethod
    def askQuestionAndAnswer(inp:str)->Tuple[str,str]:
        ans = Book.getAnsFromInternet(inp)
        return inp,ans

    @staticmethod
    def getAnsFromInternet(que,mode = 'preset'):
        raise Err('not defined')

    def add(self, que, ans=None) -> str:
        que = delEnter(que)
        for added_item in self.items:
            if que == added_item[0]:
                return None
        if ans:
            ans = delEnter(ans)
            self.items.append([que,ans])
            self.weighted.append(1.0)
            #self.weighted = np.append(self.weighted,1)
            return ans
        ans_got = self.getAnsFromInternet(que)
        self.items.append([que,delEnter(ans_got)])
        self.weighted.append(1.0)
        #Eself.weighted = np.append(self.weighted,1)
        return ans_got
    
    def __init__(self): 
        self.inited = True
        self.FILE_ROOT = ''
        self.SAVE2RELEASE = True
        self.items = []
        self.weighted = []
        
    def __init__(self,root_path,weighted_file = True,mode = 'default'):
        self.file_mode = mode
        self.inited = True
        self.FILE_ROOT = root_path
        self.SAVE2RELEASE = True
        self.saveWeightFile = weighted_file
        if root_path[len(root_path)-1] != '/':
            root_path += '/'
        
        if mode == 'json':
            if not os.path.isfile(root_path + 'book.json'):
                print('no file name :' + root_path)
                print('press "y" to create, or other to quit')
                confirm = input()
                if not confirm == 'y':
                    sys.exit()
                    return
                self.createNewBookDir(root_path)
                self.isNew = True
            self.file_mode = 'json'

            js_f = myopen(self.FILE_ROOT+'book.json','r',encoding='utf-8')
            dc = json.load(js_f)
            self.items = [ [data[0],data[1]] for data in dc['data'] ]
            self.weighted = [ data[2] for data in dc['data'] ]
            return
            
        try:
            if not os.path.isfile(root_path + 'que.txt'):
                print('no file name :' + root_path)
                print('press "y" to create, or other to quit')
                confirm = input()
                if not confirm == 'y':
                    sys.exit()
                self.createNewBookDir(root_path)
                self.isNew = True
            
            fl_ques = myopen(os.path.join(self.FILE_ROOT,'que.txt'),'r',encoding='utf-8')
            fl_Anss = myopen(os.path.join(self.FILE_ROOT,'ans.txt'),'r',encoding='utf-8')
            fl_weighted = None
            if weighted_file:
                try:
                    fl_weighted = myopen(os.path.join(self.FILE_ROOT,'weighted.txt'),'r',encoding='utf-8')
                except:
                    print('cannot open weighted')
            self.items = list()
            self.weighted = list()
            for que in fl_ques:
                ans = fl_Anss.readline()
                self.items.append([delEnter(que),delEnter(ans)])

            if fl_weighted:
                self.weighted = [float(w) for w in fl_weighted]
            else:
                self.weighted = [1.0 for n in self.items]

            if len(self.weighted) != len(self.items):
                print('weighted file error. reopening without weighted file')
                self.weighted = [1.0 for n in self.items]
                    
            
        except Exception as e:
            print('cannot open book {} by getting error:'.format(self.FILE_ROOT))
            print(str(e))
            sys.exit()
        finally:
            fl_ques.close()
            fl_Anss.close()
            if fl_weighted:
                fl_weighted.close()
        

    def getUnfamiliarLength(self) -> int:
        return len([w for w in self.weighted if w > 1])

    def getRandWord(self):
        w_len = len(self.weighted)
        w_sum = sumList([w for w in self.weighted if w > 0])
        seak = my_rand(0,w_sum)
        which = 0
        i = 0
        num = 0
        while(True):
            if i == len(self.weighted):
                break
            if self.weighted[i] < 0:
                i += 1
                continue
            if seak-num < self.weighted[i]:
                which = i
                break
            num += self.weighted[i]
            i += 1
        w_less_each = len(self.items)
        self.weighted[which] = self.weighted[which] - w_less_each
        self.weighted = [(w + w_less_each/float(w_len)) for w in self.weighted]
        return self.items[which][0],self.items[which][1],which

    def release(self):
        self.inited = False
        if not self.SAVE2RELEASE:
            return
        
        if self.file_mode == 'json':
            data_dc = {}
            data_dc['data'] = []
            for i in range(len(self.items)):
                data_dc['data'].append([self.items[i][0],self.items[i][1],self.weighted[i]])
            with myopen(os.path.join(self.FILE_ROOT,'book.json'),'w',encoding='utf-8') as f:
                f.write(json.dumps(data_dc,ensure_ascii=False,indent=4))
            return
            

        fl_ques = myopen(os.path.join(self.FILE_ROOT,'que.txt'),'w',encoding='utf-8')
        fl_Anss = myopen(os.path.join(self.FILE_ROOT,'ans.txt'),'w',encoding='utf-8')

        for each in self.items:
            if len(each[0]) == 0:
                continue
            if each[0][len(each[0])-1] != '\n':
                each[0] += '\n'
            if each[1][len(each[1])-1] != '\n':
                each[1] += '\n'
            fl_ques.write(each[0])
            fl_Anss.write(each[1])
        
        fl_ques.close()
        fl_Anss.close()

        if self.saveWeightFile:
            fl_weighted = myopen(os.path.join(self.FILE_ROOT,'weighted.txt'),'w',encoding='utf-8')
            for w in self.weighted:
                fl_weighted.write(str(w) + '\n')
            fl_weighted.close()

    def releaseIfNeed(self):
        if self.inited:
            self.release()

    def __del__(self):
        if self.inited:
            print('class<getRandWord> releasing automatically')
            self.release()
    
    def createNewBookDir(self,path:str):
        if self.file_mode == 'json':
            if path[len(path)-1] != '/':
                path+= '/'
            if not os.path.isdir(path):
                os.mkdir(path)
            with myopen(path+'book.json','w',encoding='utf-8') as f:
                json.dump({'data':[]},f)
            return
        if path[len(path)-1] != '/':
            path+= '/'
        if not os.path.isdir(path):
            os.mkdir(path)
        with myopen(path+'que.txt','w'),myopen(path+'ans.txt','w'),myopen(path+'weighted.txt','w'):
            pass
    

class BookViewer(Book):
    def __init__(self,search_path):
        self.bookset = []
        self.bookname = []
        filenames = os.listdir(search_path)
        while True:
            if len(filenames) == 0:
                break
            filename = filenames.pop(0)
            if os.path.isdir(filename):
                filenames.append(os.listdir(filename))
            if 'book.json' in filename:
                self.bookset.append(Book(filename))
                self.bookname.append(preDirName(filename))
    def getRandWord(self):
        pass

def mergeBooks(dst:Book,books:List[Book])->Book:
    for book in books:
        [dst.weighted.append(w) for w in book.weighted]
        [dst.items.append(item) for item in book.items]
    dst.SAVE2RELEASE = False
    return dst

def convertFile(name:str):
    book_old = Book(name,mode='')
    data_dc = {}
    data_dc['data'] = []
    for i in range(len(book_old.items)):
        data_dc['data'].append([book_old.items[i][0],book_old.items[i][1],book_old.weighted[i]])
    with myopen(os.path.join(name,'book.json'),'w',encoding='utf-8') as f:
        f.write(json.dumps(data_dc,ensure_ascii=False,indent=4))

def init():
    global TITLE_EACH_QUESTION
    TITLE_EACH_QUESTION = ''
    

if __name__ == "__main__":
    pass