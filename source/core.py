import random
import os
from typing import Tuple,List

TIME_LIMIT_EACH_REQUEST = 0.3

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
    

class Err(Exception):pass

class Book:
    def delWord(self,index:int):
        w_less_each = len(self.items)
        extraWeight = w_less_each - self.weighted[index]
        del self.items[index]
        #self.weighted = np.delete(self.weighted,index)
        del self.weighted[index]
        #self.weighted -= extraWeight / self.weighted.shape[0]
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
        
    def __init__(self,root_path = './'):
        try:
            self.isNew = False
            self.inited = True
            if root_path[len(root_path)-1] != '/':
                root_path += '/'
            if not os.path.isdir(root_path):
                self.createNewBookDir(root_path)
                self.isNew = True
            self.FILE_ROOT = root_path
            self.SAVE2RELEASE = True
            fl_ques = open(self.FILE_ROOT+'que.txt','r',encoding='utf-8')
            fl_Anss = open(self.FILE_ROOT+'ans.txt','r',encoding='utf-8')
            fl_weighted = None
            try:
                fl_weighted = open(self.FILE_ROOT+'weighted.txt','r',encoding='utf-8')
            except:
                pass
            self.items = list()
            self.weighted = list()
            for que in fl_ques:
                ans = fl_Anss.readline()
                self.items.append([delEnter(que),delEnter(ans)])

                if fl_weighted:                
                    self.weighted.append(float(fl_weighted.readline()))
                else:
                    self.weighted.append(1.0)
            ''
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

        print(sumList(self.weighted))
        w_less_each = len(self.items)
        self.weighted[which] = self.weighted[which] - w_less_each
        self.weighted = [(w + w_less_each/float(w_len)) for w in self.weighted]

        print(sumList(self.weighted))
        return self.items[which][0],self.items[which][1],which

    def release(self):
        self.inited = False
        if not self.SAVE2RELEASE:
            return
        fl_ques = open(self.FILE_ROOT+'que.txt','w',encoding='utf-8')
        fl_Anss = open(self.FILE_ROOT+'ans.txt','w',encoding='utf-8')

        for each in self.items:
            if each[0][len(each[0])-1] != '\n':
                each[0] += '\n'
            if each[1][len(each[1])-1] != '\n':
                each[1] += '\n'
            fl_ques.write(each[0])
            fl_Anss.write(each[1])
        
        fl_ques.close()
        fl_Anss.close()

        if os.path.isfile(self.FILE_ROOT+'weighted.txt'):
            fl_weighted = open(self.FILE_ROOT+'weighted.txt','w',encoding='utf-8')
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
        if path[len(path)-1] != '/':
            path+= '/'
        if not os.path.isdir(path):
            os.mkdir(path)
        with open(path+'que.txt','w'),open(path+'ans.txt','w'),open(path+'weighted.txt','w'):
            pass
    

def mergeBooks(dst:Book,books:List[Book])->Book:
    for book in books:
        [dst.weighted.append(w) for w in book.weighted]
        [dst.items.append(item) for item in book.items]
    dst.SAVE2RELEASE = False
    return dst

